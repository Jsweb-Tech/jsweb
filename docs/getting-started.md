# Getting Started with JsWeb

Welcome to JsWeb! This guide will walk you through the process of setting up your development environment, creating a new project, and running your first JsWeb application.

## Installation

JsWeb is available on PyPI and can be installed with `pip`. It's recommended to use a virtual environment to manage your project's dependencies.

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install JsWeb
pip install jsweb
```

## Creating a New Project

Once JsWeb is installed, you can use the `jsweb` command-line interface (CLI) to generate a new project. This will create a directory with a standard structure, including all the necessary files to get you started.

```bash
jsweb new myproject
cd myproject
```

This will create a `myproject` directory with the following structure:

```
myproject/
├── alembic/
├── static/
├── templates/
├── alembic.ini
├── app.py
├── auth.py
├── config.py
├── forms.py
├── models.py
└── views.py
```

## Running the Development Server

To run your new JsWeb application, use the `jsweb run` command from within your project directory.

```bash
jsweb run --reload
```

The `--reload` flag enables auto-reloading, which means the server will automatically restart whenever you make changes to your code. This is incredibly useful during development.

You can now access your application by navigating to `http://127.0.0.1:8000` in your web browser.

## What's Next?

Now that you have a running JsWeb project, you're ready to start building your application. Here are a few topics you might want to explore next:

*   **Routing**: Learn how to define routes to handle different URLs in your application.
*   **Templating**: Discover how to use Jinja2 templates to render dynamic HTML.
*   **Database**: Set up a database and use SQLAlchemy to interact with your data.
*   **Forms**: Create forms to handle user input and validation.
*   **Admin**: Explore the built-in admin interface for managing your application's data.
