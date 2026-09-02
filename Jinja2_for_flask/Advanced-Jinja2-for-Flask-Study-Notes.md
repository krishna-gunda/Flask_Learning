# Advanced Jinja2 for Flask — Complete Study Notes

**Made for:** Krishna | Beginner → Advanced | Goal: Flask backend + AI/ML web apps

**How to use this document:** Read top to bottom in order — later parts assume earlier ones. Every code block is labeled `# Python`, `# app.py (Flask)`, or `<!-- HTML/Jinja2 -->` so you always know which language you're looking at.

---

## Table of Contents

1. Fundamentals Review
2. Working with Python Data
3. Conditional Statements
4. Loops
5. Loop Filtering
6. Filters
7. select / selectattr / reject / rejectattr
8. Template Inheritance ⭐⭐⭐
9. include
10. macro
11. Importing Macros
12. set
13. Expressions and Operators
14. Tests
15. url_for()
16. request object
17. session
18. Flash Messages
19. Whitespace Control
20. Autoescaping & Security ⭐⭐⭐
21. Custom Filters
22. Custom Global Functions
23. Context Processors
24. Calling Python Methods
25. Debugging
26. Project Structure
27. Complete Mini Project
28. Cheat Sheet + Interview Prep

---

# PART 1 — Jinja2 Fundamentals Review
**Level: Beginner (quick refresher)**

### 1. Topic Name
Jinja2 basics: `{{ }}`, `{% %}`, `{# #}`

### 2. What is it?
Jinja2 is the **template engine** Flask uses to turn Python data into HTML pages. A template engine takes a text file (your HTML) with special placeholders in it, fills those placeholders with real data, and outputs plain HTML that the browser can show.

Think of it like a **mail-merge letter**: the template is `"Dear {{ name }}, your order {{ order_id }} has shipped."` and Jinja2 fills in the blanks for each customer.

### 3. Why do we need it?
Without a template engine, you'd have to build HTML strings by hand in Python using string concatenation (`"<h1>" + name + "</h1>"`), which is messy, error-prone, and mixes Python logic with HTML markup. Jinja2 lets you write clean HTML files with small, readable placeholders, and keeps your Python code focused on logic, not string-building.

### 4. Syntax — the three delimiter types

| Delimiter | Purpose | Produces output? |
|---|---|---|
| `{{ ... }}` | **Expression** — print a value | Yes, becomes visible text |
| `{% ... %}` | **Statement** — logic like if/for/set | No, controls the template but prints nothing itself |
| `{# ... #}` | **Comment** — notes for developers | No, removed entirely, invisible even in "View Source" |

### 5. Simple Example
```jinja2
{{ 2 + 2 }}          <!-- prints: 4 -->
{% if 2 + 2 == 4 %}  <!-- runs logic, prints nothing by itself -->
    Math works!
{% endif %}
{# This comment never appears in the browser #}
```

### 6. Flask Example
```python
# app.py
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def home():
    name = "Krishna"
    return render_template("home.html", name=name)
```
```jinja2
<!-- templates/home.html -->
<h1>Hello, {{ name }}!</h1>
{# TODO: add a welcome image later #}
```

### 7. Line-by-line Explanation
- `render_template("home.html", name=name)` — this function looks inside your `templates/` folder for `home.html`, reads it as text, and asks Jinja2 to process it.
- `name=name` is a **keyword argument**: the left `name` is the variable name Jinja2 will see *inside the HTML file*, and the right `name` is the Python variable whose value gets sent over. They don't have to match — `render_template("home.html", username=name)` would make it available as `{{ username }}` in HTML instead.
- Internally, Flask hands Jinja2 a **dictionary of context data**, roughly `{"name": "Krishna"}`. Jinja2 stores this as the template's "context."
- When Jinja2 sees `{{ name }}` in the HTML, it looks up `"name"` in that context dictionary and substitutes the value as text.
- The final output is a plain HTML string — Jinja2's job is done, and Flask sends that string back to the browser as the HTTP response body.

### 8. Expected Output
```
Hello, Krishna!
```
(The comment is completely absent from the page source.)

### 9. Real-world Use Case
Every dynamic page in a Flask app — dashboards, product pages, user profiles — uses `{{ }}` to inject data and `{% %}` to control what's shown, in what order, and how many times.

### 10. Common Mistakes
| Mistake | Problem | Fix |
|---|---|---|
| `{ name }` (single braces) | Jinja2 ignores it; prints literally `{ name }` | Use double braces `{{ name }}` |
| Using `{{ }}` for an `if` | `{{ if x }}` is invalid — `{{ }}` is only for values | Use `{% if x %}` |
| Forgetting `render_template` and just returning a string with `{{ }}` in it | Flask won't process Jinja2 syntax on a plain string | Always route HTML through `render_template()` |

### 11. Practice Question
Create a route `/greet` that passes a variable `city = "Hyderabad"` to a template, and print `"Welcome from Hyderabad!"` using `{{ }}`, with a `{# #}` comment above it explaining what the line does.

---
# PART 2 — Working with Python Data
**Level: Beginner–Intermediate**

### 1. Topic Name
Accessing Python data types (strings, lists, tuples, dicts, nested structures) from Jinja2

### 2. What is it?
When you pass a Python variable into `render_template()`, Jinja2 receives the **actual Python object** — not a text copy. So a list is still a list, a dict is still a dict, and Jinja2 has special syntax to reach into each type.

### 3. Why do we need it?
Real apps rarely pass a single string. You'll pass lists of students, dictionaries of user profiles, and nested combinations of both (a list of dictionaries is *the* most common shape in real apps — think "rows from a database"). You need to know exactly how to pull data out of each shape.

### 4. Syntax
```jinja2
{{ name }}                     <!-- string -->
{{ students[0] }}               <!-- list index -->
{{ student["name"] }}           <!-- dict, bracket access -->
{{ student.name }}               <!-- dict, dot access -->
{{ student.address.city }}       <!-- nested dict -->
{{ students[0]["name"] }}        <!-- list of dicts -->
```

### 5. Simple Example
```python
name = "Krishna"
students = ["Krishna", "Rahul", "Anil"]
student = {"name": "Krishna", "age": 22, "marks": 85}
```
```jinja2
{{ name }}              <!-- Krishna -->
{{ students[1] }}        <!-- Rahul -->
{{ student["age"] }}     <!-- 22 -->
{{ student.marks }}      <!-- 85 -->
```

### 6. Flask Example
```python
# app.py
@app.route("/profile")
def profile():
    student = {
        "name": "Krishna",
        "age": 22,
        "marks": 85,
        "address": {"city": "Hyderabad", "state": "Telangana"},
        "skills": ["Python", "Flask", "ML"]
    }
    return render_template("profile.html", student=student)
```
```jinja2
<!-- templates/profile.html -->
<h2>{{ student.name }}</h2>
<p>Age: {{ student["age"] }}</p>
<p>City: {{ student.address.city }}</p>
<p>First skill: {{ student.skills[0] }}</p>
```

### 7. Line-by-line Explanation
- `student.address.city` — Jinja2 walks the dictionary one level at a time: first it looks up `"address"` inside `student` (getting another dict), then looks up `"city"` inside *that* dict.
- `student.skills[0]` — `.skills` accesses the list stored under the `"skills"` key; `[0]` then indexes into that list like any Python sequence.
- **Bracket vs dot — the real difference:** `student["name"]` performs a strict dictionary key lookup only. `student.name` is smarter — Jinja2 first tries `student["name"]` (dict lookup), and if that fails, it tries `getattr(student, "name")` (attribute lookup, useful for objects/class instances, not just dicts). So dot notation works for *both* dicts and objects, while bracket notation is dict-only (but bracket notation is required when your key isn't a valid Python identifier, e.g. `student["first-name"]` — dots can't contain a hyphen).

### 8. Expected Output
```
Krishna
Age: 22
City: Hyderabad
First skill: Python
```

### 9. Real-world Use Case
Any time you fetch a row from a database (SQLAlchemy returns objects, raw SQL/Mongo returns dicts) and want to display its fields — dot notation handles both cases uniformly, which is exactly why most Flask templates prefer `student.name` over `student["name"]`.

### 10. Common Mistakes
| Mistake | Problem | Fix |
|---|---|---|
| `{{ student.marks[0] }}` when `marks` is an int, not a list | `TypeError`/`UndefinedError` | Check the real shape of your data before indexing |
| Using `student.first-name` | Dot notation can't contain hyphens; Jinja2 misparses it | Use `student["first-name"]` |
| Assuming `student.name` always works for a plain dict passed from JSON with weird keys | Works for normal string keys, but fails if the key isn't found by either method | Use `.get()`-style defaults — covered in Part 6 (`default` filter) |

### 11. Practice Question
Given `student = {"name": "Anil", "marks": {"maths": 90, "science": 85}}`, write a template line that prints Anil's science marks using dot notation, and another line using bracket notation.

---
# PART 3 — Conditional Statements
**Level: Beginner–Intermediate**

### 1. Topic Name
`if`, `elif`, `else` in Jinja2

### 2. What is it?
Jinja2's `if` lets you show or hide parts of HTML depending on a condition — exactly like Python's `if`, but written with `{% %}` tags and a required closing `{% endif %}`.

### 3. Why do we need it?
HTML has no built-in logic. Without `{% if %}`, you couldn't show "Welcome back!" only to logged-in users, or grade labels only when marks exist — you'd need a separate hand-written HTML file for every possible scenario.

### 4. Syntax
```jinja2
{% if condition %}
    ...
{% elif other_condition %}
    ...
{% else %}
    ...
{% endif %}
```

### 5. Simple Example
```jinja2
{% if marks >= 90 %}
    A Grade
{% elif marks >= 75 %}
    B Grade
{% else %}
    C Grade
{% endif %}
```

### 6. Flask Example
```python
# app.py
@app.route("/result")
def result():
    marks = 82
    return render_template("result.html", marks=marks)
```
```jinja2
<!-- templates/result.html -->
<p>Your marks: {{ marks }}</p>
{% if marks >= 90 %}
    <p>Grade: A</p>
{% elif marks >= 75 %}
    <p>Grade: B</p>
{% elif marks >= 50 %}
    <p>Grade: C</p>
{% else %}
    <p>Grade: Fail</p>
{% endif %}
```

### 7. Line-by-line Explanation
- `{% if marks >= 90 %}` — Jinja2 evaluates the Python-like expression `marks >= 90` against the value in the context. This is real comparison logic running at render time, not just text.
- Every `{% if %}` **must** be paired with an `{% endif %}` because Jinja2's tags don't use indentation (unlike Python) to know where a block ends — indentation in HTML is just whitespace, so Jinja2 needs an explicit closing tag to know where your conditional block stops.
- `{% elif %}` works exactly like Python's `elif` — only the first matching branch runs; later branches are skipped even if they'd also be true.

### 8. Expected Output
```
Your marks: 82
Grade: B
```

### 9. Real-world Use Case
Showing/hiding admin buttons based on user role, showing "Out of Stock" vs "Add to Cart", displaying different messages for pass/fail results.

### 10. Common Mistakes
| Mistake | Problem | Fix |
|---|---|---|
| Forgetting `{% endif %}` | `TemplateSyntaxError: Unexpected end of template` | Always close every `{% if %}` |
| Writing `{% if marks => 90 %}` | `=>` is not valid Jinja2/Python syntax | Use `>=` |
| Using Python-only functions like `len()` incorrectly assuming Jinja2 doesn't support it | Jinja2 *does* support `len()`, but many built-ins (e.g. `print()`) don't work — Jinja2 only exposes a safe subset of Python | Check Jinja2 docs, prefer filters like `|length` |

**How Jinja2 conditions differ from Python:** Jinja2 conditions run inside a *sandboxed* environment — you can use comparisons, `and`/`or`/`not`, `in`, filters, and tests, but you cannot run arbitrary statements (no `import`, no defining functions, no multi-line assignments) inside `{% if %}`. This is intentional — templates should stay presentation-only.

### 11. Practice Question
Given `age = 17`, write an if/elif/else block that prints `"Minor"` if under 18, `"Adult"` if 18–59, and `"Senior"` if 60+.

---
# PART 4 — Loops
**Level: Intermediate — Very Important ⭐**

### 1. Topic Name
`{% for %}` loops and the `loop` variable

### 2. What is it?
`{% for %}` repeats a block of HTML once for every item in a list, dict, or other iterable — the template equivalent of Python's `for item in items:`.

### 3. Why do we need it?
You almost never know in advance how many students, products, or comments you'll have. Loops let one small HTML block automatically expand to fit however much data you pass in.

### 4. Syntax
```jinja2
{% for item in items %}
    {{ item }}
{% endfor %}
```

### 5. Simple Example
```python
students = ["Krishna", "Rahul", "Anil"]
```
```jinja2
<ul>
{% for student in students %}
    <li>{{ student }}</li>
{% endfor %}
</ul>
```

### 6. Flask Example — list of dicts + nested loop
```python
# app.py
@app.route("/students")
def students_page():
    students = [
        {"name": "Krishna", "marks": 85, "subjects": ["Python", "ML"]},
        {"name": "Rahul", "marks": 65, "subjects": ["Java"]},
        {"name": "Anil", "marks": 92, "subjects": ["Python", "DSA"]},
    ]
    return render_template("students.html", students=students)
```
```jinja2
<!-- templates/students.html -->
<table>
{% for student in students %}
    <tr>
        <td>{{ loop.index }}</td>
        <td>{{ student.name }}</td>
        <td>{{ student.marks }}</td>
        <td>
            {% for subject in student.subjects %}
                {{ subject }}{% if not loop.last %}, {% endif %}
            {% endfor %}
        </td>
    </tr>
{% endfor %}
</table>
```

### 7. Line-by-line Explanation
- `{% for student in students %}` — on each pass, Jinja2 takes the next element from `students` and binds it to the local name `student`, valid only inside this loop block.
- The inner `{% for subject in student.subjects %}` is a **nested loop**: for *each* outer `student`, Jinja2 runs a full inner loop over that student's own `subjects` list — this is exactly like nested `for` loops in Python.
- `{% if not loop.last %}, {% endif %}` prints a comma after every subject except the final one, so you get `"Python, ML"` instead of `"Python, ML, "`.

**The `loop` variable — available automatically inside any `{% for %}`:**

| Variable | Meaning | Example (3 items) |
|---|---|---|
| `loop.index` | Current iteration, 1-based | 1, 2, 3 |
| `loop.index0` | Current iteration, 0-based | 0, 1, 2 |
| `loop.revindex` | Iterations remaining, 1-based | 3, 2, 1 |
| `loop.revindex0` | Iterations remaining, 0-based | 2, 1, 0 |
| `loop.first` | `True` on the first iteration only | True, False, False |
| `loop.last` | `True` on the last iteration only | False, False, True |
| `loop.length` | Total number of items in the loop | 3, 3, 3 |

### 8. Expected Output
```
1   Krishna   85   Python, ML
2   Rahul     65   Java
3   Anil      92   Python, DSA
```

### 9. Real-world Use Case
Rendering a table of database rows, a numbered comment thread (`loop.index`), highlighting the first/last row differently with CSS (`loop.first`/`loop.last`), or a progress indicator (`loop.index / loop.length`).

