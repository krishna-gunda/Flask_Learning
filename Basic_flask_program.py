# ============================================================
# BASIC FLASK PROGRAM
# ============================================================

# Step 1: Create a virtual environment
# Command:
# python -m venv venv

# Step 2: Activate the virtual environment
# Windows:
# venv\Scripts\activate

# Step 3: Install Flask inside the virtual environment
# Command:
# pip install flask


# ============================================================
# IMPORT FLASK
# ============================================================

from flask import Flask


# ============================================================
# CREATE THE FLASK APPLICATION
# ============================================================

# Flask is a class provided by the Flask framework.
# Flask(__name__) creates a Flask application object.
#
# __name__ tells Flask where the current Python file is located.
# Flask uses this information to find resources such as
# templates and static files.
#
# 'app' is the object through which we configure our Flask
# application.

app = Flask(__name__)


# ============================================================
# CREATE A ROUTE
# ============================================================

# @app.route("/") creates the root (default) URL of our website.
#
# When a user visits:
#
# http://127.0.0.1:5000/
#
# Flask will execute the function written immediately below
# this decorator.

@app.route("/")
def home():

    # This string is returned to the browser as the response.
    return "Welcome to Krishna's Home"


# ============================================================
# START THE FLASK APPLICATION
# ============================================================

# __name__ is a special Python variable.
#
# When this file is executed directly:
#
#     python app.py
#
# Python sets:
#
#     __name__ = "__main__"
#
# Therefore, the condition below becomes True and Flask starts
# the development server.
#
# If this file is imported into another Python file,
# __name__ will NOT be "__main__".
#
# In that situation, app.run() will not execute automatically.
#
# This prevents the Flask server from starting unexpectedly
# when the file is imported.

if __name__ == "__main__":

    # Start Flask's development server.
    #
    # debug=True enables debug mode:
    # - Automatically reloads the server when code changes.
    # - Shows detailed error messages during development.
    #
    # NOTE: debug=True should normally be used only during
    # development, not in production.

    app.run(debug=True)