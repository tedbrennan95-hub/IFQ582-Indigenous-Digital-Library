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

from flask import Flask, render_template

# Import database functions from the Model layer
from models.database import get_database_connection
from models.database import get_all_collection_items


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


# ----------------------------------------------------------
# Browse Collection Route
# ----------------------------------------------------------
#
# This route displays all collection items stored in MySQL.
#
# MVC flow:
#
# Browser requests /collections
#        ↓
# Flask runs this route
#        ↓
# Route calls get_all_collection_items()
#        ↓
# database.py retrieves records from MySQL
#        ↓
# Records are passed to collections.html
#        ↓
# Browser displays the collection page
#
# ----------------------------------------------------------

@app.route("/collections")
def collections():

    # Retrieve all collection items from the database
    items = get_all_collection_items()

    # Send the items to the HTML template
    return render_template("collections.html", items=items)


# ==========================================================
# Main Program
# ==========================================================

if __name__ == "__main__":

    app.run(debug=True)