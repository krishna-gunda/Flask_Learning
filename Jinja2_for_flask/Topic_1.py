from flask import Flask,render_template

app=Flask(__name__)
@app.route('/')
def home():
    return "<h1>Welcome to home<h1>"
@app.route('/<name>')
def krishna(name):
    return render_template("home.html",name=name) # this will go to the home.html and then execute the html file

if __name__=='__main__':
    app.run(debug=True)