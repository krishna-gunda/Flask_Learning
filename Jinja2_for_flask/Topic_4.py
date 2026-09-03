from flask import Flask , render_template
app=Flask(__name__)
@app.route('/')
def home():
    return "<h1>Welcome Home<h1>"
@app.route('/profile')
def profile():
    students={"name":"Krishna",
              "age":22,
              "marks":85,
              "address":{"city":"Hyderabad",
              "state":"Telangana"},
              "skills": ["Python","Flask","Machine Learning"]
              }
    return render_template("profile.html",student=students)

if __name__=='__main__':
    app.run(debug=True)