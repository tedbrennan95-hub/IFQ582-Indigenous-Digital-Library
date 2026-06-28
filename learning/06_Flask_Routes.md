# Flask Routes
---
## What is a Route?
A **Route** connects a web address (URL) entered by the user
to a Python function inside the Flask application.

When a user visits a webpage, Flask checks the requested URL
and determines which function should be executed.

Every webpage in a Flask application requires a route.

---
## Think of a Route like this...

Imagine visiting a shopping centre.

You want to visit a particular store.

The directory tells you exactly where to go.

A Flask Route works in the same way.

It tells Flask which Python function should be executed
when a specific URL is requested.

---
## Request Flow

User enters URL
↓
http://127.0.0.1:5000/
↓
Flask receives request
↓
Route is matched
↓
Python function executes
↓
HTML page is loaded
↓
Browser displays webpage

---

## Basic Route Example

```python
@app.route("/")
def home():

    return render_template("home.html")
```

Explanation:

`@app.route("/")`

Tells Flask to respond when the user visits the website's
home page.

`def home():`

Defines the Python function that will execute.

`render_template("home.html")`

Loads the HTML page stored inside the **templates**
folder and sends it back to the browser.

---
## Multiple Routes

A Flask application normally contains many routes.

Example

```python
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/collections")
def collections():
    return render_template("collections.html")


@app.route("/login")
def login():
    return render_template("login.html")
```

Each route represents a different page of the website.

---

## Routes in Our Assignment
For the Indigenous Digital Library we expect to build
routes such as:

| Route             | Purpose                               |
| ----------------- | ------------------------------------- |
| `/`               | Home Page                             |
| `/collections`    | Display collection items              |
| `/item/<id>`      | Display an individual collection item |
| `/request-access` | Submit an access request              |
| `/review`         | Community review page                 |
| `/login`          | User login                            |

As our application grows, each page will have its own route.

---
## How Routes fit into MVC

Browser
↓
Flask Route (Controller)
↓
Python Function
↓
MySQL Database (Model)
↓
HTML Template (View)
↓
Browser

Routes are part of the **Controller** because they control
what happens when the user requests a webpage.

---

## Common Route Examples

Home Page

```python
@app.route("/")
```

About Page
```python
@app.route("/about")
```

Login Page
```python
@app.route("/login")
```

Item Details
```python
@app.route("/item/<item_id>")
```

The value inside `< >` is called a **route parameter**.

It allows Flask to pass information into the function.

---

## Key Takeaways

✔ Every webpage requires a Route.
✔ A Route connects a URL to a Python function.
✔ Routes belong to the Flask Controller.
✔ Routes often return HTML using `render_template()`.
✔ Routes can receive information through URL parameters.

---
## Interview Question
**Question**
What is a Flask Route?

**Answer**
A Flask Route maps a URL to a Python function.

When a user visits a webpage, Flask matches the requested
URL to the appropriate route, executes the corresponding
function, and returns the generated HTML page to the browser.

---
## Things Ted Should Remember

Remember...
The browser never runs Python directly.
The browser requests a URL.
Flask receives the request.
Flask chooses the correct Route.
The Route runs a Python function.
The function returns an HTML page.

---
## Related Files
app.py
templates/
base.html

---
## Progress Tracker
☑ Learned
☑ Built
☑ Tested
☑ Explained
☑ Documented

------------------------------------------------------------

Connection to the Government Analytics Portal

The Government Analytics Portal contains many Flask routes.

Examples include:

@app.route("/")
@app.route("/claims")
@app.route("/telephony")
@app.route("/population")
@app.route("/admin")

Although the pages perform different tasks, every route
follows the same pattern:

1. User requests a URL.
2. Flask matches the route.
3. Python executes.
4. Data may be retrieved from the database.
5. HTML is returned to the browser.

This assignment uses exactly the same concept, but on a
smaller scale.

------------------------------------------------------------