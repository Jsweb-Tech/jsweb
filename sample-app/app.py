# D:/jones/Python/jsweb/sample-app/app.py

from jsweb import JsWebApp, run, render, html, json, __VERSION__
import config
import models
# ✅ 1. Import the User model
from models import User

app = JsWebApp(static_url=config.STATIC_URL, static_dir=config.STATIC_DIR, template_dir=config.TEMPLATE_FOLDER)


@app.route("/")
def home(req):
    return render("welcome.html", {"name": config.APP_NAME, "version": config.VERSION, "library_version": __VERSION__})


# ✅ 2. Add a new route to create a user
@app.route("/add-user")
def add_user(req):
    """Creates a new user and saves it to the database."""
    try:
        # Check if the user already exists to prevent errors
        existing_user = User.first(email="john.doe@example2.com")
        if existing_user:
            user_data = {"id": 1, "name": "John Doe"}
            return json(user_data)

        new_user = User(
            name="John Doe2",
            email="john.doe@example2.com"
        )
        new_user.save()
        return json(new_user.all())
    except Exception as e:
        # This will catch other potential database errors
        return f"❌ Error adding user: {e}"


if __name__ == "__main__":
    # Initialize the database connection when running the app
    from jsweb.database import init_db

    init_db(config.DATABASE_URL)
    run(app, host=config.HOST, port=config.PORT)
