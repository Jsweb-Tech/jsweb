from functools import wraps
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from .response import redirect, url_for

# This will be initialized by the JsWebApp instance
_serializer = None
_user_loader = None

def init_auth(secret_key, user_loader_func):
    """Initializes the authentication system."""
    global _serializer, _user_loader
    _serializer = URLSafeTimedSerializer(secret_key)
    _user_loader = user_loader_func

def login_user(response, user):
    """Logs a user in by creating a secure session cookie."""
    session_token = _serializer.dumps(user.id)
    response.set_cookie("session", session_token, httponly=True)

def logout_user(response):
    """Logs a user out by deleting the session cookie."""
    response.delete_cookie("session")

def get_current_user(request):
    """Gets the currently logged-in user from the session cookie."""
    session_token = request.cookies.get("session")
    if not session_token:
        return None

    try:
        # The max_age check (e.g., 30 days) is handled by the serializer
        user_id = _serializer.loads(session_token, max_age=2592000)
        return _user_loader(user_id)
    except (SignatureExpired, BadTimeSignature):
        return None

def login_required(handler):
    """
    A decorator to protect routes from unauthenticated access.
    If the user is not logged in, it redirects to the URL for the 'auth.login' endpoint.
    """
    @wraps(handler)
    def decorated_function(request, *args, **kwargs):
        if not request.user:
            # Use url_for to dynamically find the login page
            login_url = url_for(request, 'auth.login')
            return redirect(login_url)
        return handler(request, *args, **kwargs)
    return decorated_function
