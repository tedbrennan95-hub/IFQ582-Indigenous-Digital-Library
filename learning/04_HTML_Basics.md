# HTML Basics

------------------------------------------------------------
## What is HTML?
HTML stands for **HyperText Markup Language**.

It is the standard language used to create webpages.

HTML provides the structure of a webpage by defining
elements such as headings, paragraphs, images, links,
tables and forms.

Think of HTML as the **skeleton** of a website.

------------------------------------------------------------
## How HTML fits into Flask

In a Flask application, HTML pages are stored inside the
`templates` folder.

When a user requests a webpage:

Browser
↓
Flask Route
↓
render_template()
↓
HTML Template
↓
Browser displays webpage

Flask combines Python with HTML to generate dynamic
webpages.

------------------------------------------------------------

## Basic HTML Structure

```html
<!DOCTYPE html>

<html>

<head>

    <title>My Website</title>

</head>

<body>

    <h1>Welcome</h1>

    <p>Hello World!</p>

</body>

</html>
```

Every webpage begins with this basic structure.

------------------------------------------------------------
## Common HTML Elements

| Tag | Purpose |
|------|----------|
| `<html>` | Root element of the webpage |
| `<head>` | Stores page information |
| `<title>` | Browser tab title |
| `<body>` | Visible webpage content |
| `<h1>` | Main heading |
| `<p>` | Paragraph |
| `<a>` | Hyperlink |
| `<img>` | Display an image |
| `<table>` | Create a table |
| `<form>` | User input form |

------------------------------------------------------------
## Our Assignment Example
Our first webpage is:

home.html

```html
<h1>
Welcome to the Indigenous Digital Library
</h1>

<p>
Flask has been successfully configured.
</p>
```

Flask loads this page using:

```python
return render_template("home.html")
```
------------------------------------------------------------
## Key Takeaways
✔ HTML creates the structure of a webpage.
✔ HTML files are stored inside the **templates** folder.
✔ Flask uses **render_template()** to display HTML pages.
✔ HTML works together with CSS and JavaScript.

------------------------------------------------------------
## Interview Question

**Question**
What is HTML?

**Answer**
HTML (HyperText Markup Language) is the standard
language used to create webpages.

It provides the structure and content of a webpage and is
rendered by the user's web browser.

------------------------------------------------------------
## Things Ted Should Remember
Remember...

HTML only defines the webpage structure.
It does **NOT** perform calculations.
It does **NOT** connect to the database.
Python (Flask) performs the processing.
HTML displays the results.

------------------------------------------------------------
## Related Files
templates/home.html
templates/base.html
app.py

------------------------------------------------------------
## Progress Tracker
☑ Learned
☑ Built
☑ Tested
☑ Explained
☑ Documented

------------------------------------------------------------