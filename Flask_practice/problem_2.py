'''Problem 1 — Hello Flask

Create a Flask application that:

Creates a Flask application object.
Has a route /
When a user visits /, it should return:
Hello, Welcome to Flask!'''

# learn the flask by building the applications

from flask import Flask

app=Flask(__name__)

@app.route("/")
def home():
    return "Hello, Welcome to flask"

if __name__=="__main__":
    app.run()