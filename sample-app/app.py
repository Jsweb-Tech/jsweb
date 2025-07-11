
from jsweb import JsWebApp, run, render, __VERSION__, html
import config
import models
from jsweb.database import init_db
from models import *

app = JsWebApp()
init_db(config.DATABASE_URL, echo=config.DEBUG)

@app.route("/add")
def add_user(req):
    # Create and save user
    user = User(name="Jones", email="jones@example.com")
    user.save()

    return render("user_added.html", {"user": user})
    
@app.route("/")
def home(req):
    return render("welcome.html", {"name": config.APP_NAME, "version": __VERSION__})

if __name__ == "__main__":
    run(app, host=config.HOST, port=config.PORT)
