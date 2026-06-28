# Flask Fundamentals
--------------------------------------------------------
## What is Flask?

Flask is a lightweight web framework written in Python.

A framework provides a collection of tools that make it
easier to build websites.

Instead of writing an entire website from scratch,
Flask provides:

• Routing
• Templates
• Forms
• Sessions
• Error handling

--------------------------------------------------------
## Think of Flask like this...
Restaurant Example
Customer
↓
Waiter
↓
Kitchen
↓
Meal
↓
Customer

Flask is the waiter.
It receives requests from users.
It takes those requests to Python.

Python may retrieve data from MySQL.

Flask then returns the completed webpage.

--------------------------------------------------------
## In our Assignment
Browser
↓
Flask
↓
MySQL
↓
HTML
↓
Browser
--------------------------------------------------------
## Code Example
@app.route("/")

def home():

    return render_template("home.html")

--------------------------------------------------------
## What did we learn?
✓ Flask is the Controller.
✓ Flask receives requests.
✓ Flask decides which function runs.
✓ Flask returns webpages.


------------------------------------------------------------
## Key Takeaways
✔ Flask is a Python web framework.
✔ Flask follows the MVC architecture.
✔ Flask controls application flow.
✔ Flask connects HTML with Python.

------------------------------------------------------------
## Interview Question
Q:
What is Flask?

Answer:
Flask is a lightweight Python web framework that
allows developers to build dynamic web applications.

It acts as the Controller in the MVC architecture,
receiving requests from users, interacting with the
database when required, and returning HTML pages
to the browser.

------------------------------------------------------------
## Related Files
app.py
templates/
routes/

------------------------------------------------------------