# Dynamic Routes

from flask import Flask
app=Flask(__name__)
@app.route('/')
def home():
    return "<h1>Welcome Home<h1>"
@app.route('/<name>')
def about(name):
    return f"Welcome {name}"

if __name__=='__main__':
    app.run(debug=True)
