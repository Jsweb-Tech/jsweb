from jsweb import Blueprint, render, json, html, __VERSION__, login_required, url_for
from forms import UploadForm
import os

# A blueprint for the main site pages
views_bp = Blueprint('views')

@views_bp.route("/", methods=["GET", "POST"], endpoint="home")
async def home(req):
    message = ""
    if req.method == "POST":
        form_data = await req.form()
        message = f"Received a POST request with data: {form_data.get('test_input', 'N/A')}"

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
async def profile(req):
    return render(req, "profile.html", {"req": req, "app": req.app, "library_version": __VERSION__})

# JSON API Example
@views_bp.route("/api/users", methods=["GET"], endpoint="api_users")
async def api_get_users(req):
    """Example JSON API endpoint - GET request"""
    users = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
        {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
    ]
    return json({"users": users, "count": len(users)})

@views_bp.route("/api/users", methods=["POST"], endpoint="api_create_user")
async def api_create_user(req):
    """Example JSON API endpoint - POST request with JSON body"""
    data = await req.json()

    # Validate JSON data
    if not data.get("name") or not data.get("email"):
        return json({"error": "Name and email are required"}, status=400)

    # Simulate user creation
    new_user = {
        "id": 4,
        "name": data.get("name"),
        "email": data.get("email")
    }
    return json({"message": "User created", "user": new_user}, status=201)

# File Upload Example
@views_bp.route("/upload", methods=["GET", "POST"], endpoint="upload")
async def upload_file(req):
    """Example file upload endpoint"""
    form_data = await req.form()
    files_data = await req.files()
    form = UploadForm(form_data, files_data)

    if req.method == "POST" and form.validate():
        uploaded_file = form.file.data

        # Create uploads directory if it doesn't exist
        upload_dir = os.path.join(req.app.config.BASE_DIR, "uploads")
        os.makedirs(upload_dir, exist_ok=True)

        # Save the file
        file_path = os.path.join(upload_dir, uploaded_file.filename)
        uploaded_file.save(file_path)

        return html(f"""
            <h1>File Uploaded Successfully!</h1>
            <p>Filename: {uploaded_file.filename}</p>
            <p>Content Type: {uploaded_file.content_type}</p>
            <p>Size: {uploaded_file.size} bytes</p>
            <a href="/upload">Upload another file</a>
        """)

    return render(req, "upload.html", {"form": form})