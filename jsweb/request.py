from urllib.parse import parse_qs

class Request:
    def __init__(self, environ, app):
        self.environ = environ
        self.app = app  # Store a reference to the app instance
        self.method = self.environ.get("REQUEST_METHOD", "GET").upper()
        self.path = self.environ.get("PATH_INFO", "/")
        self.query = self._parse_query(self.environ.get("QUERY_STRING", ""))
        self.headers = self._parse_headers(self.environ)
        self.cookies = self._parse_cookies(self.environ)
        self.user = None  # Will be populated by the app

        self._body = None
        self._form = None

    @property
    def body(self):
        if self._body is None:
            try:
                length = int(self.environ.get("CONTENT_LENGTH", 0))
                self._body = self.environ["wsgi.input"].read(length).decode("utf-8")
            except (ValueError, KeyError):
                self._body = ""
        return self._body

    @property
    def form(self):
        if self._form is None:
            if self.method in ("POST", "PUT", "PATCH") and "application/x-www-form-urlencoded" in self.environ.get("CONTENT_TYPE", ""):
                self._form = {k: v[0] for k, v in parse_qs(self.body).items()}
            else:
                self._form = {}
        return self._form

    def _parse_query(self, query_string):
        return {k: v[0] for k, v in parse_qs(query_string).items()}

    def _parse_headers(self, environ):
        return {
            k[5:].replace("_", "-").title(): v
            for k, v in environ.items()
            if k.startswith("HTTP_")
        }

    def _parse_cookies(self, environ):
        cookie_string = environ.get("HTTP_COOKIE", "")
        if not cookie_string:
            return {}
        cookies = {}
        for cookie in cookie_string.split('; '):
            if '=' in cookie:
                key, value = cookie.split('=', 1)
                cookies[key] = value
        return cookies
