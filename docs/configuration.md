# Configuration

JsWeb applications are configured using a `config.py` file in your project's root directory. This file contains all the settings that your application needs to run, such as the database connection string, secret key, and other options.

A new project created with `jsweb new` will have a default `config.py` file that looks like this:

```python
import os

# Get the base directory of the project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Secret key for signing sessions and other security-related things
SECRET_KEY = "your-secret-key"

# Database configuration
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "app.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Static files configuration
STATIC_URL = "/static"
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Template files configuration
TEMPLATE_FOLDER = "templates"
```

## Core Configuration Options

Here are some of the most important configuration options:

| Setting                       | Description                                                                                                                              |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `SECRET_KEY`                  | A secret key that is used for session signing and other security features. This should be a long, random string.                          |
| `SQLALCHEMY_DATABASE_URI`     | The connection string for your database. This tells SQLAlchemy where to find your database.                                              |
| `SQLALCHEMY_TRACK_MODIFICATIONS` | If set to `True`, SQLAlchemy will track modifications of objects and emit signals. The default is `False`.                               |
| `STATIC_URL`                  | The URL prefix for your static files.                                                                                                    |
| `STATIC_DIR`                  | The directory where your static files are located.                                                                                       |
| `TEMPLATE_FOLDER`             | The directory where your templates are located.                                                                                          |

## Accessing Configuration

The configuration is available in your application through the `app.config` object. For example, you can access the `SECRET_KEY` like this:

```python
from jsweb import JsWebApp
import config

app = JsWebApp(config=config)

secret_key = app.config.SECRET_KEY
```
