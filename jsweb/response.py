# D:/jones/Python/jsweb/jsweb/response.py
import json as pyjson
from typing import List, Tuple, Union


class Response:
    """
    A base class for HTTP responses. It encapsulates the body, status, and headers.
    """
    default_content_type = "text/plain"

    def __init__(
            self,
            body: Union[str, bytes],
            status: str = "200 OK",
            headers: List[Tuple[str, str]] = None,
            content_type: str = None,
    ):
        self.body = body
        self.status = status
        # Use a new list if headers is None to avoid mutable default argument issues
        self.headers = list(headers) if headers else []

        # Set the content type
        content_type = content_type or self.default_content_type
        self.headers.append(("Content-Type", content_type))

    def to_wsgi(self) -> Tuple[bytes, str, List[Tuple[str, str]]]:
        """
        Converts the Response object into a tuple that the WSGI server can understand.
        """
        # Ensure the body is bytes
        body_bytes = self.body if isinstance(self.body, bytes) else self.body.encode("utf-8")
        return body_bytes, self.status, self.headers


class HTMLResponse(Response):
    """
    A specific response class for HTML content.
    """
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
            status: str = "200 OK",
            headers: List[Tuple[str, str]] = None,
    ):
        # Convert the Python data structure to a JSON string
        body = pyjson.dumps(data)
        super().__init__(body, status, headers)


# Keep the simple helper functions for convenience.
# They now return Response objects instead of tuples.
def html(body: str, status: str = "200 OK", headers: List[Tuple[str, str]] = None) -> HTMLResponse:
    """Helper function to quickly create an HTMLResponse."""
    return HTMLResponse(body, status, headers)


def json(data: any, status: str = "200 OK", headers: List[Tuple[str, str]] = None) -> JSONResponse:
    """Helper function to quickly create a JSONResponse."""
    return JSONResponse(data, status, headers)
