# ==========================================================
# Indigenous Digital Library
# IFQ582 - Assignment 2
# Author: Ted Brennan
#
# File: app.py
#
# PURPOSE
# -------
# This is the main Flask application.
#
# Flask acts as the Controller in the Model-View-Controller
# architecture.
#
# Controller responsibilities:
# • Receive browser requests
# • Call the Model when database data is needed
# • Pass data to HTML templates
# • Return completed pages to the browser
#
# ==========================================================

# ----------------------------------------------------------
# Import Required Libraries
# ----------------------------------------------------------

from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from datetime import datetime
import mysql.connector

# Import database functions from the Model layer
from models.database import get_database_connection
from models.database import get_all_collection_items
from models.database import get_collection_item_by_id
from models.database import search_collection_items

# ----------------------------------------------------------
# Create Flask Application
# ----------------------------------------------------------
app = Flask(__name__)

# ----------------------------------------------------------
# Database Route
# ----------------------------------------------------------
# This route confirms that Flask can connect to the MySQL
# database.
# ----------------------------------------------------------

@app.route("/database-test")
def database_test():

    connection = get_database_connection()

    if connection.is_connected():

        connection.close()

        return "<h2>✅ Successfully connected to the Indigenous Library database.</h2>"

    return "<h2>❌ Database connection failed.</h2>"

# ============================================================
# LOGIN REQUIRED DECORATOR
# ============================================================

def login_required(f):
    """
    Prevents users from accessing protected pages
    unless they are logged in.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):

        # Check whether the user has logged in
        if "user_id" not in session:

            flash("Please log in to continue.")

            return redirect(url_for("login"))

        return f(*args, **kwargs)

    return decorated_function

# ============================================================
# ============================================================
# ============================================================
# ============================================================
# MYSQL LOGIN, LOGOUT AND SESSION MANAGEMENT
# ============================================================

# Used by Flask to protect session data
app.secret_key = "dev-secret-key-change-later"

# ============================================================
# MYSQL DATABASE CONNECTION
# ============================================================

def get_db_connection():
    """
    Creates a connection to the MySQL database.
    Update the password if your MySQL password is different.
    """

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Carltonblues50!",
        database="ifq582_assignment"
    )

# ============================================================
# ACCESS REQUEST DATABASE HELPERS
# ============================================================

def create_access_request(user_id, item_id, reason):
    """
    Creates a new access request.
    """

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO access_requests
        (
            item_id,
            user_id,
            reason,
            request_status,
            request_date
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s
        )
    """, (
        item_id,
        user_id,
        reason,
        "Pending",
        datetime.now()
    ))

    connection.commit()

    cursor.close()
    connection.close()


def check_existing_access_request(user_id, item_id):
    """
    Checks whether the logged-in user already has an
    active request for this item.
    """

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM access_requests
        WHERE user_id = %s
          AND item_id = %s
          AND request_status IN ('Pending', 'Approved')
    """, (user_id, item_id))

    existing_request = cursor.fetchone()

    cursor.close()
    connection.close()

    return existing_request

# ============================================================
# LOGIN PAGE
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Shows the login page and checks login details
    against the MySQL users table.
    """

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                user_id,
                full_name,
                email,
                role
            FROM users
            WHERE email = %s
              AND password_hash = %s
        """, (email, password))

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:
            session["user_id"] = user["user_id"]
            session["user_name"] = user["full_name"]
            session["user_email"] = user["email"]
            session["user_role"] = user["role"]

            flash("Login successful.")
            return redirect(url_for("home"))

        flash("Invalid email or password.")

    return render_template("login.html")

# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():
    """
    Logs the user out by clearing the session.
    """

    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("login"))

# ============================================================
# ROLE CHECK HELPER
# ============================================================

def user_has_role(required_role):
    """
    Checks whether the logged-in user has the required role.
    """

    return session.get("user_role") == required_role

# ============================================================
# GET USER ACCESS REQUESTS HELPER
# ============================================================

def get_user_access_requests(user_id):
    """
    Retrieves all access requests submitted by the logged-in user.
    Joins access_requests to collection_items so the page can show item titles.
    """

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            ar.request_id,
            ar.item_id,
            ci.title,
            ar.reason,
            ar.request_status,
            ar.request_date
        FROM access_requests ar
        JOIN collection_items ci
            ON ar.item_id = ci.item_id
        WHERE ar.user_id = %s
        ORDER BY ar.request_date DESC
    """, (user_id,))

    requests = cursor.fetchall()

    cursor.close()
    connection.close()

    return requests

