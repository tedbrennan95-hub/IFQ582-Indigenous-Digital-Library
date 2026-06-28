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

from flask import Flask, render_template, url_for, request

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
# Home Page Route
# ----------------------------------------------------------

@app.route("/")
def home():

    return render_template("home.html")


# ----------------------------------------------------------
# Database Test Route
# ----------------------------------------------------------
#
# This route confirms that Flask can connect to the MySQL
# database.
#
# ----------------------------------------------------------

@app.route("/database-test")
def database_test():

    connection = get_database_connection()

    if connection.is_connected():

        connection.close()

        return "<h2>✅ Successfully connected to the Indigenous Library database.</h2>"

    return "<h2>❌ Database connection failed.</h2>"

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
def collection_detail(item_id):

    item = get_collection_item_by_id(item_id)

    if item is None:
        return "<h2>Collection item not found.</h2>", 404

    return render_template("collection_detail.html", item=item)

# ==========================================================
# ==========================================================
# ==========================================================
# ==========================================================
# Main Program
# ==========================================================

if __name__ == "__main__":

    app.run(debug=True)