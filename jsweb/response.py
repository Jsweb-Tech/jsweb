# D:/jones/Python/jsweb/jsweb/response.py
import json as pyjson
import logging
import re
from typing import List, Tuple, Union
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import os

logger = logging.getLogger(__name__)

# Global template environment, configured by the application
_template_env = None

def configure_template_env(template_path: str):
    """Configures the global Jinja2 template environment."""
    global _template_env
    _template_env = Environment(loader=FileSystemLoader(template_path))

def url_for(req, endpoint: str, **kwargs) -> str:
    """
    Generates a URL for the given endpoint.
    """
    # A special case for static files, which don't have a route
    if endpoint == 'static':
        static_url = getattr(req.app.config, "STATIC_URL", "/static")
        filename = kwargs.get('filename', '')
        return f"{static_url}/{filename}"

    path = req.app.router.endpoints.get(endpoint)
    if path is None:
        raise ValueError(f"Endpoint '{endpoint}' not found.")

    # Replace path parameters with values from kwargs
    for key, value in kwargs.items():
        path = re.sub(rf"<\w+:{key}>", str(value), path)

    if "<" in path and ">" in path:
        raise ValueError(f"Missing URL parameters for endpoint '{endpoint}': required parameters are in the path '{path}'")

    return path

# A comprehensive mapping of common status codes to their reason phrases.
HTTP_STATUS_CODES = {
    200: "OK",
    201: "Created",
    202: "Accepted",
    204: "No Content",
    301: "Moved Permanently",
    302: "Found",
    304: "Not Modified",
    307: "Temporary Redirect",
    308: "Permanent Redirect",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    409: "Conflict",
    422: "Unprocessable Entity",
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
}


class Response:
    """
    A base class for HTTP responses. It encapsulates the body, status, and headers.
    """
    default_content_type = "text/plain"

    def __init__(
            self,
            body: Union[str, bytes],
            status: Union[int, str] = 200,
            headers: List[Tuple[str, str]] = None,
            content_type: str = None,
    ):
        self.body = body

        if isinstance(status, int):
            reason = HTTP_STATUS_CODES.get(status, "Unknown Status")
            self.status = f"{status} {reason}"
        else:
            self.status = status

        self.headers = list(headers) if headers else []

        final_content_type = content_type or self.default_content_type
        if not any(h[0].lower() == "content-type" for h in self.headers):
            self.headers.append(("Content-Type", final_content_type))

    def set_cookie(
        self,
        key: str,
        value: str = "",
        max_age: int = None,
        expires: datetime = None,
        path: str = "/",
        domain: str = None,
        secure: bool = False,
        httponly: bool = False,
        samesite: str = 'Lax',
    ):
        """Sets a cookie in the response headers."""
        cookie_val = f"{key}={value}"
        if max_age is not None:
            cookie_val += f"; Max-Age={max_age}"
        if expires is not None:
            cookie_val += f"; Expires={expires.strftime('%a, %d %b %Y %H:%M:%S GMT')}"
        if path is not None:
            cookie_val += f"; Path={path}"
        if domain is not None:
            cookie_val += f"; Domain={domain}"
        if samesite is not None:
            cookie_val += f"; SameSite={samesite}"
        if secure:
            cookie_val += "; Secure"
        if httponly:
            cookie_val += "; HttpOnly"
        self.headers.append(("Set-Cookie", cookie_val))

    def delete_cookie(self, key: str, path: str = "/", domain: str = None):
        """Deletes a cookie by setting its expiry date to the past."""
        self.set_cookie(key, expires=datetime(1970, 1, 1), path=path, domain=domain)

    def to_wsgi(self) -> Tuple[bytes, str, List[Tuple[str, str]]]:
        """
        Converts the Response object into a tuple that the WSGI server can understand.
        """
        body_bytes = self.body if isinstance(self.body, bytes) else self.body.encode("utf-8")
        if not any(h[0].lower() == "content-length" for h in self.headers):
            self.headers.append(("Content-Length", str(len(body_bytes))))

        return body_bytes, self.status, self.headers


class HTMLResponse(Response):
    """A specific response class for HTML content."""
    default_content_type = "text/html"


class JSONResponse(Response):
    """
    A specific response class for JSON content.
    It automatically handles dumping the data to a JSON string.
    """
    default_content_type = "application/json"

    def __init__(
            self,
            data: any,
            status: Union[int, str] = 200,
            headers: List[Tuple[str, str]] = None,
    ):
        body = pyjson.dumps(data)
        super().__init__(body, status, headers)


class RedirectResponse(Response):
    """
    A specific response class for HTTP redirects.
    """
    def __init__(
        self,
        url: str,
        status: int = 302,  # Default to a temporary redirect
        headers: List[Tuple[str, str]] = None,
    ):
        super().__init__(body="", status=status, headers=headers)
        self.headers.append(("Location", url))

class Forbidden(Response):
    """A specific response class for 403 Forbidden errors."""
    def __init__(self, body="403 Forbidden"):
        super().__init__(body, status=403, content_type="text/html")

def render(req, template_name: str, context: dict = None) -> "HTMLResponse":
    """
    Renders a Jinja2 template into an HTMLResponse.
    """
    if _template_env is None:
        raise RuntimeError(
            "Template environment not configured. "
            "Please ensure the JsWebApp is initialized correctly."
        )

    if context is None:
        context = {}

    if hasattr(req, 'csrf_token'):
        context['csrf_token'] = req.csrf_token
    
    # Make url_for available in all templates
    context['url_for'] = lambda endpoint, **kwargs: url_for(req, endpoint, **kwargs)

    template = _template_env.get_template(template_name)
    body = template.render(**context)
    return HTMLResponse(body)


def html(body: str, status: Union[int, str] = 200, headers: List[Tuple[str, str]] = None) -> HTMLResponse:
    return HTMLResponse(body, status, headers)

def json(data: any, status: Union[int, str] = 200, headers: List[Tuple[str, str]] = None) -> JSONResponse:
    return JSONResponse(data, status, headers)

def redirect(url: str, status: int = 302, headers: List[Tuple[str, str]] = None) -> RedirectResponse:
    return RedirectResponse(url, status, headers)
