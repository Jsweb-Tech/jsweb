from jsweb.routing import Router
from jsweb.request import Request
from jsweb.static import serve_static
# Assuming you have a response module as suggested
from jsweb.response import Response, HTMLResponse


class JsWebApp:
    """
    The main application class for the JsWeb framework.

    It is responsible for routing requests and is configurable.
    Database schema management should be handled by a separate CLI command.
    """

    def __init__(self, static_url="/static", static_dir="static", template_dir="templates"):
        self.router = Router()
        self.template_filters = {}

        # Make static and template paths configurable
        self.static_url = static_url
        self.static_dir = static_dir
        self.template_dir = template_dir

    def route(self, path, methods=None):
        """A decorator to register a view function for a given URL path."""
        if methods is None:
            methods = ["GET"]
        return self.router.route(path, methods)

    def filter(self, name):
        """
        A decorator to register a custom filter for use in templates.
        The filter is registered with this specific app instance.
        """

        def decorator(func):
            self.template_filters[name] = func
            return func

        return decorator

    def __call__(self, environ, start_response):
        """The main WSGI entry point."""
        req = Request(environ)

        # Handle static files using the configured path
        if req.path.startswith(self.static_url):
            content, status, headers = serve_static(req.path, self.static_url, self.static_dir)
            start_response(status, headers)
            # Ensure content is bytes
            return [content if isinstance(content, bytes) else content.encode("utf-8")]

        # Resolve and handle dynamic routes
        handler = self.router.resolve(req.path, req.method)
        if handler:
            response = handler(req)

            # If a handler returns a raw string, wrap it in a default response object
            if isinstance(response, str):
                response = HTMLResponse(response)

            # If it's not a Response object, it's an error
            if not isinstance(response, Response):
                raise TypeError(f"View function did not return a Response object (got {type(response).__name__})")

            # Convert our Response object to what the WSGI server needs
            body_bytes, status, headers = response.to_wsgi()
            start_response(status, headers)
            return [body_bytes]

        # Handle 404 Not Found
        start_response("404 Not Found", [("Content-Type", "text/html")])
        return [b"<h1>404 Not Found</h1>"]