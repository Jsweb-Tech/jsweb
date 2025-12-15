# Routing

Routing is the process of mapping URLs to the functions that handle them. In JsWeb, you can define routes using the `@app.route()` decorator.

## Basic Routing

Here's a simple example of how to define a route:

```python
from jsweb import JsWebApp
import config

app = JsWebApp(config=config)

@app.route("/")
async def home(req):
    return "Hello, World!"
```

In this example, we're mapping the root URL (`/`) to the `home` function. When a user visits the root of our site, the `home` function will be called, and the string "Hello, World!" will be returned to the user's browser.

## HTTP Methods

By default, a route only responds to `GET` requests. You can specify the HTTP methods that a route should handle using the `methods` argument.

```python
@app.route("/submit", methods=["GET", "POST"])
async def submit(req):
    if req.method == "POST":
        # Handle the POST request
        return "Form submitted!"
    # Handle the GET request
    return "Please submit the form."
```

## URL Parameters

You can add variable sections to a URL by marking them with `<variable_name>`. The variable is then passed as a keyword argument to your function.

```python
@app.route("/user/<username>")
async def profile(req, username):
    return f"Hello, {username}!"
```

You can also specify a type for the variable, like `<int:user_id>`.

```python
@app.route("/user/id/<int:user_id>")
async def profile_by_id(req, user_id):
    return f"Hello, user number {user_id}!"
```

JsWeb supports the following converters:

*   `string` (default)
*   `int`
*   `float`
*   `path`
*   `uuid`