### 10. Common Mistakes
| Mistake | Problem | Fix |
|---|---|---|
| Forgetting `{% endfor %}` | `TemplateSyntaxError` | Always close loops |
| Using `loop.index` expecting 0-based | Off-by-one bugs in labels | Remember `.index` is 1-based, `.index0` is 0-based |
| Trying to access `loop` inside a macro or outside a `for` | `UndefinedError` | `loop` only exists inside an active `{% for %}` block |

### 11. Practice Question
Given a list of 5 product names, print a numbered list where the **first** item has the label "(NEW)" next to it and the **last** item has "(LAST ONE)" next to it, using `loop.first` and `loop.last`.

---
# PART 5 — Loop Conditions, Filtering, and `else`
**Level: Intermediate**

### 1. Topic Name
Inline loop filtering (`for ... if ...`) and the loop's `{% else %}`

### 2. What is it?
Jinja2 lets you attach an `if` directly to a `for` line to skip items that don't match — and lets you attach an `{% else %}` to the loop itself, which runs only if the loop had **zero** items to iterate over.

### 3. Why do we need it?
Real lists are often empty (no search results, no orders yet) or need filtering (only show passing students). Doing this in the template avoids writing near-duplicate Python code just to pre-filter a list, and `{% else %}` avoids a blank, confusing page when there's nothing to show.

### 4. Syntax
```jinja2
{% for student in students if student.marks >= 70 %}
    {{ student.name }}
{% else %}
    No students found
{% endfor %}
```

### 5. Simple Example
```python
numbers = [1, 2, 3, 4, 5, 6]
```
```jinja2
{% for n in numbers if n % 2 == 0 %}
    {{ n }}    <!-- prints only 2, 4, 6 -->
{% endfor %}
```

### 6. Flask Example
```python
# app.py
@app.route("/passed")
def passed():
    students = [
        {"name": "Krishna", "marks": 85},
        {"name": "Rahul", "marks": 40},
    ]
    return render_template("passed.html", students=students)
```
```jinja2
<!-- templates/passed.html -->
<h3>Passed Students</h3>
<ul>
{% for student in students if student.marks >= 50 %}
    <li>{{ student.name }} — {{ student.marks }}</li>
{% else %}
    <li>No students have passed yet.</li>
{% endfor %}
</ul>
```

### 7. Line-by-line Explanation
- `{% for student in students if student.marks >= 50 %}` — Jinja2 checks the condition for *every* item; items that fail it are silently skipped, they never enter the loop body at all (this is different from wrapping the whole body in a separate `{% if %}` — with inline filtering, `loop.index`/`loop.first`/`loop.last` are recalculated based only on the *filtered* items).
- `{% else %}` here belongs to the `for`, not to any `if` — it fires only when the loop body executed **zero times total** (either because `students` was empty, or because the `if` condition filtered out everything).

