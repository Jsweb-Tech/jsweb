# Templating

JsWeb uses the [Jinja2](https://jinja.palletsprojects.com/) templating engine to render dynamic HTML. Jinja2 is a powerful and flexible templating language that allows you to embed logic and variables directly into your HTML files.

## Rendering Templates

To render a template, you can use the `render` function from the `jsweb.response` module.

```python
from jsweb.response import render

@app.route("/")
async def home(req):
    return render(req, "index.html", {"name": "World"})
```

In this example, we're rendering the `index.html` template and passing a context dictionary with a `name` variable. The `render` function will look for the `index.html` template in the `templates` folder of your project.

## Template Variables

You can use variables in your templates by enclosing them in double curly braces (`{{ ... }}`).

```html
<!-- templates/index.html -->
<h1>Hello, {{ name }}!</h1>
```

When you render this template, `{{ name }}` will be replaced with the value of the `name` variable from the context dictionary.

## Template Logic

Jinja2 also supports control structures like `if` statements and `for` loops.

### `if` Statements

```html
{% if user %}
  <p>Hello, {{ user.name }}!</p>
{% else %}
  <p>Please log in.</p>
{% endif %}
```

### `for` Loops

```html
<ul>
  {% for item in items %}
    <li>{{ item }}</li>
  {% endfor %}
</ul>
```

## Template Inheritance

Template inheritance allows you to build a base template with common elements and then extend it in other templates.

### `base.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    <div class="content">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

### `index.html`

```html
{% extends "base.html" %}

{% block title %}Home{% endblock %}

{% block content %}
    <h1>Welcome to my site!</h1>
{% endblock %}
```

## Custom Filters

You can add your own custom filters to the Jinja2 environment using the `@app.filter()` decorator.

```python
@app.filter("uppercase")
def uppercase_filter(s):
    return s.upper()
```

You can then use this filter in your templates:

```html
{{ "hello" | uppercase }}  <!-- Renders as "HELLO" -->
```
