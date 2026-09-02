
# Import Flask to create the web application
# render_template is used to open HTML files from the templates folder
from flask import Flask, render_template


# Create the Flask application
app = Flask(__name__)


# This route runs when the user visits the home page "/"
@app.route('/')
def website():

    # Return a simple HTML heading to the browser
    return "<h1>Welcome to my website</h1>"


# <name> is a dynamic part of the URL
# Example: /Krishna → name will be "Krishna"
@app.route('/<name>')
def home(name):

    # Send the name to the home.html template
    # We can use this value inside HTML using {{ name }}
    return render_template("home.html", name=name)


# <int:age> means the age entered in the URL must be a number
# Example: /22 → age will be 22
@app.route('/<int:age>')
def age(age):

    # Send the age to the Topic_2.html template
    # We can use this value inside HTML using {{ age }}
    return render_template("Topic_2.html", age=age)


# Start the Flask application
# This code runs only when we directly run this Python file
if __name__ == '__main__':
    app.run(debug=True)