### 8. Expected Output
```
Passed Students
- Krishna — 85
```
(Rahul is skipped since 40 < 50; if *both* had failed, you'd see "No students have passed yet.")

### 9. Real-world Use Case
Search results pages ("No results found for your search"), filtered dashboards (only show overdue tasks), admin panels (only show active users) — all without touching the Python route logic.

### 10. Common Mistakes
| Mistake | Problem | Fix |
|---|---|---|
| Expecting `{% else %}` to run when the `if` filters out *some but not all* items | It only runs when the loop produced **zero** iterations | If you need a message for "some items were filtered," count them in Python instead |
| Complex filtering logic inline (`if a and b or c and not d`) | Hard to read, mixes business logic into HTML | Pre-filter the list in Python and pass only the filtered list to the template |

### 11. Practice Question
Given a list of products where each has a `stock` field, print only products with `stock > 0`, and show "All products are out of stock" if none qualify.

---
# PART 6 — Jinja2 Filters ⭐ Very Important
**Level: Intermediate–Advanced**

### 1. Topic Name
Filters — `{{ value|filter_name }}`

### 2. What is it?
A filter is a small function applied to a value using the pipe symbol `|`. It takes the value on its left, transforms it, and prints (or passes along) the result. It's exactly like passing a value into a Python function, just written back-to-front: `{{ name|upper }}` is conceptually `upper(name)`.

### 3. Why do we need it?
Raw data is rarely display-ready. A name might need capitalizing, a price might need rounding to 2 decimals, a list might need joining into a comma-separated string. Rather than pre-formatting every single value in Python (which bloats your routes with display logic), filters let the *template* handle formatting, keeping Python focused on business logic and Jinja2 focused on presentation.

### 4. Syntax
```jinja2
{{ value|filter_name }}
{{ value|filter_name(argument) }}
{{ value|filter_one|filter_two }}   <!-- chaining -->
```

### 5. Simple Example
```jinja2
{{ "  krishna  "|trim|title }}   <!-- "Krishna" -->
```

### 6. Flask Example
```python
# app.py
@app.route("/card")
def card():
    name = "  krishna  "
    price = 1299.5
    skills = ["python", "flask", "sql"]
    return render_template("card.html", name=name, price=price, skills=skills)
```
```jinja2
<!-- templates/card.html -->
<h2>{{ name|trim|title }}</h2>
<p>Price: ₹{{ price|round(2) }}</p>
<p>Skills: {{ skills|join(", ")|upper }}</p>
```

### 7. Line-by-line Explanation — filter chaining
- `{{ name|trim|title }}` runs **left to right**: first `trim` removes leading/trailing whitespace from `"  krishna  "` → `"krishna"`. That *result* is then piped into `title`, which capitalizes each word → `"Krishna"`. Each filter receives the output of the one before it, just like `title(trim(name))` in Python.
- `{{ price|round(2) }}` — `round` here takes an **argument** (2), passed in parentheses just like a normal function call — Jinja2 filters can accept extra arguments beyond the piped value.
- `{{ skills|join(", ")|upper }}` — `join(", ")` turns the list `["python", "flask", "sql"]` into the single string `"python, flask, sql"`; `upper` then uppercases that whole string.

### 8. Expected Output
```
Krishna
Price: ₹1299.50
Skills: PYTHON, FLASK, SQL
```

### 9. Real-world Use Case
Formatting currency, dates, and names consistently across an entire site by using the same filter everywhere, instead of repeating formatting code in every route.

### 10. Common Mistakes
| Mistake | Problem | Fix |
|---|---|---|
| `{{ name | upper }}` with a filter on a variable that's `None` | Some filters error on `None` | Chain with `default` first: `{{ name|default("")|upper }}` |
| Assuming filters run right-to-left | Output looks wrong / unexpected | Filters always run left → right |
| Using a filter name that doesn't exist | `TemplateAssertionError: No filter named 'x'` | Check spelling against the Jinja2 docs, or Part 21 to register your own |

### Reference table — commonly used built-in filters

| Filter | What it does | Example | Result |
|---|---|---|---|
| `upper` | Uppercase | `{{ "hi"|upper }}` | `HI` |
| `lower` | Lowercase | `{{ "HI"|lower }}` | `hi` |
| `capitalize` | First letter of the *string* capitalized, rest lowercased | `{{ "hi there"|capitalize }}` | `Hi there` |
| `title` | Capitalizes each word | `{{ "hi there"|title }}` | `Hi There` |
| `trim` | Removes leading/trailing whitespace | `{{ "  hi  "|trim }}` | `hi` |
| `length` (or `count`) | Number of items/characters | `{{ students|length }}` | `3` |
| `default(val, bool)` | Fallback if undefined/falsy | `{{ nickname|default("Guest") }}` | `Guest` |
| `replace(a, b)` | Replace substring | `{{ "hi"|replace("hi","bye") }}` | `bye` |
| `join(sep)` | List → string | `{{ ["a","b"]|join("-") }}` | `a-b` |
| `first` | First item | `{{ students|first }}` | first element |
| `last` | Last item | `{{ students|last }}` | last element |
| `sort` | Sorted copy | `{{ [3,1,2]|sort }}` | `[1,2,3]` |
| `reverse` | Reversed copy | `{{ [1,2,3]|reverse|list }}` | `[3,2,1]` |
| `unique` | Removes duplicates | `{{ [1,1,2]|unique|list }}` | `[1,2]` |
| `list` | Converts iterator/generator to a real list (many filters return "lazy" iterators, `list` forces them into a printable list) | `{{ (1,2,3)|list }}` | `[1, 2, 3]` |
| `string` | Convert to string | `{{ 5|string }}` | `"5"` |
| `int` | Convert to integer | `{{ "5"|int }}` | `5` |
| `float` | Convert to float | `{{ "5"|float }}` | `5.0` |
| `round(n)` | Round to n decimals | `{{ 3.14159|round(2) }}` | `3.14` |
| `abs` | Absolute value | `{{ -5|abs }}` | `5` |
| `min` | Smallest in iterable | `{{ [3,1,2]|min }}` | `1` |
| `max` | Largest in iterable | `{{ [3,1,2]|max }}` | `3` |
| `sum` | Sum of iterable | `{{ [1,2,3]|sum }}` | `6` |
| `map(attr)` | Apply an operation to every item | `{{ students|map(attribute="name")|list }}` | list of names |
| `select` | Keep items passing a test | see Part 7 | — |
| `selectattr` | Keep dict/obj items whose attribute passes a test | see Part 7 | — |
| `reject` | Opposite of select | see Part 7 | — |
| `rejectattr` | Opposite of selectattr | see Part 7 | — |

**Practical Flask example — `default` (extremely common):**
```jinja2
<p>Bio: {{ user.bio|default("No bio added yet.") }}</p>
```
If `user.bio` is `None`, empty, or missing entirely, this prints the fallback text instead of a blank space or an error — this single filter prevents a huge number of "ugly blank field" bugs.

**Practical Flask example — `map` with `attribute`:**
```python
students = [{"name": "Krishna"}, {"name": "Rahul"}]
```
```jinja2
{{ students|map(attribute="name")|join(", ") }}
<!-- Krishna, Rahul -->
```
`map(attribute="name")` pulls out just the `"name"` field from every dict in the list — extremely useful for turning a list of records into a simple list of one field, ready to `join` into a sentence.

### 11. Practice Question
Given `price = 999.999`, print it rounded to 2 decimals with a "₹" prefix. Given `tags = ["python","flask","flask","sql"]`, print the unique tags joined by commas, all uppercase.

---
# PART 7 — `select`, `selectattr`, `reject`, `rejectattr`
**Level: Advanced**

### 1. Topic Name
Filtering collections of dicts/objects: `select`, `selectattr`, `reject`, `rejectattr`

### 2. What is it?
These are filters that take a **list** and return a *new* list containing only the items that pass (or fail) a test.
- `select` / `reject` work on lists of plain values (numbers, strings).
- `selectattr` / `rejectattr` work on lists of **dicts or objects**, checking one specific attribute/key of each item.

### 3. Why do we need it?
This is the templating equivalent of Python's `filter()`. Instead of writing a separate route just to get "students who passed," you can filter directly in the template when the logic is simple display logic (though for complex business rules, filtering in Python is still cleaner — see Part 24).

### 4. Syntax
```jinja2
{{ numbers|select("odd")|list }}
{{ students|selectattr("marks", "greaterthan", 70)|list }}
{{ students|rejectattr("marks", "lessthan", 50)|list }}
```

### 5. Simple Example
```python
numbers = [1, 2, 3, 4, 5, 6]
```
```jinja2
{{ numbers|select("even")|list }}   <!-- [2, 4, 6] -->
{{ numbers|reject("even")|list }}   <!-- [1, 3, 5] -->
```

### 6. Flask Example
```python
# app.py
@app.route("/toppers")
def toppers():
    students = [
        {"name": "Krishna", "marks": 85},
        {"name": "Rahul", "marks": 65},
        {"name": "Anil", "marks": 92},
    ]
    return render_template("toppers.html", students=students)
```
```jinja2
<!-- templates/toppers.html -->
<h3>Toppers (marks > 80)</h3>
<ul>
{% for s in students|selectattr("marks", "greaterthan", 80) %}
    <li>{{ s.name }} — {{ s.marks }}</li>
{% endfor %}
</ul>

<h3>Need Improvement (marks < 70)</h3>
<ul>
{% for s in students|selectattr("marks", "lessthan", 70) %}
    <li>{{ s.name }} — {{ s.marks }}</li>
{% endfor %}
</ul>
```

### 7. Line-by-line Explanation
- `students|selectattr("marks", "greaterthan", 80)` — for every dict in `students`, Jinja2 looks up the `"marks"` key (this is the *attribute name*, given as a string), then applies the **test** `"greaterthan"` (a Jinja2 test — see Part 14) comparing it against `80`. Only dicts where this test passes make it into the resulting list.
- Note this returns a **generator**, not a list — it's "lazy," meaning it hasn't actually computed the filtered items yet, just set up *how* to compute them. That's fine when you feed it directly into a `{% for %}` loop (loops can consume generators directly), but if you ever want to print it with `{{ }}` or check its length, you must add `|list` first — e.g. `{{ (students|selectattr("marks","greaterthan",80)|list)|length }}`.
- `"greaterthan"`, `"lessthan"`, `"equalto"` are **comparison tests** built into Jinja2, used specifically as the second argument to `selectattr`/`rejectattr`.
- `rejectattr` is the exact mirror of `selectattr` — it keeps items that **fail** the test instead of passing it.

### 8. Expected Output
```
Toppers (marks > 80)
- Krishna — 85
- Anil — 92

Need Improvement (marks < 70)
- Rahul — 65
```

### 9. Real-world Use Case
Building admin dashboards that split one big dataset into multiple views ("active users" vs "inactive users", "in-stock" vs "out-of-stock" products) without hitting the database multiple times or writing multiple Flask routes.

### 10. Common Mistakes
| Mistake | Problem | Fix |
|---|---|---|
| Forgetting `|list` when you need to reuse the result (length, indexing) | `TypeError` or unexpected generator object shown | Add `|list` |
| Using `selectattr` on a list of plain strings | Strings don't have named attributes/keys to check | Use `select` instead for plain-value lists |
| Confusing `select` (values) with `selectattr` (dict/object fields) | Wrong filter picked, `TypeError` | `select` = simple values, `selectattr` = dicts/objects |

### 11. Practice Question
Given the `students` list from above, print the names only (using `map(attribute="name")`) of students with `marks` greater than or equal to 70, joined into one comma-separated sentence.

---
# PART 8 — Template Inheritance ⭐⭐⭐ Very Important
**Level: Intermediate–Advanced**

### 1. Topic Name
Template Inheritance — `{% extends %}` and `{% block %}`

### 2. What is it?
Template inheritance lets you define one **base/parent template** with the common page skeleton (header, navbar, footer, `<html>`/`<head>` boilerplate) and mark certain regions as **blocks** — named "fill-in-the-blank" zones. Every other page then **extends** this base and only supplies the content for those specific blocks, inheriting everything else automatically.

### 3. Why do we need it?
Without inheritance, every single page (`home.html`, `about.html`, `contact.html`...) would need its own copy-pasted `<head>`, navbar, and footer. Change your site's logo once, and you'd have to edit 20 files. Inheritance means you edit `base.html` once, and *every* child page updates automatically — this is the single most important concept for avoiding repeated HTML in Flask apps.

### 4. Syntax
```jinja2
<!-- base.html -->
{% block content %}{% endblock %}

<!-- child.html -->
{% extends "base.html" %}
{% block content %}
    ...
{% endblock %}
```

### 5. Simple Example
```jinja2
<!-- base.html -->
<h1>My Site</h1>
{% block content %}
    <p>Default content</p>
{% endblock %}
```
```jinja2
<!-- child.html -->
{% extends "base.html" %}
{% block content %}
    <p>Custom page content!</p>
{% endblock %}
```
Rendering `child.html` produces: `<h1>My Site</h1><p>Custom page content!</p>` — the block's default text was **replaced**, everything outside the block was **kept**.

### 6. Flask Example — full project

**Project structure:**
```text
project/
├── app.py
└── templates/
    ├── base.html
    ├── home.html
    ├── about.html
    └── contact.html
```

```python
# app.py
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")
```

```jinja2
<!-- templates/base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}My Site{% endblock %}</title>
</head>
<body>
    <nav>
        <a href="{{ url_for('home') }}">Home</a> |
        <a href="{{ url_for('about') }}">About</a> |
        <a href="{{ url_for('contact') }}">Contact</a>
    </nav>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        <p>&copy; 2026 My Site</p>
    </footer>
</body>
</html>
```

```jinja2
<!-- templates/home.html -->
{% extends "base.html" %}

{% block title %}Home — My Site{% endblock %}

{% block content %}
    <h1>Welcome Home!</h1>
    <p>This is the homepage.</p>
{% endblock %}
```

```jinja2
<!-- templates/about.html -->
{% extends "base.html" %}

{% block title %}About — My Site{% endblock %}

{% block content %}
    <h1>About Us</h1>
    <p>We build Flask apps.</p>
{% endblock %}
```

### 7. Line-by-line Explanation
- `{% extends "base.html" %}` **must be the very first line** of a child template. It tells Jinja2: "start by rendering `base.html`, and wherever `base.html` defines a `{% block %}`, look for a matching block in *this* file to override it."
- `{% block content %}{% endblock %}` in `base.html` is a **named placeholder**. The name (`content`) is how Jinja2 matches it up with the child's own `{% block content %}...{% endblock %}`.
- You can have **multiple blocks** — here there are two: `title` (for the `<title>` tag, letting each page set its own browser-tab title) and `content` (the main body). Each is overridden independently.
- If a child template doesn't override a block at all, Jinja2 falls back to whatever default content was written inside that block in the base file (in our simple example, `<p>Default content</p>`).
- `url_for('home')` inside the shared navbar works correctly on *every* page that extends `base.html`, because it's evaluated fresh each time the *final combined* template renders (see Part 15).

**Rendering flow diagram:**
```text
base.html  (skeleton: nav + footer + empty blocks)
     ↓  extends
home.html  (fills in {% block title %} and {% block content %})
     ↓  Jinja2 merges child content INTO the base skeleton
Final combined HTML string
     ↓
Browser
```
Jinja2 processes this from the *child's* perspective: it reads `home.html`, sees `{% extends %}`, jumps to `base.html`, builds the full page structure, then plugs the child's block content into the matching slots — the child never independently produces its own full HTML document; it only supplies fragments.

### 8. Expected Output (visiting `/`)
```
[Home | About | Contact]   <- navbar, same on every page

Welcome Home!
This is the homepage.

© 2026 My Site
```

### 9. Real-world Use Case
Every multi-page Flask site (e-commerce, dashboards, blogs) uses one `base.html` for consistent layout, navigation, and styling, with each page template staying tiny and focused only on its unique content.

### 10. Common Mistakes
| Mistake | Problem | Fix |
|---|---|---|
| `{% extends %}` not on the first line | Jinja2 raises an error or silently misbehaves | Always make it line 1 |
| Block name mismatch (`{% block Content %}` vs `{% block content %}`) | Jinja2 treats them as different blocks — child content just doesn't appear | Names are case-sensitive; match exactly |
| Forgetting `{% endblock %}` | `TemplateSyntaxError` | Always close blocks |
| Putting content in the child *outside* any block | It's silently ignored — only content inside a matching block gets used | Wrap all your real content inside `{% block %}...{% endblock %}` |

### Nested blocks
You can nest a block inside another block for more granular overriding:
```jinja2
{% block content %}
    <div class="page">
        {% block page_content %}{% endblock %}
    </div>
{% endblock %}
```
A child can override just `page_content` while leaving the surrounding `<div class="page">` wrapper from the parent's `content` block intact — useful when several pages share a common wrapper but need different inner content.

### 11. Practice Question
Create a `base.html` with blocks `title` and `content`, then create `contact.html` that extends it and shows a contact form heading. Add a third block called `sidebar` to `base.html` with a default `"No sidebar content"` message, and override it only in `about.html`.

---
# PART 9 — `include`
**Level: Intermediate**

### 1. Topic Name
`{% include %}`

### 2. What is it?
`include` inserts the full rendered content of *another* template file at that exact spot — like copy-pasting a reusable HTML snippet into place, but done automatically by Jinja2.

### 3. Why do we need it?
Some UI pieces (a navbar, footer, a "product card," an alert banner) appear on many *different* base layouts, or repeat many times on the *same* page (e.g. one card per product). `include` lets you write that snippet once as its own small file and reuse it anywhere, keeping templates DRY (Don't Repeat Yourself).

### 4. Syntax
```jinja2
{% include "navbar.html" %}
```

### 5. Simple Example
```jinja2
<!-- alert.html -->
<div class="alert">{{ message }}</div>
```
```jinja2
<!-- page.html -->
{% set message = "Saved successfully!" %}
{% include "alert.html" %}
```
`alert.html` automatically sees `message` because included templates share the **same context** as the page that includes them.

### 6. Flask Example
**Project structure:**
```text
templates/
├── base.html
├── navbar.html
├── footer.html
└── home.html
```
```jinja2
<!-- templates/navbar.html -->
<nav>
    <a href="{{ url_for('home') }}">Home</a> |
    <a href="{{ url_for('about') }}">About</a>
</nav>
```
```jinja2
<!-- templates/footer.html -->
<footer><p>&copy; 2026 My Site</p></footer>
```
```jinja2
<!-- templates/base.html -->
<!DOCTYPE html>
<html>
<body>
    {% include "navbar.html" %}
    {% block content %}{% endblock %}
    {% include "footer.html" %}
</body>
</html>
```

### 7. Line-by-line Explanation
- `{% include "navbar.html" %}` renders `navbar.html` fully (running any `{{ }}`/`{% %}` inside it, like `url_for`) and drops the resulting HTML directly into `base.html` at that line.
- Because `base.html` is itself extended by every child page (Part 8), the navbar and footer now automatically appear on *every* page in the site with **zero repetition** — you maintain one navbar file, not one per page.
- Included templates automatically have access to all variables currently in scope where the `include` is called — you don't need to explicitly pass them (though you *can* restrict this with `{% include "x.html" without context %}` if needed).

### 8. Expected Output
Any page extending `base.html` shows the same navbar and footer automatically, with page-specific content sandwiched in between.

### `extends` vs `include` — the crucial difference

| | `{% extends %}` | `{% include %}` |
|---|---|---|
| Direction of control | Child *inherits* the parent's structure — parent is in charge | Current template *pulls in* another file — current file is in charge |
| Used for | Whole-page layout/skeleton (one base per page) | Small reusable fragments (navbar, card, alert) — often multiple per page |
| How many per file | Exactly one `{% extends %}`, and it must be the first line | Any number of `{% include %}`, anywhere in the file |
| Blocks involved? | Yes — relies on named `{% block %}` regions | No blocks needed at all |
| Analogy | "This page IS-A type of base page" | "Paste this snippet here" |

### 9. Real-world Use Case
`include` for: navbars, footers, flash-message banners, a single product/user "card" repeated in a loop, sidebar widgets. `extends` for: the one overall page skeleton every page shares.

### 10. Common Mistakes
| Mistake | Problem | Fix |
|---|---|---|
| Using `include` where `extends` was needed (or vice versa) | Confusing structure, blocks don't work as expected | Use `extends` for page skeleton, `include` for reusable snippets |
| Wrong file path in `include` | `TemplateNotFound` | Path is relative to the `templates/` folder root |
| Assuming an included file needs variables passed explicitly | Unnecessary complexity | Included files automatically see the calling template's variables |

### 11. Practice Question
Create a `card.html` snippet that displays a single student's name and marks, then use `{% include "card.html" %}` inside a `{% for %}` loop over a list of students to render one card per student.

---
# PART 10 — `macro`
**Level: Advanced**

### 1. Topic Name
Macros — `{% macro %}...{% endmacro %}`

### 2. What is it?
A macro is a **reusable, parameterized block of HTML** — essentially a function that returns HTML instead of a Python value. You define it once with parameters, then "call" it wherever you need that HTML, passing in different arguments each time.

### 3. Why do we need it?
`{% include %}` reuses a *static* fragment, but it can't take parameters — its content only changes via variables already in scope. Macros solve this: they let you build genuinely reusable **components**, like a styled form input, that need different labels/names/types every time they're used, without duplicating the surrounding `<label>`/`<input>`/error-message HTML each time.

### 4. Syntax
```jinja2
{% macro input_field(name, type="text") %}
    <label>{{ name }}</label>
    <input type="{{ type }}" name="{{ name }}">
{% endmacro %}

{{ input_field("username") }}
{{ input_field("password", type="password") }}
```

### 5. Simple Example
```jinja2
{% macro greet(name) %}
    <p>Hello, {{ name }}!</p>
{% endmacro %}

{{ greet("Krishna") }}
{{ greet("Rahul") }}
```
Output:
```
Hello, Krishna!
Hello, Rahul!
```

### 6. Flask Example — reusable form component

**Project structure:**
```text
templates/
├── base.html
├── macros.html
└── forms.html
```
```jinja2
<!-- templates/macros.html -->
{% macro input_field(name, label, type="text", value="") %}
    <div class="form-group">
        <label for="{{ name }}">{{ label }}</label>
        <input
            type="{{ type }}"
            id="{{ name }}"
            name="{{ name }}"
            value="{{ value }}"
        >
    </div>
{% endmacro %}
```
```jinja2
<!-- templates/forms.html -->
{% extends "base.html" %}
{% from "macros.html" import input_field %}

{% block content %}
    <form method="POST">
        {{ input_field("name", "Full Name") }}
        {{ input_field("email", "Email Address", type="email") }}
        {{ input_field("password", "Password", type="password") }}
        <button type="submit">Register</button>
    </form>
{% endblock %}
```

### 7. Line-by-line Explanation
- `{% macro input_field(name, label, type="text", value="") %}` defines a macro named `input_field` with four **parameters**. `type="text"` and `value=""` are **default parameters** — if the caller doesn't supply them, these values are used automatically (identical concept to Python default function arguments).
- `{{ input_field("name", "Full Name") }}` calls the macro with just two positional arguments; `type` and `value` fall back to their defaults (`"text"` and `""`).
- `{{ input_field("email", "Email Address", type="email") }}` overrides the `type` default by passing it as a **keyword argument**, exactly like calling a Python function.
- Every call to `input_field` generates a completely independent block of labeled-input HTML, with no repeated markup written by hand — this is the real payoff: three calls, one definition.

### Python function vs Jinja2 macro

| | Python function | Jinja2 macro |
|---|---|---|
| Lives in | `.py` file | `.html` template file |
| Returns | Any Python value (int, list, dict...) | A string of rendered HTML |
| Runs | On the server, before rendering starts | During template rendering itself |
| Purpose | Business logic, calculations, data fetching | Reusable presentation/markup |
| Can it query a database? | Yes | Technically possible but strongly discouraged — keep logic in Python |

### 8. Expected Output
Three neatly labeled form fields (`Full Name` as text, `Email Address` as an email input, `Password` as a password input), all sharing identical `<div class="form-group">` styling, generated from one macro definition.

### 9. Real-world Use Case
Any repeated UI component with variations: form fields, button styles, star-rating widgets, table row templates, badge/label components across an admin dashboard.

### 10. Common Mistakes
| Mistake | Problem | Fix |
|---|---|---|
| Forgetting `{% endmacro %}` | `TemplateSyntaxError` | Always close the macro |
| Defining a macro directly inside the file that uses it dozens of times across the project | Leads to duplicate definitions across files | Put shared macros in one dedicated file (e.g. `macros.html`) and import them (Part 11) |
| Passing arguments in the wrong order without keywords | Wrong values land in the wrong slots (e.g. label text ends up as the `name` attribute) | Use keyword arguments for clarity, especially past the first 1–2 params |

### 11. Practice Question
Write a macro `render_button(text, css_class="btn-primary")` that outputs a `<button class="{{ css_class }}">{{ text }}</button>`, then call it twice — once with defaults, once overriding `css_class` to `"btn-danger"`.

---

# PART 11 — Importing Macros
**Level: Advanced**

### 1. Topic Name
`{% import %}` vs `{% from ... import ... %}`

### 2. What is it?
Since macros usually live in a separate file (e.g. `macros.html`), you need a way to bring them into whatever template wants to use them — exactly like Python's `import` statement.

### 3. Why do we need it?
Without importing, a macro defined in `macros.html` simply isn't visible inside `forms.html` — Jinja2 templates don't automatically share macros across files; each file's macros are private until explicitly imported.

### 4. Syntax
```jinja2
{% import "macros.html" as forms %}
{{ forms.input_field("username", "Username") }}
```
```jinja2
{% from "macros.html" import input_field %}
{{ input_field("username", "Username") }}
```

### 5. Simple Example
```jinja2
<!-- macros.html -->
{% macro shout(text) %}{{ text|upper }}!!!{% endmacro %}
```
```jinja2
<!-- Option A: import as namespace -->
{% import "macros.html" as m %}
{{ m.shout("hello") }}     <!-- HELLO!!! -->

<!-- Option B: import specific names -->
{% from "macros.html" import shout %}
{{ shout("hello") }}       <!-- HELLO!!! -->
```

### 6. Flask Example
(Reusing `macros.html` and `forms.html` from Part 10 — that file already uses `{% from "macros.html" import input_field %}`.)
```jinja2
<!-- Alternative: importing as a namespace instead -->
{% extends "base.html" %}
{% import "macros.html" as forms %}

{% block content %}
    <form method="POST">
        {{ forms.input_field("name", "Full Name") }}
        {{ forms.input_field("email", "Email Address", type="email") }}
        <button type="submit">Register</button>
    </form>
{% endblock %}
```

### 7. Line-by-line Explanation — the difference
- `{% import "macros.html" as forms %}` loads *all* macros from `macros.html` into a single namespace object called `forms`. You then access each macro through it: `forms.input_field(...)`, `forms.another_macro(...)`. This is like Python's `import module_name` — you always prefix with the module name.
- `{% from "macros.html" import input_field %}` pulls just the one named macro `input_field` directly into the current template's scope — you call it bare, `input_field(...)`, no prefix. This is like Python's `from module import specific_function`.
- **When to use which:** if a file uses *many* macros from the same source, `import ... as` keeps things organized and avoids name clashes (`forms.input_field` vs `cards.input_field` could coexist). If you only need one or two macros, `from ... import` is shorter and cleaner.

### 8. Expected Output
Identical output either way — the choice is purely about code organization, not behavior.

### 9. Real-world Use Case
Large Flask apps typically keep one `macros.html` (or several, split by purpose: `form_macros.html`, `table_macros.html`) and import them wherever forms or tables are rendered, keeping every form on the site visually and structurally consistent.

### 10. Common Mistakes
| Mistake | Problem | Fix |
|---|---|---|
| Mixing `import` and `from...import` inconsistently across a big project | Confusing to read/maintain | Pick one convention per project and stick to it |
| Forgetting the macro file path is relative to `templates/` | `TemplateNotFound` | Double-check the path matches your actual folder structure |
| Placing `{% import %}`/`{% from %}` after using the macro | `UndefinedError` — macro not yet available | Imports must appear before first use, typically near the top of the file |

### 11. Practice Question
Create `macros.html` with two macros: `render_button` (from Part 10) and a new `render_badge(text, color="grey")` that outputs a colored `<span>`. Import both into a page using `{% from ... import ... %}` with a comma-separated list, and use each once.

---
# PART 12 — `set`
**Level: Intermediate**

### 1. Topic Name
`{% set %}` — creating/computing variables inside a template

### 2. What is it?
`{% set %}` creates a new variable *inside* the template, or computes one from existing variables — like a Python assignment (`x = 5`), but living entirely within Jinja2's world.

### 3. Why do we need it?
Sometimes you need a small computed value (a total, a formatted label, a flag) that's only relevant for display and isn't worth sending from Flask. `set` avoids repeating the same expression (`{{ price * quantity }}`) multiple times in one template.

### 4. Syntax
```jinja2
{% set name = "Krishna" %}
{% set total = price * quantity %}
```

### 5. Simple Example
```jinja2
{% set price = 100 %}
{% set quantity = 3 %}
{% set total = price * quantity %}
<p>Total: {{ total }}</p>   <!-- Total: 300 -->
```

### 6. Flask Example
```python
# app.py
@app.route("/cart")
def cart():
    items = [
        {"name": "Pen", "price": 10, "qty": 5},
        {"name": "Book", "price": 200, "qty": 2},
    ]
    return render_template("cart.html", items=items)
```
```jinja2
<!-- templates/cart.html -->
{% set grand_total = 0 %}
<table>
{% for item in items %}
    {% set line_total = item.price * item.qty %}
    {% set grand_total = grand_total + line_total %}
    <tr>
        <td>{{ item.name }}</td>
        <td>{{ item.qty }}</td>
        <td>₹{{ line_total }}</td>
    </tr>
{% endfor %}
</table>
<p>Grand Total: ₹{{ grand_total }}</p>
```

### 7. Line-by-line Explanation — an important gotcha
- `{% set line_total = item.price * item.qty %}` computes a fresh value each loop iteration — this works fine because it's a brand-new variable each time.
- **BUT** `{% set grand_total = grand_total + line_total %}` **does not actually work as written** inside a `{% for %}` loop in standard Jinja2! Variables set with plain `{% set %}` inside a loop are scoped *to that iteration only* — the running total resets and doesn't "leak" out to the next loop pass or outside the loop, because loops create a new inner scope each time. This is a very common beginner trap.
- **The fix** uses a `namespace()` object, which Jinja2 provides specifically to work around this scoping limitation:
```jinja2
{% set ns = namespace(total=0) %}
{% for item in items %}
    {% set ns.total = ns.total + item.price * item.qty %}
{% endfor %}
<p>Grand Total: ₹{{ ns.total }}</p>
```
Because `ns` is an object (a namespace), modifying `ns.total` mutates the *same* object across iterations instead of creating a new locally-scoped variable each time — so the running sum correctly persists.

### Block `set`
For multi-line or HTML-containing values:
```jinja2
{% set greeting %}
    <strong>Hello, {{ name }}!</strong>
{% endset %}
{{ greeting }}
```
This captures a whole rendered block of HTML into a variable, useful when you want to reuse a chunk of markup multiple times in the same template.

### 8. Expected Output
```
Pen     5   ₹50
Book    2   ₹400
Grand Total: ₹450
```

### 9. Real-world Use Case
Shopping cart totals, computing a percentage/progress value for a progress bar, building a temporary display label from multiple fields (`{% set full_name = student.first + " " + student.last %}`).

### 10. Common Mistakes
| Mistake | Problem | Fix |
|---|---|---|
| Accumulating a total across loop iterations with plain `{% set %}` | Silently doesn't work — value resets every iteration | Use `namespace()` |
| Overusing `set` for real business logic (discounts, tax calculation) | Business rules get buried in HTML, hard to test/maintain | Compute it in Flask/Python and pass the final value in |
| Expecting `set` variables to persist across different template files | They don't — each template's `set` variables are local to that file (unless passed explicitly or set in a parent before an include) | Pass computed values through `render_template()` context instead |

**When `set` should and shouldn't be used:** Use it for small, purely presentational computations local to one template. Avoid it for anything resembling business logic (discounts, validation, security checks) — that always belongs in Flask/Python, where it's testable and reusable outside the browser.

### 11. Practice Question
Given `price = 500` and `discount_percent = 10`, use `{% set %}` to compute the discounted price and display both the original and discounted price.

---

# PART 13 — Expressions and Operators
**Level: Intermediate**

### 1. Topic Name
Arithmetic, comparison, logical, string, and membership operators in Jinja2

### 2. What is it?
Jinja2 expressions support most of the same operators as Python, letting you compute values and check conditions directly inside `{{ }}` and `{% %}`.

### 3. Why do we need it?
Templates constantly need small computations (totals, percentages) and checks (does this list contain X?) without needing a full round-trip back to Python for every tiny detail.

### 4. Syntax & Reference Table

| Category | Operators | Example | Result |
|---|---|---|---|
| Arithmetic | `+ - * / // % **` | `{{ price * quantity }}` | product |
| Comparison | `== != > < >= <=` | `{{ marks >= 50 }}` | `True`/`False` |
| Logical | `and or not` | `{% if a and not b %}` | — |
| String concat | `~` (converts both sides to string and joins) | `{{ "Hi " ~ name }}` | `"Hi Krishna"` |
| Membership | `in`, `not in` | `{% if "Python" in skills %}` | — |
| Identity/type test | `is` | `{% if value is none %}` | — |

### 5. Simple Example
```jinja2
{{ 10 // 3 }}      <!-- 3  (floor/integer division) -->
{{ 10 % 3 }}       <!-- 1  (remainder) -->
{{ 2 ** 3 }}       <!-- 8  (power) -->
{{ "Hi " ~ 5 }}     <!-- "Hi 5" — ~ converts 5 to string automatically -->
```

### 6. Flask Example
```python
# app.py
@app.route("/product")
def product():
    price = 250
    quantity = 4
    skills = ["Python", "Flask", "SQL"]
    return render_template("product.html", price=price, quantity=quantity, skills=skills)
```
```jinja2
<!-- templates/product.html -->
<p>Total: ₹{{ price * quantity }}</p>

{% if "Python" in skills %}
    <p>Python skill confirmed.</p>
{% endif %}

{% if price > 200 and quantity >= 3 %}
    <p>Eligible for bulk discount!</p>
{% endif %}

<p>{{ "Item cost: " ~ price ~ " x " ~ quantity }}</p>
```

### 7. Line-by-line Explanation
- `price * quantity` — standard arithmetic; Jinja2 respects Python's usual operator precedence (`*`/`/` before `+`/`-`), and you can use parentheses to group, exactly as in Python.
- `"Python" in skills` — the `in` operator checks membership: for a list it checks if the value is an element; for a string it checks substring presence (`"yth" in "Python"` → `True`); for a dict it checks if the value matches a *key*.
- `price > 200 and quantity >= 3` — `and`/`or`/`not` combine multiple boolean conditions exactly like Python; both sides are evaluated to `True`/`False` first, then combined.
- `"Item cost: " ~ price ~ " x " ~ quantity` — the `~` operator is Jinja2's dedicated **string concatenation operator**. Unlike `+`, which would error if you tried `"text" + 250` (can't add a string and an int in Python), `~` automatically converts every value to its string form before joining — this makes it the safer, more common choice for building mixed text+number strings inline.

### 8. Expected Output
```
Total: ₹1000
Python skill confirmed.
Eligible for bulk discount!
Item cost: 250 x 4
```

### 9. Real-world Use Case
Computing line totals in a cart, checking permission flags (`"admin" in user.roles`), building small formatted strings for labels/tooltips.

### 10. Common Mistakes
| Mistake | Problem | Fix |
|---|---|---|
| Using `+` to join a string and a number | `TypeError`-style rendering error | Use `~` instead of `+` for mixed-type concatenation |
| Confusing `/` and `//` | `/` gives a float (`10/3 = 3.333...`), `//` gives integer floor division (`10//3 = 3`) | Pick the one matching what you actually need |
| Writing `if a and or b` (invalid combination) | Syntax error | Use proper grouping: `if (a and b) or c` |

### 11. Practice Question
Given `cart_total = 850` and `free_shipping_threshold = 1000`, print `"Add ₹150 more for free shipping"` computed with arithmetic, only if the total is below the threshold.

---

# PART 14 — Tests
**Level: Advanced**

### 1. Topic Name
Jinja2 Tests — used with the `is` keyword

### 2. What is it?
A **test** checks whether a value has a certain *property* or *type*, returning `True`/`False`. Tests are used after the keyword `is`: `{% if value is defined %}`.

### 3. Why do we need it?
Templates often receive optional or uncertain data — a variable that might not have been passed at all, or might be `None`, or might be the wrong type. Tests let you safely check these conditions *before* trying to use the value, preventing errors.

### 4. Syntax
```jinja2
{% if value is defined %}
{% if value is not none %}
{% if value is string %}
```

### 5. Simple Example
```jinja2
{% if nickname is defined %}
    Hello, {{ nickname }}
{% else %}
    Nickname not provided
{% endif %}
```

### 6. Flask Example
```python
# app.py
@app.route("/user/<name>")
def user_page(name):
    # note: "age" is intentionally NOT passed
    return render_template("user.html", name=name)
```
```jinja2
<!-- templates/user.html -->
<p>Name: {{ name }}</p>

{% if age is defined %}
    <p>Age: {{ age }}</p>
{% else %}
    <p>Age not provided.</p>
{% endif %}

{% if name is string %}
    <p>Name is text data.</p>
{% endif %}
```

### Reference table — commonly used tests

| Test | Checks | Example |
|---|---|---|
| `defined` | Variable exists in context | `{% if x is defined %}` |
| `undefined` | Variable does NOT exist | `{% if x is undefined %}` |
| `none` | Value is exactly `None` | `{% if x is none %}` |
| `boolean` | Is a `True`/`False` value | `{% if x is boolean %}` |
| `true` / `false` | Is specifically `True` / `False` | `{% if x is true %}` |
| `string` | Is a string | `{% if x is string %}` |
| `number` | Is any numeric type | `{% if x is number %}` |
| `integer` | Is specifically an int | `{% if x is integer %}` |
| `float` | Is specifically a float | `{% if x is float %}` |
| `iterable` | Can be looped over | `{% if x is iterable %}` |
| `mapping` | Is dict-like | `{% if x is mapping %}` |
| `sequence` | Is list-like (ordered) | `{% if x is sequence %}` |
| `sameas` | Is the exact same object (identity, like Python's `is`) | `{% if x is sameas none %}` |

### 7. Line-by-line Explanation
- `{% if age is defined %}` — before Jinja2 even tries to *read* the value of `age`, this checks whether the key `"age"` exists in the render context at all. If you tried `{{ age }}` directly without this check and `age` was never passed, Jinja2 would raise an `UndefinedError` (in strict configurations) or silently print nothing — checking `is defined` first avoids that uncertainty.
- `{% if name is string %}` — this checks the actual Python *type* of the value, useful when a variable could sometimes be a string and sometimes something else (e.g., an ID that might be an `int` or a `str` depending on where it came from).

### Filter vs Test — the crucial distinction

| | Filter | Test |
|---|---|---|
| Syntax | `value|filter_name` | `value is test_name` |
| Purpose | **Transforms** a value into a new value | **Checks** a condition, returns True/False |
| Used with | `{{ }}` (to print the transformed result) | `{% if %}` (to branch based on the result) |
| Example | `{{ name|upper }}` → `"KRISHNA"` | `{% if name is string %}` → `True` |
| Can you chain them? | Yes, filters chain: `a|b|c` | Tests don't chain the same way — combine with `and`/`or` instead |

### 8. Expected Output (visiting `/user/Krishna`)
```
Name: Krishna
Age not provided.
Name is text data.
```

### 9. Real-world Use Case
Safely handling optional profile fields, checking if a database query returned `None` before accessing its attributes, verifying a form field's type before formatting it.

### 10. Common Mistakes
| Mistake | Problem | Fix |
|---|---|---|
| Confusing `is undefined` with `is none` | A variable can be explicitly set to `None` (defined, but empty) vs never passed at all (undefined) — these are different states | Use `is defined`/`is undefined` for "was it passed at all," `is none` for "was it passed as empty" |
| Using `|` instead of `is` for a test | `{{ x|defined }}` — wrong syntax, `defined` isn't a filter | Use `{% if x is defined %}` |
| Assuming every variable exists by default | Leads to `UndefinedError` crashes in production | Test with `is defined` or use the `default` filter for safety |

### 11. Practice Question
Write a check that prints `"Score not entered"` if a `score` variable is undefined, `"No score yet"` if it's `None`, and the actual score otherwise.

---
# PART 15 — `url_for()` Inside Jinja2
**Level: Intermediate — Very Important ⭐**

### 1. Topic Name
`url_for()` — dynamic URL generation in templates

### 2. What is it?
`url_for()` is a Flask function (automatically made available inside every Jinja2 template) that generates the correct URL for a given route function's **name**, rather than you typing the URL path by hand.

### 3. Why do we need it?
If you hardcode links like `<a href="/students/edit/5">`, changing that route's URL pattern later in `app.py` (say from `/students/edit/<id>` to `/students/<id>/edit`) means hunting down and fixing every hardcoded link across every template. `url_for('edit_student', id=5)` always produces the *current, correct* URL automatically, because it asks Flask's routing system directly instead of guessing.

### 4. Syntax
```jinja2
<a href="{{ url_for('function_name') }}">Link</a>
<a href="{{ url_for('function_name', id=5) }}">Link with param</a>
{{ url_for('static', filename='css/style.css') }}
```

### 5. Simple Example
```python
# app.py
@app.route("/about")
def about():
    return render_template("about.html")
```
```jinja2
<a href="{{ url_for('about') }}">About Us</a>
<!-- generates: <a href="/about">About Us</a> -->
```

### 6. Flask Example — dynamic route + static file
```python
# app.py
@app.route("/student/<int:id>")
def student_detail(id):
    return render_template("detail.html", id=id)
```
```jinja2
<!-- templates/detail.html -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">

<a href="{{ url_for('student_detail', id=5) }}">View Student 5</a>
<a href="{{ url_for('student_detail', id=id) }}">View This Student Again</a>
```

### 7. Line-by-line Explanation
- `url_for('student_detail', id=5)` — the **first argument is the Python function's name** (`student_detail`), *not* the route path string (`/student/<int:id>`). Flask looks up which route was registered with `@app.route(...)` on top of a function called `student_detail`, and reconstructs its URL pattern.
- `id=5` is passed as a keyword argument matching the `<int:id>` placeholder in that route's path — Flask substitutes it in, producing `/student/5`.
- `url_for('static', filename='css/style.css')` is a **special built-in endpoint** Flask registers automatically for every app to serve files from the `static/` folder — it produces something like `/static/css/style.css`, and importantly, Flask can add cache-busting query strings to this automatically in some configurations, another reason to never hardcode static paths.

### Why `url_for()` beats hardcoding
| Hardcoded `<a href="/student/5">` | `{{ url_for('student_detail', id=5) }}` |
|---|---|
| Breaks silently if the route path changes | Always matches the current route definition |
| Doesn't handle special characters/encoding automatically | Automatically URL-encodes parameters |
| No compile-time/render-time check that the route even exists | Raises a clear error immediately if the route name is misspelled or missing |

### 8. Expected Output
```html
<link rel="stylesheet" href="/static/css/style.css">
<a href="/student/5">View Student 5</a>
<a href="/student/5">View This Student Again</a>
```

### 9. Real-world Use Case
Every navbar, every "Edit"/"Delete"/"View" link in a table of records, every CSS/JS/image reference in your `<head>` — always generated through `url_for()`, never hand-typed.

### 10. Common Mistakes
| Mistake | Problem | Fix |
|---|---|---|
| Passing the URL path instead of the function name: `url_for('/student/5')` | `BuildError: Could not build url` | Always use the Python function's name |
| Forgetting required arguments for a dynamic route | `BuildError` | Supply every `<param>` the route needs as a keyword argument |
| Hardcoding `/static/...` paths | Breaks if static folder config changes, misses caching benefits | Always use `url_for('static', filename=...)` |

### 11. Practice Question
Given a route `@app.route("/products/<category>/<int:id>")` with function name `product_detail`, write the `url_for()` call to link to category `"books"`, id `12`.

---

# PART 16 — `request` Object Inside Templates
**Level: Intermediate**

### 1. Topic Name
Accessing Flask's `request` object in Jinja2

### 2. What is it?
Flask automatically injects the current `request` object into every template's context. It represents the **incoming HTTP request** — the URL, HTTP method, form data, query parameters, headers, and more — the same `request` object you already use inside Flask routes (`from flask import request`).

### 3. Syntax
```jinja2
{{ request.method }}
{{ request.path }}
{{ request.args.get('q') }}
```

### 4. Simple Example
```jinja2
<p>You visited: {{ request.path }}</p>
<p>Using method: {{ request.method }}</p>
```

### 5. Flask Example — highlighting the active nav link
```jinja2
<!-- templates/navbar.html -->
<nav>
    <a href="{{ url_for('home') }}"
       class="{% if request.path == url_for('home') %}active{% endif %}">
        Home
    </a>
    <a href="{{ url_for('about') }}"
       class="{% if request.path == url_for('about') %}active{% endif %}">
        About
    </a>
</nav>
```

### 6. Line-by-line Explanation
- `request.path` returns the current URL path being viewed, e.g. `/about` — no need for Flask to explicitly pass this in; it's always available.
- `request.path == url_for('home')` compares the *current* page's path against the URL that the "Home" link would point to — if they match, the `active` CSS class is added, giving a highlighted nav-link effect purely through template logic.
- `request.args.get('q')` reads a URL query parameter (e.g. `?q=python` → `"python"`) — useful for showing "You searched for: ..." on a search-results page without Flask needing to pass the search term separately.

### 7. Why it should sometimes be avoided
`request` gives templates access to *raw* incoming data, including form submissions and query strings. It's tempting to do validation or business decisions (`{% if request.args.get('admin') == 'true' %}` to show admin content) directly in the template — **don't**. Security-sensitive checks belong in Flask/Python, where you have proper control flow, error handling, and can't accidentally leak logic into client-visible HTML comments or be bypassed by a user directly editing the URL. Templates should only *read* `request` for harmless display purposes (showing the current path, echoing back a search term), never for authorization decisions.

### 8. Expected Output (visiting `/about`)
```html
<a href="/" class="">Home</a>
<a href="/about" class="active">About</a>
```

### 9. Real-world Use Case
Active nav-link highlighting, showing "no results for '{{ request.args.get('q') }}'" on search pages, displaying breadcrumbs based on `request.path`.

### 10. Common Mistakes
| Mistake | Problem | Fix |
|---|---|---|
| Using `request` for security/authorization checks in templates | Security logic becomes fragile and hard to audit | Do all auth checks in Flask route code, pass only a simple `is_admin` boolean to the template |
| `request.args.get('q')` without a default when `q` might be missing | Prints "None" awkwardly | `request.args.get('q', '')` or chain with `|default('')` |

### 11. Practice Question
Add "active" highlighting (as shown above) to a 3-link navbar for Home, About, and Contact.

---

# PART 17 — `session` Inside Templates
**Level: Intermediate**

### 1. Topic Name
Accessing Flask's `session` in Jinja2

### 2. What is it?
`session` is Flask's built-in mechanism for storing small pieces of data (like "is this user logged in," "what's their username") that persist across multiple requests from the same browser, using a signed cookie. Like `request`, Flask automatically makes `session` available inside every template.

### 3. Syntax
```jinja2
{{ session["username"] }}
{{ session.get("username") }}
```

### 4. Flask Example — login-aware navbar
```python
# app.py
from flask import Flask, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "replace-with-a-real-secret-key"

@app.route("/login/<username>")
def login(username):
    session["username"] = username
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))

@app.route("/")
def home():
    return render_template("home.html")
```
```jinja2
<!-- templates/navbar.html -->
<nav>
    {% if session.get("username") %}
        <span>Welcome, {{ session["username"] }}</span>
        <a href="{{ url_for('logout') }}">Logout</a>
    {% else %}
        <a href="{{ url_for('login', username='guest') }}">Login</a>
        <a href="#">Register</a>
    {% endif %}
</nav>
```

### 5. Line-by-line Explanation
- `session["username"] = username` (in Python) writes the value into the session cookie — Flask handles the encoding/signing behind the scenes, so this data is tamper-resistant (a user can't just edit the cookie to change their username, since Flask verifies a cryptographic signature using `app.secret_key`).
- `session.get("username")` in the template is the **safe** way to check for a session value — if `"username"` was never set (user never logged in), `.get()` simply returns `None` instead of raising a `KeyError`, unlike `session["username"]` which would error if the key is missing.
- **Why `.get()` is preferred over bracket access here specifically:** unlike the earlier dict-access discussion in Part 2 (where dot notation `.name` is usually the safe choice), `session` behaves like a genuine Python dict, and bracket access on a *missing* key raises an error — so `.get()` (or a `{% if 'username' in session %}` check) is the safer default when the key might not exist.

### 6. Expected Output
```
Not logged in:  [Login] [Register]
Logged in:      Welcome, Krishna  [Logout]
```

### 7. Real-world Use Case
Login state in the navbar, shopping cart item count (`session.get("cart_count", 0)`), remembering a user's last-viewed page or preferred language.

### 8. Common Mistakes
| Mistake | Problem | Fix |
|---|---|---|
| Using `session["key"]` without checking existence first | `KeyError`/`UndefinedError` if key was never set | Use `session.get("key")` or `session.get("key", default_value)` |
| Storing large or sensitive data (passwords, full objects) in `session` | Session cookies have a size limit and are visible/decodable client-side (though signed, not encrypted, by default) | Store only small identifiers (like a user ID), fetch full details from the database each request |
| Forgetting `app.secret_key` | Flask raises a `RuntimeError` — sessions require a secret key to sign the cookie | Always set `app.secret_key` |

### 9. Practice Question
Extend the login-aware navbar to also show a "Cart (3 items)" link only when `session.get("cart_count")` is greater than 0.

---

# PART 18 — Flash Messages
**Level: Intermediate**

### 1. Topic Name
Flask flash messages + `get_flashed_messages()`

### 2. What is it?
"Flashing" lets you queue a one-time message in Python (e.g. "Login successful!") that survives exactly one redirect, to be displayed once on the *next* page the user sees, then automatically discarded.

### 3. Syntax
```python
flash("Login successful!")
flash("Invalid password!", "error")
```
```jinja2
{% with messages = get_flashed_messages() %}
    {% for message in messages %}
        <p>{{ message }}</p>
    {% endfor %}
{% endwith %}
```

### 4. Flask Example — with categories
```python
# app.py
from flask import Flask, render_template, flash, redirect, url_for, request

app = Flask(__name__)
app.secret_key = "replace-with-a-real-secret-key"

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    if username == "krishna":
        flash("Login successful!", "success")
        return redirect(url_for("home"))
    else:
        flash("Invalid username!", "error")
        return redirect(url_for("home"))

@app.route("/")
def home():
    return render_template("home.html")
```
```jinja2
<!-- templates/home.html -->
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
            <div class="alert alert-{{ category }}">{{ message }}</div>
        {% endfor %}
    {% endif %}
{% endwith %}
```

### 5. Line-by-line Explanation
- `flash("Login successful!", "success")` in Python doesn't display anything itself — it just pushes `("success", "Login successful!")` into a temporary queue stored in the session, to be picked up on the *very next* request/page render.
- `{% with messages = get_flashed_messages(with_categories=true) %}` — `get_flashed_messages()` retrieves (and simultaneously **clears**) that queue. `with_categories=true` changes the return shape from a flat list of message strings into a list of `(category, message)` tuples, so you can style errors differently from success messages.
- `{% with ... %}...{% endwith %}` creates a small scoped block where `messages` exists only within it — this is a minor scoping convenience (though in modern Jinja2, `{% set %}` at the top of the block works almost as well); the classic Flask docs pattern uses `with` specifically to avoid calling `get_flashed_messages()` more than once (each call clears the queue, so calling it twice would silently lose the messages on the second call).
- `class="alert alert-{{ category }}"` dynamically builds a CSS class name like `alert-success` or `alert-error`, letting your stylesheet color-code each category differently (green for success, red for error) without any extra template logic.

### 6. Expected Output
```html
<div class="alert alert-success">Login successful!</div>
```
(shown once, then gone on the next page load/refresh)

### 7. Real-world Use Case
"Item added to cart," "Profile updated successfully," "Invalid credentials, please try again" — any one-time notification tied to a redirect after a form submission (the classic Post/Redirect/Get pattern).

### 8. Common Mistakes
| Mistake | Problem | Fix |
|---|---|---|
| Calling `get_flashed_messages()` more than once in the same page | Second call gets an empty list — messages are consumed on first read | Store the result once (`{% with %}` or `{% set %}`), reuse the variable |
| Forgetting `app.secret_key` | Flashing silently fails (relies on sessions, which require a secret key) | Set `app.secret_key` |
| Not checking `with_categories=true` when you actually want categories | You'd get plain strings, not `(category, message)` tuples, and unpacking would fail | Match your Python `flash()` category usage with the matching template call |

### 9. Practice Question
Add a `"warning"` category flash message for "Session about to expire," and render it with a yellow-styled `alert-warning` div alongside the existing success/error handling.

---

# PART 19 — Whitespace Control
**Level: Beginner–Intermediate**

### 1. Topic Name
Whitespace control — `{%- ... -%}`

### 2. What is it?
By default, Jinja2 tags leave behind the line breaks and indentation surrounding them in your template source, which can produce HTML output with extra blank lines or stray spaces. Adding a `-` right next to a tag's `{%`/`%}` (or `{{`/`}}`) tells Jinja2 to strip whitespace on that side.

### 3. Why do we need it?
Extra blank lines in generated HTML are usually harmless visually (browsers collapse whitespace), but they can bloat page size slightly and make "View Source" messy — and in rare cases (like inside a `<pre>` tag, or when building minified output, or generating non-HTML text like emails/CSV), stray whitespace actually *does* matter and needs to be controlled.

### 4. Syntax
```jinja2
{%- if condition -%}   <!-- strips whitespace both before and after this tag -->
{%- if condition %}     <!-- strips only before -->
{% if condition -%}     <!-- strips only after -->
```

### 5. Simple Example
```jinja2
<ul>
{% for x in [1,2,3] %}
    <li>{{ x }}</li>
{% endfor %}
</ul>
```
Without control, this produces extra blank lines between `<ul>` and the first `<li>` (because the newline after `{% for %}` is preserved literally). Adding `-`:
```jinja2
<ul>
{%- for x in [1,2,3] %}
    <li>{{ x }}</li>
{%- endfor %}
</ul>
```
tightens up the output by trimming the whitespace immediately adjacent to those tags.

### 6. Flask Example
```jinja2
<!-- generating a comma-separated list with no stray spaces -->
<p>Tags:
{%- for tag in tags %} {{ tag }}{% if not loop.last %},{% endif %}
{%- endfor -%}
</p>
```

### 7. Line-by-line Explanation
- `{%- for tag in tags %}` — the `-` right after `{%` strips any whitespace (including the newline) that appears *immediately before* this tag in the source file.
- `{%- endfor -%}` — both sides trimmed, cleaning up before *and* after the closing tag.
- This doesn't change the *data* being looped — it only affects incidental whitespace coming from how you formatted the template file itself.

### 8. Expected Output
Clean, single-line output like `Tags: python, flask, sql` instead of output littered with extra line breaks and indentation from the source template.

### 9. Real-world Use Case
Generating non-HTML text output from templates (plain-text emails, CSV rows, config files) where whitespace is meaningful, or fine-tuning tightly-styled inline HTML elements where an unwanted stray space would visibly break layout (e.g. inline `<span>` elements next to each other).

### 10. Common Mistakes
| Mistake | Problem | Fix |
|---|---|---|
| Overusing `-` everywhere "just in case" | Output becomes one unreadable long line, harder to debug | Only add whitespace control where it visibly matters |
| Expecting `-` to strip whitespace *inside* the tag's own content | It only affects whitespace *outside*, adjacent to the tag | Don't confuse it with trimming variable values — use the `trim` filter for that |

### 11. Practice Question
Take the "Simple Example" for-loop above and add whitespace control so the generated `<ul>` has zero blank lines between `<ul>` and the first `<li>` when viewed in "View Source."

---
# PART 20 — Autoescaping and Security ⭐⭐⭐ Very Important
**Level: Advanced**

### 1. Topic Name
Autoescaping, XSS, and the `|safe` filter

### 2. What is it?
**Autoescaping** means Jinja2 automatically converts special HTML characters (`<`, `>`, `&`, `"`, `'`) in any value you print with `{{ }}` into their "escaped" HTML-entity equivalents (`&lt;`, `&gt;`, `&amp;`, etc.) *before* inserting them into the page. Flask turns this on by default for `.html` templates.

### 3. Why do we need it?
Imagine a comment box where a user types: `<script>alert('hacked')</script>`. If you printed that text into your HTML **without** escaping, the browser would treat it as *real HTML/JavaScript* and actually execute that script for every visitor who views the page — a classic attack called **Cross-Site Scripting (XSS)**. Autoescaping neutralizes this by converting `<script>` into the harmless text `&lt;script&gt;`, which the browser displays as plain visible text instead of running it as code.

### 4. Syntax — the dangerous escape hatch
```jinja2
{{ user_input }}          <!-- SAFE: autoescaped by default -->
{{ user_input|safe }}     <!-- DANGEROUS: tells Jinja2 "trust this, don't escape it" -->
```

### 5. Simple Example
```python
comment = "<b>Nice post!</b> <script>alert('hacked')</script>"
```
```jinja2
{{ comment }}
<!-- Rendered in browser as literal text: -->
<!-- <b>Nice post!</b> <script>alert('hacked')</script> -->
<!-- (no bold text, no alert popup — it's just displayed as plain text) -->

{{ comment|safe }}
<!-- Rendered as ACTUAL HTML: -->
<!-- Bold "Nice post!" appears, AND the alert('hacked') script actually runs! -->
```

### 6. Flask Example — the wrong way vs the right way
```python
# app.py — DO NOT do this with untrusted input
@app.route("/comment", methods=["POST"])
def comment():
    text = request.form.get("text")   # comes directly from a user, untrusted!
    return render_template("show_comment.html", text=text)
```
```jinja2
<!-- templates/show_comment.html — DANGEROUS -->
<p>{{ text|safe }}</p>   <!-- any user can now inject a live <script> into your page -->
```
```jinja2
<!-- templates/show_comment.html — SAFE (the default, do nothing extra) -->
<p>{{ text }}</p>   <!-- autoescaping neutralizes any HTML/JS the user typed -->
```

### 7. Line-by-line Explanation
- `{{ text }}` alone is already safe — Flask's Jinja2 environment has `autoescape=True` configured for `.html`/`.htm`/`.xml` templates by default, so **you don't need to do anything special** to be protected; the danger only appears when you *opt out* of that protection.
- `|safe` explicitly tells Jinja2: "I promise this string is already trustworthy HTML, please print it raw, don't escape it." This is meant for content **you** generated in Python (e.g., HTML you built yourself from a trusted template/markdown converter), never for raw user-typed input.
- The correct, safe pattern for genuinely needing to render user-provided *rich text* (e.g., a blog post editor) is to **sanitize** it server-side first, using a dedicated library (like `bleach`) that strips dangerous tags/attributes while allowing a safe whitelist (`<b>`, `<i>`, `<p>`), and *then* mark the sanitized result `|safe` — never mark raw, unprocessed user input as `|safe`.

### 8. Expected Output
With plain `{{ text }}`: the malicious script is displayed as harmless visible text, never executes.
With `{{ text|safe }}` on unsanitized input: the script actually runs in every visitor's browser — a real, exploitable vulnerability.

### `|safe` vs normal output

| | `{{ value }}` (default) | `{{ value|safe }}` |
|---|---|---|
| HTML special characters | Escaped (`<` becomes `&lt;`) | Printed as-is, raw |
| Safe for user-supplied text? | Yes, always | No — never, unless separately sanitized |
| When to use | Every normal variable print | Only for HTML you generated/trust yourself (e.g. output of a Markdown-to-HTML converter you control) |

### 9. Real-world Use Case
Every form field, comment box, username display, search box echo — anywhere user-typed text reaches the page — relies on default autoescaping to prevent XSS. `|safe` is reserved for narrow, deliberate cases like rendering pre-sanitized rich text or HTML snippets your own backend built.

### 10. Common Mistakes
| Mistake | Problem | Fix |
|---|---|---|
| Using `|safe` on any field that came from `request.form`/`request.args`/a database record originally sourced from user input | Opens a direct XSS vulnerability | Never use `|safe` on raw user input; sanitize first if rich HTML is genuinely needed |
| Assuming autoescaping protects JavaScript contexts too (e.g. inserting a variable directly into a `<script>` block) | Autoescaping is HTML-context-aware, not JS-aware — injecting into inline `<script>` can still be dangerous | Avoid injecting user data directly into `<script>` blocks; use `tojson` filter or pass data via safe attributes instead |
| Turning off autoescaping globally "to make things easier" | Removes protection for the *entire* app, not just one field | Never disable autoescaping app-wide; handle the rare needed case locally with `|safe` on sanitized content only |

### 11. Practice Question
Given `bio = "<i>I love Python</i><script>stealCookies()</script>"`, show what `{{ bio }}` displays vs what `{{ bio|safe }}` would do, and explain in one sentence why the second is dangerous here.

---
# PART 21 — Custom Filters
**Level: Advanced**

### 1. Topic Name
Registering your own Jinja2 filters in Flask

### 2. What is it?
A custom filter is a normal Python function you write and then "register" with Flask, after which it becomes usable inside templates with the exact same `|filter_name` syntax as built-in filters like `|upper`.

### 3. Why do we need it?
Built-in filters cover generic needs, but real apps have domain-specific formatting: currency symbols, custom date formats, converting a status code into a human label. Rather than repeating that formatting logic (or a macro) in every template, a custom filter centralizes it in one Python function.

### 4. Syntax
```python
@app.template_filter("currency")
def currency(value):
    return f"₹{value:.2f}"
```
```jinja2
{{ price|currency }}
```

### 5. Simple Example
```python
# app.py
@app.template_filter("shout")
def shout(text):
    return text.upper() + "!!!"
```
```jinja2
{{ "hello"|shout }}   <!-- HELLO!!! -->
```

### 6. Flask Example
```python
# app.py
from flask import Flask, render_template

app = Flask(__name__)

@app.template_filter("currency")
def currency(value):
    return f"₹{value:,.2f}"

@app.route("/checkout")
def checkout():
    total = 1234.5
    return render_template("checkout.html", total=total)
```
```jinja2
<!-- templates/checkout.html -->
<p>Total: {{ total|currency }}</p>
```

### 7. Line-by-line Explanation
- `@app.template_filter("currency")` is a **decorator** — it takes the plain Python function `currency` defined right below it and registers it into Flask's Jinja2 environment under the name `"currency"`. If you omit the string argument (`@app.template_filter()`), Flask uses the function's own name (`currency`) as the filter name automatically.
- Inside the function, `value` is a completely ordinary Python parameter — whatever gets piped in from the template (`total`, in this case) arrives here as a normal Python value, and you can use any Python logic/formatting (`f"₹{value:,.2f}"` uses an f-string with comma thousands-separators and 2 decimal places) exactly as you would anywhere else in Python.
- `{{ total|currency }}` — Jinja2 sees `|currency`, looks it up in its filter registry, finds your registered function, and calls it as `currency(total)`, printing whatever string it returns.

### 8. Expected Output
```
Total: ₹1,234.50
```

### 9. Real-world Use Case
Currency formatting, relative time ("2 hours ago"), converting a numeric grade into a letter grade, truncating long text with an ellipsis for card previews, formatting phone numbers.

### 10. Common Mistakes
| Mistake | Problem | Fix |
|---|---|---|
| Forgetting to return a value from the filter function | Filter prints "None" everywhere it's used | Always `return` the transformed value |
| Registering the same filter name twice | The second registration silently overwrites the first | Keep filter names unique and centralized in one place |
| Putting complex, error-prone logic in a filter with no error handling | One bad value (e.g. `None` passed to `currency`) crashes the whole page render | Add basic guards (`if value is None: return "-"`) inside the filter |

### 11. Practice Question
Write and register a custom filter `truncate_words(text, limit=10)` that shows only the first `limit` words of a string followed by `"..."` if it was cut off, then use it on a blog post preview.

---

# PART 22 — Custom Global Functions
**Level: Advanced**

### 1. Topic Name
`@app.template_global()` — custom functions callable inside templates

### 2. What is it?
A template global is a Python function made available for direct **calling** inside any template — `{{ function_name() }}` — as opposed to a filter, which is always applied *to* a value with `|`.

### 3. Why do we need it?
Some values aren't "transformations of an existing variable" (which is what filters are for) — they're standalone computations you want available anywhere without explicitly passing them through every single `render_template()` call. A global function fills that gap.

### 4. Syntax
```python
@app.template_global()
def get_current_year():
    return 2026
```
```jinja2
{{ get_current_year() }}
```

### 5. Simple Example
```python
@app.template_global()
def add(a, b):
    return a + b
```
```jinja2
{{ add(2, 3) }}   <!-- 5 -->
```

### 6. Flask Example
```python
# app.py
import datetime

@app.template_global()
def get_current_year():
    return datetime.datetime.now().year
```
```jinja2
<!-- templates/base.html -->
<footer>
    <p>&copy; {{ get_current_year() }} My Site. All rights reserved.</p>
</footer>
```

### 7. Line-by-line Explanation
- `@app.template_global()` registers the function into Jinja2's **global namespace**, meaning it's callable from *every* template in the project without needing to be passed via `render_template()` on each route — unlike a normal variable passed as `render_template("page.html", year=2026)`, which is only available in that one specific render call.
- `{{ get_current_year() }}` — note the parentheses: this is a genuine **function call** happening at render time, computing the year fresh every time the page loads, unlike a static variable that would need updating manually every January.

### Filters vs Globals — quick distinction
| | Filter | Global function |
|---|---|---|
| Syntax | `{{ value|my_filter }}` | `{{ my_function() }}` |
| Purpose | Transform an *existing* value | Compute/produce a *new* value from scratch |
| Needs an input piped in? | Yes, always operates on something | No, can take its own arguments or none at all |

### 8. Expected Output
```
© 2026 My Site. All rights reserved.
```
(automatically correct every year, with zero manual updates)

### 9. Real-world Use Case
Copyright year in the footer, a "is this feature flag enabled?" check available across the whole site, small utility calculations (like `add`) reused across many unrelated templates.

### 10. Common Mistakes
| Mistake | Problem | Fix |
|---|---|---|
| Forgetting the parentheses when calling it | `{{ get_current_year }}` prints the function object's repr, not its result | Always call it with `()` |
| Using a global function for something that's really a per-request/per-user value (should come from `render_template` context instead) | Global functions can't easily access route-specific data unless passed as arguments | Pass request-specific data as function arguments, or use a context processor (Part 23) for automatic per-request variables |

### 11. Practice Question
Write a `@app.template_global()` function `is_weekend()` that returns `True`/`False` based on today's day, and use it to show a "🎉 Happy Weekend!" banner conditionally in a template.

---

# PART 23 — Context Processors
**Level: Advanced**

### 1. Topic Name
`@app.context_processor`

### 2. What is it?
A context processor is a Python function that returns a **dictionary of variables** which Flask automatically injects into the context of **every** template render — you never need to pass these variables manually in any individual `render_template()` call.

### 3. Why do we need it?
Some data (the app's name, the logged-in user's display name, the current year) is needed on almost *every* page — the navbar shows the app name, the footer shows the year, every page might show "Hi, {{ current_user }}". Repeating `render_template("x.html", app_name="...", current_user="...", year=...)` in every single route is tedious and error-prone (forget it once, and that page's navbar breaks). A context processor solves this once, centrally.

### 4. Syntax
```python
@app.context_processor
def inject_user():
    return {"app_name": "Student Management System"}
```
```jinja2
{{ app_name }}
```

### 5. Simple Example
```python
@app.context_processor
def inject_globals():
    return {"site_name": "MySite", "year": 2026}
```
```jinja2
<title>{{ site_name }}</title>
<footer>&copy; {{ year }}</footer>
```
Both `site_name` and `year` are now usable in *every* template, on every route, without any route passing them explicitly.

### 6. Flask Example
```python
# app.py
from flask import Flask, render_template, session

app = Flask(__name__)
app.secret_key = "dev"

@app.context_processor
def inject_app_context():
    return {
        "app_name": "Student Management System",
        "current_user": session.get("username", "Guest"),
    }

@app.route("/")
def home():
    return render_template("home.html")   # note: no app_name/current_user passed here!

@app.route("/about")
def about():
    return render_template("about.html")  # yet both are still available here too
```
```jinja2
<!-- templates/base.html -->
<title>{{ app_name }}</title>
<p>Logged in as: {{ current_user }}</p>
```

### 7. Line-by-line Explanation
- `@app.context_processor` registers `inject_app_context` to run **automatically, right before every single template render**, no matter which route triggered it.
- The function returns a plain Python `dict` — Flask merges this dict into the context of whatever template is about to render, as if you'd typed those key-value pairs directly into that route's `render_template(...)` call.
- Notice neither `home()` nor `about()` explicitly passes `app_name` or `current_user` — yet both variables are fully available inside `base.html` regardless of which route rendered it. This is the entire point: **write once, available everywhere.**
- `session.get("username", "Guest")` shows the context processor can contain real logic too (not just static values) — it re-evaluates on every request, so it correctly reflects the *current* session state each time.

### Passing variables via `render_template()` vs context processor
| | `render_template("x.html", var=val)` | `@app.context_processor` |
|---|---|---|
| Scope | Only that one render call | Automatically every template, every route |
| Best for | Data specific to one page (a single student's details) | Data needed almost everywhere (app name, logged-in user, current year) |
| Risk of forgetting | High if repeated across many routes | None — set up once |

### 8. Expected Output
Every page — home, about, and any future page — automatically shows the correct app name and current logged-in user in its title/navbar, with zero repeated code in the route functions.

### 9. Real-world Use Case
`app_name`, `current_user`, `current_year`, feature flags, global site settings, cart item count in an e-commerce navbar — any value that's conceptually "global" to the whole site rather than specific to one page.

### 10. Common Mistakes
| Mistake | Problem | Fix |
|---|---|---|
| Returning something that isn't a dict | `TypeError` at render time | Always `return {...}` |
| Putting expensive operations (slow DB queries) in a context processor | Slows down *every single page* on the site, since it runs on every render | Keep context processors lightweight; cache expensive lookups |
| Naming a context processor variable the same as a variable explicitly passed via `render_template()` | The explicitly passed one silently overrides the context processor's value for that specific page — can be confusing if unintentional | Keep names distinct, or use this override behavior deliberately when you want a page-specific exception |

### 11. Practice Question
Add a context processor that injects `total_students = len(students)` (using a module-level sample list) into every template, and display it in the footer of `base.html`.

---

# PART 24 — Calling Python Functions / Methods
**Level: Advanced**

### 1. Topic Name
Method calls inside templates, and where to draw the logic line

### 2. What is it?
Jinja2 allows calling certain Python **methods** directly on values inside templates, e.g. `{{ name.upper() }}` — because Jinja2's expression evaluator supports basic attribute/method access, not just filters.

### 3. Why do we need to understand this?
It's tempting to reach for `.upper()`, `.strip()`, `.split()` etc. directly since they "just work" — but knowing *when this is appropriate* versus when it crosses into business logic that belongs in Python is an important judgment call for writing maintainable Flask apps.

### 4. Syntax
```jinja2
{{ name.upper() }}
{{ text.split(",") }}
{{ "  hi  ".strip() }}
```

### 5. Simple Example
```python
name = "krishna"
```
```jinja2
{{ name.upper() }}   <!-- KRISHNA -->
```

### 6. Flask Example
```jinja2
{{ student.name.upper() }}
{{ ", ".join(student.skills) }}
```

### 7. Line-by-line Explanation
- `{{ name.upper() }}` — Jinja2 first resolves `name` (a Python string), then sees `.upper` — since strings genuinely have an `upper` method, and it's callable (note the `()`), Jinja2 invokes it exactly like Python would, returning the uppercase string.
- This works because Jinja2's sandbox permits calling methods on objects that don't have obviously dangerous side effects — but it's still Python method-calling machinery under the hood, not special Jinja2 syntax.

### Filters vs direct method calls — which should you prefer?
| | `{{ name|upper }}` | `{{ name.upper() }}` |
|---|---|---|
| Works if `name` might be `None`/undefined | Can chain safely: `{{ name|default("")|upper }}` | Crashes immediately — `None` has no `.upper()` method |
| Readability in a template-heavy codebase | Consistent with Jinja2's own style (`|filter` conventions), preferred by most Flask style guides | Looks like raw Python leaking into HTML |
| **General rule** | **Prefer filters** for simple transformations — safer and more idiomatic | Acceptable for very simple, safe method calls, but avoid habitually reaching for it |

### Where to draw the line — keep business logic in Python
```jinja2
<!-- AVOID: business logic embedded in the template -->
{% if student.marks >= 90 and student.attendance >= 75 and not student.has_pending_fees %}
    <p>Eligible for scholarship</p>
{% endif %}
```
```python
# PREFER: compute the decision in Flask, pass a simple flag
@app.route("/student/<int:id>")
def student_detail(id):
    student = get_student(id)
    is_scholarship_eligible = (
        student.marks >= 90 and student.attendance >= 75 and not student.has_pending_fees
    )
    return render_template("detail.html", student=student, is_eligible=is_scholarship_eligible)
```
```jinja2
{% if is_eligible %}
    <p>Eligible for scholarship</p>
{% endif %}
```
The second version is far easier to unit-test (you can test `is_scholarship_eligible`'s logic directly in Python, without rendering any HTML at all), and keeps the template purely about *display*, not *decisions*.

### 8. Expected Output
```
KRISHNA
Python, Flask, ML
```

### 9. Real-world Use Case
Simple, safe, side-effect-free method calls (`.upper()`, `.strip()`, `.split()`) are fine directly in templates for quick display tweaks. Anything resembling a business rule, calculation involving multiple fields, or database access should always live in Python.

### 10. Common Mistakes
| Mistake | Problem | Fix |
|---|---|---|
| Calling `.upper()` on a value that might be `None` | Crashes the page render | Guard with `is none`/`default` first, or prefer the `|upper` filter with `|default("")` chained before it |
| Embedding multi-condition business rules directly in `{% if %}` | Hard to test, hard to read, logic scattered across HTML files | Compute the boolean/value in Python, pass a simple flag/result to the template |
| Calling methods that have side effects (modifying data) from a template | Templates should be read-only/display-only; side effects during rendering are unpredictable and hard to trace | Never call mutating methods from templates — only read-only, safe operations |

### 11. Practice Question
Rewrite this template snippet to move the business logic into Flask instead:
```jinja2
{% if (student.marks / student.max_marks) * 100 >= 40 %}
    <p>Result: Pass</p>
{% else %}
    <p>Result: Fail</p>
{% endif %}
```

---
# PART 25 — Jinja2 Template Debugging
**Level: Intermediate–Advanced**

### 1. Topic Name
Reading and fixing common Jinja2/Flask errors

### 2. What is it?
When something goes wrong in a template, Flask (in debug mode) shows a detailed error page with a traceback pointing to the exact template line. Learning to read these quickly saves huge amounts of time.

### 3. Common Errors Reference

| Error | Typical Cause | How to Fix |
|---|---|---|
| `UndefinedError: 'x' is undefined` | You used `{{ x }}` but never passed `x` in `render_template()`, or misspelled the variable name | Check the exact spelling matches between Python and template; use `is defined` or `default` for optional values |
| `TemplateNotFound: page.html` | Wrong filename, wrong folder, or file simply doesn't exist in `templates/` | Verify path is relative to `templates/` root; check for typos and correct extension |
| `TemplateSyntaxError: Unexpected end of template` | Missing `{% endif %}`, `{% endfor %}`, `{% endblock %}`, or `{% endmacro %}` | Count opening tags vs closing tags; every opener needs a matching closer |
| `TemplateSyntaxError: expected token 'end of print statement'` | Typo inside `{{ }}`, often a stray bracket or quote mismatch | Carefully re-check the expression syntax inside the braces |
| `BuildError: Could not build url for endpoint 'x'` | `url_for('x')` references a function name that doesn't exist or is misspelled | Match the exact Python function name under `@app.route` |
| `jinja2.exceptions.TemplateAssertionError: No filter named 'x'` | Typo in filter name, or a custom filter that was never registered | Check spelling; confirm `@app.template_filter` ran before the app started handling requests |

### 4. Example — diagnosing an `UndefinedError`
```python
# app.py
@app.route("/profile")
def profile():
    return render_template("profile.html", name="Krishna")  # 'age' NOT passed
```
```jinja2
<!-- templates/profile.html -->
<p>{{ name }}</p>
<p>{{ age }}</p>   <!-- UndefinedError: 'age' is undefined -->
```
**Fix options:**
```jinja2
<p>{{ age|default("Not provided") }}</p>
<!-- OR -->
{% if age is defined %}<p>{{ age }}</p>{% endif %}
<!-- OR (best) — actually pass it from Flask: -->
```
```python
return render_template("profile.html", name="Krishna", age=None)
```

### 5. Example — diagnosing a `TemplateSyntaxError`
```jinja2
{% for student in students %}
    <p>{{ student.name }}</p>
<!-- forgot {% endfor %} here -->
```
Flask's error page will point to roughly the end of the file with `Unexpected end of template. Jinja was looking for the following tags: 'endfor'`. **Fix:** add the missing `{% endfor %}`.

### 6. Debugging checklist
1. Read the **exact** error type first (`UndefinedError` vs `TemplateSyntaxError` mean very different things).
2. Check the **line number** Flask points to in the traceback — it's usually exact.
3. For `UndefinedError` — check spelling and confirm you actually passed the variable in `render_template()`.
4. For `TemplateNotFound` — check the path is relative to `templates/`, and double-check the filename's case (Linux servers are case-sensitive even if your local machine isn't).
5. For syntax errors — count matching open/close tags; a missing `{% endif %}`/`{% endfor %}` is the most common cause by far.
6. Turn on Flask's debug mode during development (`app.run(debug=True)`) — it gives you an interactive traceback and reloads automatically on file changes.

### 7. Real-world Use Case
Every Flask developer hits these errors regularly, especially `UndefinedError` and mismatched `{% endif %}`/`{% endfor %}` — recognizing the pattern instantly instead of panicking saves a lot of debugging time.

### 8. Common Mistakes While Debugging
| Mistake | Problem | Fix |
|---|---|---|
| Running with `debug=False` while developing | Errors show only a generic "Internal Server Error" with no useful details | Use `app.run(debug=True)` locally (never in production) |
| Assuming the error is in Python when it's actually in the template (or vice versa) | Wastes time looking in the wrong file | The traceback names the exact file — read it carefully before guessing |

### 9. Practice Question
This template throws `UndefinedError: 'students' is undefined`. Find and fix the bug:
```python
@app.route("/list")
def student_list():
    all_students = ["Krishna", "Rahul"]
    return render_template("list.html", all_students=all_students)
```
```jinja2
{% for s in students %}
    <p>{{ s }}</p>
{% endfor %}
```

---

# PART 26 — Jinja2 Project Structure
**Level: Intermediate**

### 1. Topic Name
Organizing templates and static files in a real Flask project

### 2. Recommended structure
```text
project/
│
├── app.py
│
├── templates/
│   ├── base.html
│   ├── navbar.html
│   ├── footer.html
│   │
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   │
│   ├── students/
│   │   ├── list.html
│   │   ├── add.html
│   │   └── edit.html
│   │
│   └── errors/
│       ├── 404.html
│       └── 500.html
│
└── static/
    ├── css/
    │   └── style.css
    ├── js/
    │   └── main.js
    └── images/
```

### 3. Why this matters
- **Subfolders group related pages** (`auth/`, `students/`) so the project stays navigable as it grows — a flat `templates/` folder with 40 files quickly becomes unmanageable.
- Referencing a subfolder template is simple: `render_template("students/list.html")` — Jinja2 treats the path exactly like a filesystem path relative to `templates/`.
- **A dedicated `errors/` folder** keeps custom error pages (404 Not Found, 500 Server Error) organized and easy to find, registered in Flask like:
```python
@app.errorhandler(404)
def not_found(e):
    return render_template("errors/404.html"), 404
```
- **`static/`** is a completely separate top-level folder (not inside `templates/`) because Flask serves it differently — directly as files via the `/static/...` URL, referenced with `url_for('static', filename='css/style.css')` (Part 15), whereas everything in `templates/` is *processed* by Jinja2 first, never served directly.
- Shared fragments (`navbar.html`, `footer.html`) sit at the **top level** of `templates/` since they're used across every section, not tied to one feature area.

### 4. Real-world Use Case
This exact pattern — feature-based subfolders, a shared base/navbar/footer, a dedicated errors folder, a separate static folder — is the de facto standard structure for small-to-medium Flask applications, including the mini project in Part 27.

### 5. Common Mistakes
| Mistake | Problem | Fix |
|---|---|---|
| Putting CSS/JS files inside `templates/` | Flask won't serve them correctly — Jinja2 tries to process them as templates | Always put static assets in `static/`, never `templates/` |
| One giant flat `templates/` folder with no subfolders as the project grows | Hard to find files, frequent naming collisions | Group by feature area once you exceed ~8–10 templates |
| Forgetting the `errors/` templates need `.errorhandler` registration in `app.py` to actually be used | Flask shows its default error pages instead of your custom ones | Register `@app.errorhandler(404)` etc. explicitly |

### 6. Practice Question
Reorganize a flat `templates/` folder containing `login.html`, `register.html`, `product_list.html`, `product_add.html`, `404.html` into the grouped structure shown above, and write the two `render_template()` calls needed for `login.html` and `product_list.html` with their new paths.

---
# PART 27 — Complete Mini Project: Student Management System
**Level: Bringing everything together**

This project uses **in-memory sample data** (a Python list of dicts) — no database — so you can focus entirely on Jinja2/Flask concepts. Every concept from Parts 1–26 is used somewhere below.

### 1. Project Structure
```text
project/
│
├── app.py
│
├── templates/
│   ├── base.html
│   ├── navbar.html
│   ├── footer.html
│   ├── macros.html
│   ├── home.html
│   ├── students/
│   │   ├── list.html
│   │   ├── detail.html
│   │   └── add.html
│   └── errors/
│       └── 404.html
│
└── static/
    └── css/
        └── style.css
```

### 2. `app.py`
```python
# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-in-production"

# ---- Sample "database" (in-memory) ----
students = [
    {"id": 1, "name": "Krishna", "marks": 85, "subjects": ["Python", "ML"]},
    {"id": 2, "name": "Rahul", "marks": 65, "subjects": ["Java", "DSA"]},
    {"id": 3, "name": "Anil", "marks": 40, "subjects": ["Python", "SQL"]},
]
next_id = 4

# ---- Custom filter ----
@app.template_filter("grade")
def grade_filter(marks):
    if marks >= 90:
        return "A"
    elif marks >= 75:
        return "B"
    elif marks >= 50:
        return "C"
    else:
        return "Fail"

# ---- Context processor: runs before EVERY template ----
@app.context_processor
def inject_globals():
    return {
        "app_name": "Student Management System",
        "total_students": len(students),
        "is_admin": session.get("is_admin", False),
    }

# ---- Routes ----
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/students")
def student_list():
    query = request.args.get("q", "")
    if query:
        filtered = [s for s in students if query.lower() in s["name"].lower()]
    else:
        filtered = students
    return render_template("students/list.html", students=filtered, query=query)

@app.route("/students/<int:id>")
def student_detail(id):
    student = next((s for s in students if s["id"] == id), None)
    if student is None:
        return render_template("errors/404.html"), 404
    return render_template("students/detail.html", student=student)

@app.route("/students/add", methods=["GET", "POST"])
def add_student():
    global next_id
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        marks = request.form.get("marks", "0")
        if not name:
            flash("Name is required!", "error")
            return redirect(url_for("add_student"))
        students.append({
            "id": next_id,
            "name": name,
            "marks": int(marks),
            "subjects": [],
        })
        next_id += 1
        flash(f"Student '{name}' added successfully!", "success")
        return redirect(url_for("student_list"))
    return render_template("students/add.html")

@app.route("/students/delete/<int:id>", methods=["POST"])
def delete_student(id):
    global students
    students = [s for s in students if s["id"] != id]
    flash("Student removed.", "success")
    return redirect(url_for("student_list"))

@app.route("/admin/login")
def admin_login():
    session["is_admin"] = True
    flash("Admin mode enabled.", "success")
    return redirect(url_for("student_list"))

@app.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    flash("Admin mode disabled.", "success")
    return redirect(url_for("student_list"))

@app.errorhandler(404)
def not_found(e):
    return render_template("errors/404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
```

### 3. `templates/base.html`
```jinja2
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{{ app_name }}{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    {% include "navbar.html" %}

    <main class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        {% block content %}{% endblock %}
    </main>

    {% include "footer.html" %}
</body>
</html>
```

### 4. `templates/navbar.html`
```jinja2
<nav>
    <a href="{{ url_for('home') }}">Home</a> |
    <a href="{{ url_for('student_list') }}">Students</a> |
    {% if is_admin %}
        <span>Admin Mode ✅</span>
        <a href="{{ url_for('admin_logout') }}">Logout</a>
    {% else %}
        <a href="{{ url_for('admin_login') }}">Admin Login</a>
    {% endif %}
</nav>
```

### 5. `templates/footer.html`
```jinja2
<footer>
    <p>&copy; {{ app_name }} — {{ total_students }} students registered.</p>
</footer>
```

### 6. `templates/macros.html`
```jinja2
{% macro student_card(student) %}
    <div class="card">
        <h3>{{ student.name }}</h3>
        <p>Marks: {{ student.marks }} ({{ student.marks|grade }})</p>
        <a href="{{ url_for('student_detail', id=student.id) }}">View</a>
        {% if is_admin %}
            <form method="POST" action="{{ url_for('delete_student', id=student.id) }}"
                  style="display:inline">
                <button type="submit">Delete</button>
            </form>
        {% endif %}
    </div>
{% endmacro %}
```

### 7. `templates/home.html`
```jinja2
{% extends "base.html" %}
{% block title %}Home — {{ app_name }}{% endblock %}
{% block content %}
    <h1>Welcome to {{ app_name }}</h1>
    <p>We currently have {{ total_students }} students.</p>
    <a href="{{ url_for('student_list') }}">View All Students</a>
{% endblock %}
```

### 8. `templates/students/list.html`
```jinja2
{% extends "base.html" %}
{% from "macros.html" import student_card %}

{% block title %}Students — {{ app_name }}{% endblock %}

{% block content %}
    <h1>Student List</h1>

    <form method="GET">
        <input type="text" name="q" value="{{ query }}" placeholder="Search by name">
        <button type="submit">Search</button>
    </form>

    <a href="{{ url_for('add_student') }}">+ Add Student</a>

    <div class="card-grid">
        {% for student in students %}
            {{ student_card(student) }}
        {% else %}
            <p>No students found{% if query %} for "{{ query }}"{% endif %}.</p>
        {% endfor %}
    </div>

    <h2>Passing Students ({{ (students|selectattr("marks", "greaterthan", 49)|list)|length }})</h2>
    <ul>
    {% for s in students|selectattr("marks", "greaterthan", 49) %}
        <li>{{ loop.index }}. {{ s.name }} — {{ s.marks }} ({{ s.marks|grade }})</li>
    {% endfor %}
    </ul>
{% endblock %}
```

### 9. `templates/students/detail.html`
```jinja2
{% extends "base.html" %}
{% block title %}{{ student.name }} — {{ app_name }}{% endblock %}
{% block content %}
    <h1>{{ student.name }}</h1>
    <p>Marks: {{ student.marks }} — Grade: <strong>{{ student.marks|grade }}</strong></p>

    <h3>Subjects</h3>
    {% if student.subjects %}
        <ul>
        {% for subject in student.subjects %}
            <li>{{ subject }}</li>
        {% endfor %}
        </ul>
    {% else %}
        <p>No subjects added yet.</p>
    {% endif %}

    <a href="{{ url_for('student_list') }}">Back to list</a>
{% endblock %}
```

### 10. `templates/students/add.html`
```jinja2
{% extends "base.html" %}
{% block title %}Add Student — {{ app_name }}{% endblock %}
{% block content %}
    <h1>Add New Student</h1>
    <form method="POST">
        <label>Name</label>
        <input type="text" name="name" required>

        <label>Marks</label>
        <input type="number" name="marks" min="0" max="100" required>

        <button type="submit">Save</button>
    </form>
{% endblock %}
```

### 11. `templates/errors/404.html`
```jinja2
{% extends "base.html" %}
{% block title %}Not Found — {{ app_name }}{% endblock %}
{% block content %}
    <h1>404 — Page Not Found</h1>
    <p>The student or page you're looking for doesn't exist.</p>
    <a href="{{ url_for('home') }}">Go Home</a>
{% endblock %}
```

### 12. How everything connects
```text
Browser requests /students
        ↓
Flask route student_list() runs → builds/filters the `students` list
        ↓
render_template("students/list.html", students=filtered, query=query)
        ↓
Jinja2 sees {% extends "base.html" %} → loads base.html skeleton
        ↓
context_processor's inject_globals() ALSO merges in app_name, total_students, is_admin
        ↓
base.html includes navbar.html + footer.html (both use the injected globals + url_for)
        ↓
list.html's {% block content %} imports student_card macro, loops over students,
    calls the macro once per student, uses |grade custom filter and selectattr filtering
        ↓
Final combined HTML string returned to the browser
```

### 13. Expected Output (visiting `/students`)
A page with: a navbar (Home / Students / Admin Login), a search box, an "Add Student" link, one card per student (name, marks, grade, View link), and a "Passing Students" list below showing only those with marks > 49 — with admin-only "Delete" buttons appearing once you visit `/admin/login`.

### 14. Concepts used, mapped to this project
| Concept | Where it's used |
|---|---|
| Template inheritance | Every page extends `base.html` |
| `include` | `navbar.html`, `footer.html` |
| `macro` + import | `student_card` in `macros.html`, imported into `list.html` |
| Loops + `loop` variable | `loop.index` in the passing-students list |
| Loop `if` filtering + `else` | Search results loop with "No students found" fallback |
| Custom filter | `|grade` |
| `selectattr` | Filtering passing students |
| Context processor | `app_name`, `total_students`, `is_admin` on every page |
| `url_for()` | Every link and form action |
| `session` | `is_admin` flag |
| Flash messages | Add/delete confirmations, validation errors |
| Error handling | Custom `404.html` |
| `set`/expressions | Grade calculation via filter instead of inline logic (kept in Python, as recommended in Part 24) |

---
# PART 28 — Cheat Sheet + Full Practice Set

## Quick Cheat Sheet

### Syntax
```text
{{ value }}     → print an expression
{% stmt %}      → logic (if/for/set/block/etc), no output
{# comment #}   → invisible comment
{%- -%}         → strip surrounding whitespace
```

### Conditions
```text
{% if cond %} {% elif cond %} {% else %} {% endif %}
and / or / not / in / not in / is
```

### Loops
```text
{% for x in items %} ... {% else %} ... {% endfor %}
{% for x in items if condition %}
loop.index / loop.index0 / loop.first / loop.last / loop.length / loop.revindex
```

### Filters (piping — `value|filter`)
```text
upper lower capitalize title trim length default replace join
first last sort reverse unique list string int float round abs
min max sum map select selectattr reject rejectattr
```

### Tests (checking — `value is test`)
```text
defined undefined none boolean true false string number
integer float iterable mapping sequence sameas
```

### Template reuse
```text
{% extends "base.html" %}        → inherit page skeleton
{% block name %}...{% endblock %} → named override region
{% include "file.html" %}         → paste in a fragment
{% macro name(args) %}...{% endmacro %} → reusable HTML component
{% import "file.html" as ns %}    → namespace-style import
{% from "file.html" import name %} → direct import
```

### Variables
```text
{% set x = value %}
{% set ns = namespace(total=0) %}   → mutable value that survives loop scope
{% set block_var %}...{% endset %}   → capture rendered HTML into a variable
```

### Flask integration (auto-available inside templates)
```text
url_for('function_name', param=value)
url_for('static', filename='path')
request.method / request.path / request.args.get('key')
session['key'] / session.get('key')
get_flashed_messages(with_categories=true)
```

### Advanced Flask/Jinja2 registration (in app.py)
```python
@app.template_filter("name")     # custom filter → value|name
@app.template_global()            # custom global → name()
@app.context_processor            # returns dict merged into EVERY template
```

### Security
```text
{{ value }}        → autoescaped, SAFE for user input (default)
{{ value|safe }}   → raw HTML, DANGEROUS unless value is pre-sanitized
```

---

## Comparison Tables — Recap

| Comparison | Key Difference |
|---|---|
| `{{ }}` vs `{% %}` | `{{ }}` prints a value; `{% %}` runs logic/control-flow and prints nothing itself |
| `extends` vs `include` | `extends` = one page inherits a shared skeleton (blocks); `include` = paste in a reusable fragment (no blocks) |
| filter vs test | filter *transforms* a value (`value|upper`); test *checks* a condition (`value is defined`) |
| `render_template()` vs `redirect()` | `render_template()` returns rendered HTML directly as the response; `redirect()` sends the browser a new URL to request instead (used after POST actions, the Post/Redirect/Get pattern) |
| Python function vs Jinja2 macro | Python function runs server-side and returns any data type; macro runs during template rendering and always produces an HTML string |
| `session` vs `request` | `session` persists data *across multiple requests* for one user (cookie-backed); `request` represents only the *current* incoming request's data |
| passing variables vs context processor | Passing variables (`render_template(x=1)`) is scoped to one render call; a context processor injects variables into **every** template automatically |
| `|safe` vs normal output | Normal output is autoescaped (safe by default); `|safe` disables escaping (dangerous unless the content is already trusted/sanitized) |

---

## Recommended Learning Order

Given what you already know (routes, `render_template`, basic variables, basic Jinja2 syntax), study in this order:

1. **Part 2 — Working with Python Data** (foundation for everything else)
2. **Part 3 — Conditionals** and **Part 4 — Loops** (the two workhorses of every template)
3. **Part 5 — Loop filtering/else** (small but very practical extension of Part 4)
4. **Part 6 — Filters** (huge day-to-day productivity boost)
5. **Part 13 — Expressions/Operators** and **Part 14 — Tests** (deepen your `{% if %}` toolkit)
6. **Part 8 — Template Inheritance** ⭐ (the biggest structural concept — study this thoroughly)
7. **Part 9 — include** (natural follow-on from inheritance)
8. **Part 15 — url_for()** (should be used from this point onward in every exercise)
9. **Part 7 — select/selectattr/reject/rejectattr** (natural extension of filters, once comfortable)
10. **Part 10 & 11 — macro + importing macros** (reusable components, once inheritance feels natural)
11. **Part 12 — set** (including the `namespace()` gotcha)
12. **Part 16, 17, 18 — request, session, flash messages** (Flask-specific integration)
13. **Part 20 — Autoescaping & Security** ⭐ (critical — don't skip, even though it "feels" advanced)
14. **Part 19 — Whitespace control** (minor, learn whenever convenient)
15. **Part 21, 22, 23 — custom filters, globals, context processors** (once you're comfortable extending Flask itself)
16. **Part 24 — Calling Python methods / where logic belongs** (a mindset shift, useful once you've written a few real templates)
17. **Part 25, 26 — Debugging + project structure** (useful throughout, but crystallizes once you've made a few real mistakes)
18. **Part 27 — Mini project** (do this last, as a capstone that exercises everything above together)

---

## 20 Jinja2 / Flask-Templating Interview Questions

1. What is Jinja2, and how does Flask use it to render dynamic HTML?
2. What is the difference between `{{ }}`, `{% %}`, and `{# #}`?
3. How does Flask pass data from a Python route into a Jinja2 template?
4. What's the difference between `student["name"]` and `student.name`? When would only one of them work?
5. Explain what the `loop` variable is and name at least four of its attributes.
6. What does `{% for x in items %}...{% else %}...{% endfor %}` do, and when does the `else` branch execute?
7. What is a Jinja2 filter? Give three examples and explain filter chaining.
8. What's the difference between `select`/`reject` and `selectattr`/`rejectattr`?
9. Explain template inheritance: what do `{% extends %}` and `{% block %}` do together?
10. What's the difference between `{% extends %}` and `{% include %}`?
11. What is a Jinja2 macro, and how is it different from a Python function?
12. What's the difference between `{% import "x.html" as ns %}` and `{% from "x.html" import y %}`?
13. Why might `{% set total = total + x %}` fail to accumulate correctly inside a `{% for %}` loop, and how do you fix it?
14. What is the difference between a Jinja2 filter and a Jinja2 test?
15. What does `url_for()` do, and why is it preferred over hardcoding URLs?
16. What is autoescaping, and why is it important for security? What does `|safe` do, and when is it dangerous?
17. How would you register and use a custom Jinja2 filter in a Flask app?
18. What is a Flask context processor, and how does it differ from passing variables via `render_template()`?
19. How do Flask flash messages work end-to-end, from `flash()` in Python to display in the template?
20. What's the risk of putting complex business logic directly inside a Jinja2 template, and where should that logic live instead?

---

## 20 Practical Coding Exercises

1. Create a route that passes a list of 5 favorite movies and display them as a numbered list using `loop.index`.
2. Given a dict of `{"Python": 90, "Flask": 85, "SQL": 70}`, loop through it printing each subject and score.
3. Build a page that shows "Pass" or "Fail" for a list of student dicts, using `{% if %}` inside a loop.
4. Use `selectattr` to display only students with `marks >= 60` from a list of 6 students.
5. Write a template that joins a list of tags into a comma-separated string using `|join`, then uppercases the whole result.
6. Build a `base.html` with `title` and `content` blocks, then create three child pages that extend it.
7. Create a `card.html` partial and use `{% include %}` inside a loop to render one card per product.
8. Write a macro `render_alert(message, type="info")` and use it three times with different types.
9. Create `macros.html` with two macros and import both using `{% from ... import ... %}`.
10. Use `{% set %}` to compute a cart's line totals and grand total (careful with the loop-scoping gotcha from Part 12!).
11. Write a template line using the `~` operator to build a sentence combining a string and a number.
12. Use `{% if value is defined %}` to safely handle an optional `discount` variable.
13. Build a navbar where the currently active page's link gets an `active` CSS class using `request.path`.
14. Create a login/logout flow using `session`, showing different navbar content based on login state.
15. Implement flash messages with two categories (`success`, `error`) and style them differently.
16. Register a custom filter `days_ago(date)` that returns how many days ago a given date was.
17. Register a `@app.template_global()` function that returns the app's total number of registered users.
18. Add a context processor that injects `site_name` and `current_year` into every template.
19. Demonstrate the difference between `{{ user_input }}` and `{{ user_input|safe }}` using a sample string containing `<script>`.
20. Build the full Student Management System from Part 27 yourself, from scratch, without copying — then add a new feature: editing an existing student's marks.

---

## 10 Debugging Exercises

For each, identify the bug and fix it.

1. `TemplateNotFound: student.html` — but the file is actually named `students.html`.
2. `UndefinedError: 'user' is undefined` — route passes `render_template("profile.html", username="Krishna")` but template uses `{{ user }}`.
3. ```jinja2
   {% if marks >= 50 %}
       Pass
   ```
   (missing closing tag)
4. ```jinja2
   {% for student in students %}
       {{ student.name }}
   {% endif %}
   ```
   (wrong closing tag used)
5. `BuildError: Could not build url for endpoint 'student_page'` — but the route function is actually named `student_detail`.
6. ```jinja2
   {{ students|selectattr("marks", "greaterthan", 70) }}
   ```
   printed directly with `{{ }}` shows a strange generator-object repr instead of a list.
7. A custom filter `currency` was written in `app.py` but never decorated with `@app.template_filter`, so `{{ price|currency }}` throws `No filter named 'currency'`.
8. `{{ get_flashed_messages() }}` returns an empty list even though `flash("Saved!")` was just called — called twice on the same page.
9. `{% set total = 0 %}` followed by `{% for item in items %}{% set total = total + item.price %}{% endfor %}` prints `0` at the end instead of the real sum.
10. A `<script>` tag typed into a comment box is displayed as visible text instead of formatting nicely — the developer "fixed" it by adding `|safe`, and now a different user's comment injected a working alert popup. What went wrong, and what's the safe fix?

---

## Final Mini-Project Challenge

Extend the Part 27 **Student Management System** with:
1. An **edit student** route + template (`students/edit.html`) using a form pre-filled with the student's current data.
2. A custom filter `letter_grade` that's more granular than the existing `grade` filter (A+, A, B+, B, C, Fail).
3. A context-processor-injected `average_marks` (computed across all students) shown in the footer.
4. A `search` feature (already partially built in Part 27) extended to also filter by `subjects` using `selectattr`/`in`.
5. Flash-message-driven validation: reject marks outside 0–100 with a clear error message.
6. A custom `404.html` **and** a custom `500.html` error page.
7. Whitespace-controlled output for a "comma-separated subjects" line with zero stray spaces in the rendered HTML source.

Building this end-to-end — using inheritance, includes, macros, filters, tests, sessions, flashing, `url_for`, a context processor, and a custom filter all together — is the real test of whether these notes have "clicked." Good luck, Krishna!

---

*End of notes.*
