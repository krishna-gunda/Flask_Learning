### 11. Practice Question
'''Create a route `/greet` that passes a variable `city = "Bangalore"` to a template, 
and print `"Welcome from Bangalore"` using `{{ }}`, with a `{# #}` 
comment above it explaining what the line does.'''

from flask import Flask , render_template

app=Flask(__name__)
@app.route('/')
def home():
    return "<h1>Welcome Home<h1>"
@app.route('/greet')
def greet():
    city='Bangalore'
    return render_template("greet.html",city=city)

if __name__=='__main__':
    app.run(debug=True)
