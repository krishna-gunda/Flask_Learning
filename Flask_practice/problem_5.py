'''Problem 4 — Different Routes

Create a Flask application with these routes:

/
/home
/contact

Expected output:

/          → Welcome Home
/home      → This is the Home Page
/contact   → Contact Us

Goal: Practice handling multiple URLs.'''

from flask import Flask

app=Flask(__name__)

@app.route("/")
def home():
    return "Welcome Home"
@app.route("/home")
def home_coming():
    return "This is Home Page"

@app.route("/contact")
def contact():
    return "Contact Us"

app.run()