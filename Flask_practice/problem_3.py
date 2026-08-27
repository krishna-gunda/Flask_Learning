'''Problem 2 — About Page

Create a Flask application with two routes:

/

and

/about

Expected behavior:

/ → Welcome to My Website
/about → This is the About Page

Goal: Practice creating multiple routes.'''


from flask import Flask

app = Flask(__name__)

@app.route("/")
# This creates the home (root) URL of our website.
# When the user opens "/", Flask will execute the home() function.
def home():
    # This message will be displayed on the webpage when the user visits "/".
    return "Welcome to My Website"


@app.route("/about")
# This creates the "/about" URL.
# When the user opens "/about", Flask will execute the about() function.
def about():
    # This message will be displayed on the webpage when the user visits "/about".
    return "This is the About Page"


if __name__ == "__main__":
    # This condition checks whether we are running this Python file directly.
    # If we run the file directly, the Flask application will start.
    app.run(debug=True)
    # debug=True automatically reloads the server when we make changes to our code.
    # It also shows detailed error messages when an error occurs.