# ==========================================================
# ==========================================================
# ==========================================================
# ============================================================
# HOME PAGE Route
# ============================================================

@app.route("/")
def home():
    return render_template("home.html")


# ==========================================================
# ==========================================================
# ==========================================================
# ==========================================================
# ----------------------------------------------------------
# Browse Collection Route
# ----------------------------------------------------------
#
# This route displays collection items.
#
# If the user enters a search term, Flask sends that term
# to the Model layer and retrieves matching records.
#
# If no search term is entered, all collection items are
# displayed.
#
# Example:
#
# /collections
# /collections?search=basket
#
# ----------------------------------------------------------

@app.route("/collections")
@login_required
def collections():

    search_term = request.args.get("search", "")

    if search_term:

        items = search_collection_items(search_term)

    else:

        items = get_all_collection_items()

    return render_template(
        "collections.html",
        items=items,
        search_term=search_term
    )

# ==========================================================
# ==========================================================
# ==========================================================
# ==========================================================
# ----------------------------------------------------------
# Collection Item Details Route
# ----------------------------------------------------------
#
# This route displays one collection item based on its
# item_id from the database.
#
# Example:
#
# /collection/1
# /collection/2
# /collection/3
#
# ----------------------------------------------------------

@app.route("/collection/<int:item_id>")
@login_required
def collection_detail(item_id):

    item = get_collection_item_by_id(item_id)

    if item is None:
        return "<h2>Collection item not found.</h2>", 404

    return render_template("collection_detail.html", item=item)


# ============================================================
# ============================================================
# ============================================================
# ============================================================
# REQUEST ACCESS ROUTE
# ============================================================

@app.route("/request-access/<int:item_id>", methods=["GET", "POST"])
@login_required
def request_access(item_id):
    """
    Allows a logged-in user to request access to a restricted
    collection item.
    """

    item = get_collection_item_by_id(item_id)

    if item is None:
        return "<h2>Collection item not found.</h2>", 404

    existing_request = check_existing_access_request(
        session["user_id"],
        item_id
    )

    if request.method == "POST":

        reason = request.form.get("reason")

        if existing_request:
            flash("You already have an active access request for this item.")
            return redirect(url_for("collection_detail", item_id=item_id))

        create_access_request(
            session["user_id"],
            item_id,
            reason
        )

        flash("Your access request has been submitted for review.")
        return redirect(url_for("collection_detail", item_id=item_id))

    return render_template(
        "request_access.html",
        item=item,
        existing_request=existing_request
    )


# ============================================================
# ============================================================
# ============================================================
# ============================================================
# MY REQUESTS ROUTE
# ============================================================

@app.route("/my-requests")
@login_required
def my_requests():
    """
    Shows all access requests submitted by the logged-in user.
    """

    requests = get_user_access_requests(session["user_id"])

    return render_template(
        "my_requests.html",
        requests=requests
    )

# ============================================================
# ============================================================
# ============================================================
# ============================================================
# Reviewer Dashboard
# ============================================================

