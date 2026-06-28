# ==========================================================
# Indigenous Digital Library
#
# File: database.py
#
# PURPOSE
# -------
# This file is responsible for creating the connection
# between the Flask application and the MySQL database.
#
# Separating database code from app.py keeps the project
# organised and follows the MVC architecture.
#
# ==========================================================

import mysql.connector


def get_database_connection():
    """
    Creates and returns a connection to the MySQL database.
    """

    connection = mysql.connector.connect(

        host="localhost",
        user="root",
        password="Carltonblues50!",
        database="ifq582_assignment"

    )

    return connection

# ==========================================================
# ==========================================================
# ==========================================================
# ==========================================================
# Retrieve All Collection Items
# ==========================================================
#
# This function retrieves every collection item stored
# inside the MySQL database.
#
# The data returned by this function will later be sent
# to a Flask HTML template where it can be displayed
# dynamically.
#
# This forms part of the Model layer in MVC.
#
# Browser
#     │
#     ▼
# Flask Route
#     │
#     ▼
# database.py  ← This function
#     │
#     ▼
# MySQL
#
# ==========================================================

def get_all_collection_items():

    # Create a connection to MySQL
    connection = get_database_connection()

    # Create a cursor that returns each row as a dictionary
    # instead of a tuple.
    cursor = connection.cursor(dictionary=True)

    # SQL query
    query = """
        SELECT *
        FROM collection_items
        ORDER BY title;
    """

    # Execute query
    cursor.execute(query)

    # Retrieve all records
    items = cursor.fetchall()

    # Close database objects
    cursor.close()
    connection.close()

    # Return the list of collection items
    return items

# ==========================================================
# ==========================================================
# ==========================================================
# ==========================================================

# ==========================================================
# Retrieve One Collection Item
# ==========================================================
#
# This function retrieves a single collection item using
# its item_id primary key.
#
# This supports the Item Details page.
#
# Example:
# /collection/3
#
# ==========================================================

def get_collection_item_by_id(item_id):

    connection = get_database_connection()

    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT *
        FROM collection_items
        WHERE item_id = %s;
    """

    cursor.execute(query, (item_id,))

    item = cursor.fetchone()

    cursor.close()
    connection.close()

    return item

# ==========================================================
# Search Collection Items
# ==========================================================
#
# This function searches collection items by title or
# description.
#
# It uses SQL LIKE to find partial matches.
#
# Example:
# Searching for "basket" will match:
# "Woven Basket Collection"
#
# The % symbols mean:
# match anything before or after the search term.
#
# ==========================================================

def search_collection_items(search_term):

    connection = get_database_connection()

    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT *
        FROM collection_items
        WHERE title LIKE %s
           OR description LIKE %s
        ORDER BY title;
    """

    search_pattern = f"%{search_term}%"

    cursor.execute(query, (search_pattern, search_pattern))

    items = cursor.fetchall()

    cursor.close()
    connection.close()

    return items