# Import Flask to create our web application
# Import render_template to load an HTML file from the templates folder
from flask import Flask, render_template


# Create the Flask application
app = Flask(__name__)


# When the user opens the home page "/"
# Flask will run the home() function
@app.route("/")
def home():

    # Load and display the index.html file
    # Flask automatically looks for index.html inside the "templates" folder
    return render_template("index.html")


# This checks whether we are running this file directly
# If we are, start the Flask application
if __name__ == "__main__":
    app.run(debug=True)