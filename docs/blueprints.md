# Blueprints

Blueprints are a way to organize your JsWeb application into smaller, reusable components. A blueprint is a collection of routes that can be registered with your main application. This is a great way to structure larger applications, as it allows you to group related functionality together.

## Creating a Blueprint

To create a blueprint, you first need to import the `Blueprint` class from the `jsweb` library.

**`views.py`**
```python
from jsweb import Blueprint, render

# 1. Create a "Blueprint" for a group of related pages.
views_bp = Blueprint('views')

# 2. Define a route on the blueprint.
@views_bp.route("/")
async def home(req):
    # The render function automatically finds your templates.
    return render(req, "welcome.html", {"user_name": "Guest"})
```

## Registering a Blueprint

Once you've created a blueprint, you need to register it with your main application instance.

**`app.py`**
```python
from jsweb import JsWebApp
import config

# Import the blueprint you just created.
from views import views_bp

# 3. Create the main application instance.
app = JsWebApp(config=config)

# 4. Register your blueprint with the app.
app.register_blueprint(views_bp)
```

## URL Prefixes

You can add a URL prefix to all the routes in a blueprint.

```python
auth_bp = Blueprint('auth', url_prefix='/auth')

@auth_bp.route('/login')
def login():
    ...
```

When you register this blueprint, the `login` route will be available at `/auth/login`.

## Static Files

Blueprints can also have their own static files. To do this, you need to specify the `static_folder` when you create the blueprint.

```python
admin_bp = Blueprint('admin', static_folder='static')
```

This will create a `/admin/static` endpoint that serves files from the `static` folder in your blueprint's directory.
