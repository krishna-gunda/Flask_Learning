# lets see the basic programof the flask

# we need to install the flask by creating the virtual env
# use this command to create virtual env
# python -m venv venv
# and the cd venv/scripts/
# and activate
# and the come back to currrent directory by using the cd.. twice
# and then install the pip install the flask
# 
from flask import Flask

app=Flask(__name__)  # creating the object app for the Flask class
@app.route("/")  # creating the default route to the app

def home():              # this is the function that will execute when the server starts
    return "welcome krishna's home "  # and it will return this string in the browser

# 
if __name__ == "__main__":
    app.run(debug=True)