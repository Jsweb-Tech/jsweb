import secrets
import logging
from .static import serve_static
from .database import db_session
from .response import Forbidden

logger = logging.getLogger(__name__)

class Middleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        return self.app(environ, start_response)

class CSRFMiddleware(Middleware):
    """Middleware to protect against Cross-Site Request Forgery attacks."""
    def __call__(self, environ, start_response):
        # Get the single, shared request object from the environ
        req = environ['jsweb.request']

        if req.method in ("POST", "PUT", "PATCH", "DELETE"):
            form_token = req.form.get("csrf_token")
            cookie_token = req.cookies.get("csrf_token")

            if not form_token or not cookie_token or not secrets.compare_digest(form_token, cookie_token):
                logger.error("CSRF VALIDATION FAILED. Tokens do not match or are missing.")
                response = Forbidden("CSRF token missing or invalid.")
                body_bytes, status, headers = response.to_wsgi()
                start_response(status, headers)
                return [body_bytes]

        return self.app(environ, start_response)

class StaticFilesMiddleware(Middleware):
    def __init__(self, app, static_url, static_dir):
        super().__init__(app)
        self.static_url = static_url
        self.static_dir = static_dir

    def __call__(self, environ, start_response):
        # Get the single, shared request object from the environ
        req = environ['jsweb.request']
        
        if req.path.startswith(self.static_url):
            content, status, headers = serve_static(req.path, self.static_url, self.static_dir)
            start_response(status, headers)
            return [content if isinstance(content, bytes) else content.encode("utf-8")]
        return self.app(environ, start_response)

class DBSessionMiddleware(Middleware):
    def __call__(self, environ, start_response):
        try:
            return self.app(environ, start_response)
        finally:
            db_session.remove()