@app.route("/reviewer-dashboard")
def reviewer_dashboard():

    if not session.get("user_id"):
        return redirect(url_for("login"))

    if session.get("user_role") not in ["reviewer", "admin"]:
        return "Access denied: reviewer access required.", 403

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Dashboard summary cards based on access request status
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM access_requests
        WHERE request_status = 'Pending'
    """)
    pending_count = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM access_requests
        WHERE request_status = 'Approved'
    """)
    approved_count = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM access_requests
        WHERE request_status = 'Rejected'
    """)
    rejected_count = cursor.fetchone()["total"]

    # Pending access requests awaiting reviewer decision
    cursor.execute("""
        SELECT
            ar.request_id,
            ar.item_id,
            ar.user_id,
            ar.reason,
            ar.request_status,
            ar.request_date,
            ci.title,
            ci.description
        FROM access_requests ar
        JOIN collection_items ci
            ON ar.item_id = ci.item_id
        WHERE ar.request_status = 'Pending'
        ORDER BY ar.request_date DESC
    """)

    pending_items = cursor.fetchall()

    # Recent reviewer activity / audit log preview
# Recent reviewer activity / audit log preview
    cursor.execute("""
        SELECT
            rd.decision_id,
            rd.request_id,
            rd.reviewer_id,
            rd.decision,
            rd.comments,
            rd.decision_date,
            ci.title,
            ar.request_status,
            u.full_name AS reviewer_name
        FROM review_decisions rd

        JOIN access_requests ar
            ON rd.request_id = ar.request_id

        JOIN collection_items ci
            ON ar.item_id = ci.item_id

        JOIN authorised_reviewers auth
            ON rd.reviewer_id = auth.reviewer_id

        JOIN users u
            ON auth.user_id = u.user_id

        ORDER BY rd.decision_date DESC

        LIMIT 5
    """)

    recent_activity = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "reviewer_dashboard.html",
        pending_count=pending_count,
        approved_count=approved_count,
        rejected_count=rejected_count,
        pending_items=pending_items,
        recent_activity=recent_activity
    )

# ============================================================
# ============================================================
# ============================================================
# ============================================================
# Review Access Request Page + Decision Submission
# ============================================================

@app.route("/review-request/<int:request_id>", methods=["GET", "POST"])
def review_item(request_id):

    if not session.get("user_id"):
        return redirect(url_for("login"))

    if session.get("user_role") not in ["reviewer", "admin"]:
        return "Access denied: reviewer access required.", 403

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        decision = request.form.get("decision")
        comments = request.form.get("comments")

        if decision not in ["Approved", "Rejected"]:
            cursor.close()
            conn.close()
            return "Invalid review decision.", 400

        # Find authorised reviewer record for logged-in user
        cursor.execute("""
            SELECT reviewer_id
            FROM authorised_reviewers
            WHERE user_id = %s
        """, (session.get("user_id"),))

        reviewer = cursor.fetchone()

        if not reviewer:
            cursor.close()
            conn.close()
            return "Reviewer profile not found for this logged-in user.", 403

        reviewer_id = reviewer["reviewer_id"]

        # 1. Update the access request status
        cursor.execute("""
            UPDATE access_requests
            SET request_status = %s
            WHERE request_id = %s
        """, (decision, request_id))

        # 2. Insert reviewer decision audit record
        cursor.execute("""
            INSERT INTO review_decisions
                (request_id, reviewer_id, decision, comments)
            VALUES
                (%s, %s, %s, %s)
        """, (
            request_id,
            reviewer_id,
            decision,
            comments
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(f"Access request has been {decision.lower()} successfully.", "success")
        return redirect(url_for("reviewer_dashboard"))

    # Load access request details
    cursor.execute("""
        SELECT
            ar.request_id,
            ar.item_id,
            ar.user_id,
            ar.reason,
            ar.request_status,
            ar.request_date,
            ci.title,
            ci.description,
            ci.status AS item_status
        FROM access_requests ar
        JOIN collection_items ci
            ON ar.item_id = ci.item_id
        WHERE ar.request_id = %s
    """, (request_id,))

    item = cursor.fetchone()

    cursor.close()
    conn.close()

    if not item:
        return "Access request not found.", 404

    return render_template("review_item.html", item=item)


# ==========================================================
# ==========================================================
# ==========================================================
# ==========================================================
# Main Program
# ==========================================================

if __name__ == "__main__":

    app.run(debug=True)