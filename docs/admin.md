# Admin Interface

JsWeb includes a built-in admin interface that allows you to manage your application's data. The admin interface is powered by the `jsweb.admin` module and is highly customizable.

## Enabling the Admin Interface

To enable the admin interface, you need to create an `Admin` instance and register your models with it.

```python
# app.py
from jsweb import JsWebApp
from jsweb.admin import Admin
from .models import User, Post
import config

app = JsWebApp(config=config)
admin = Admin(app)

admin.register(User)
admin.register(Post)
```

This will create an admin interface at the `/admin` URL.

## Creating an Admin User

To access the admin interface, you need to create an admin user. You can do this using the `jsweb create-admin` command.

```bash
jsweb create-admin
```

This will prompt you to enter a username, email, and password for the new admin user.

## Customizing the Admin Interface

The admin interface is automatically generated based on your models. At the moment, there are no specific customization options like `list_display` or `search_fields` available directly in the `Admin` class. However, you can extend the `Admin` class or modify the admin templates to customize the interface.
