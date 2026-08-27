'''Problem 3 — Student Information

Create a route:

/student

When the user visits it, return information about a student.

For example:

Name: Krishna
Course: Artificial Intelligence and Machine Learning
Year: 4th Year

You should store these values in variables and then return them.

Goal: Practice Python variables inside Flask routes.'''


from flask import Flask

app=Flask(__name__)
@app.route("/")
def home():
    return "This is home page"

@app.route("/student")

def student_details():
    Name="krishna"
    college="Joginpally B.R Engineering College"
    marks=80
    return f'Name={Name}<br>college name is {college}<br> marks {str(marks)}' # <br> is an HTML tag that means line break — it moves the next content to a new line in the browser.

app.run()  # directly running when ever the file executes


# Flask routes must return a valid response that can be sent to the browser.
# We commonly return a string, HTML, or JSON/dictionary.
# We should not return a raw integer like 80 directly from a route.