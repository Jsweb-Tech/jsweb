from jsweb import Blueprint, render, __VERSION__, login_required, url_for

# A blueprint for the main site pages
views_bp = Blueprint('views')

@views_bp.route("/", methods=["GET", "POST"], endpoint="home")
def home(req):
    message = ""
    if req.method == "POST":
        message = f"Received a POST request with data: {req.form.get('test_input', 'N/A')}"
    
    context = {
        "name": req.app.config.APP_NAME, 
        "version": req.app.config.VERSION, 
        "library_version": __VERSION__,
        "message": message,
        "req": req
    }
    return render(req, "welcome.html", context)

@views_bp.route("/profile", endpoint="profile")
@login_required
def profile(req):
    return render(req, "profile.html", {"req": req, "app": req.app, "library_version": __VERSION__})