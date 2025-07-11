from jsweb.database import get_engine, Base
from jsweb.template import add_filter
from jsweb.routing import Router
from jsweb.request import Request
from jsweb.static import serve_static

class JsWebApp:
    def __init__(self):
        self.router = Router()
        self.models = []

    def route(self, path, methods=None):
        if methods is None:
            methods = ["GET"]
        return self.router.route(path, methods)

    def filter(self, name):
        def decorator(func):
            add_filter(name, func)
            return func
        return decorator

    def model(self, cls):
        self.models.append(cls)
        Base.metadata.create_all(bind=get_engine())
        return cls

    def __call__(self, environ, start_response):
        req = Request(environ)

        # Serve static files
        STATIC_PREFIX = "/static/"
        if req.path.startswith(STATIC_PREFIX):
            content, status, headers = serve_static(req.path[len(STATIC_PREFIX):])
            start_response(status, headers)
            return [content if isinstance(content, bytes) else content.encode("utf-8")]

        # Dynamic routes
        handler = self.router.resolve(req.path, req.method)
        if handler:
            result = handler(req)
            if isinstance(result, tuple):
                body, status, headers = result
            else:
                body, status, headers = result, "200 OK", [("Content-Type", "text/html")]
            if isinstance(body, str):
                body = body.encode("utf-8")
            start_response(status, headers)
            return [body]
        else:
            start_response("404 Not Found", [("Content-Type", "text/html")])
            return [b"<h1>404 Not Found</h1>"]
