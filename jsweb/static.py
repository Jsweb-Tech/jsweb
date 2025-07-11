# jsweb/static.py

import os
import mimetypes
from typing import Tuple, List, Union


def serve_static(
    request_path: str, static_url: str, static_dir: str
) -> Tuple[Union[bytes, str], str, List[Tuple[str, str]]]:
    """
    Serves a static file from the configured static directory.

    Args:
        request_path: The full request path (e.g., '/static/css/style.css').
        static_url: The URL prefix for static files (e.g., '/static').
        static_dir: The local directory where static files are stored (e.g., 'static').

    Returns:
        A tuple containing the file content, status, and headers.
    """
    # 1. Calculate the relative path of the file
    # e.g., '/static/css/style.css' -> 'css/style.css'
    relative_path = request_path.lstrip("/").replace(static_url.lstrip("/"), "", 1)
    relative_path = relative_path.lstrip("/")

    # 2. Construct the full, absolute path to the file
    # This prevents ambiguity with the current working directory.
    base_dir = os.path.abspath(static_dir)
    full_path = os.path.abspath(os.path.join(base_dir, relative_path))

    # 3. Security Check: Prevent directory traversal attacks.
    # Ensure the requested file path is actually inside the static directory.
    if not full_path.startswith(base_dir):
        return b"403 Forbidden", "403 Forbidden", [("Content-Type", "text/plain")]

    # 4. Check if the file exists and is a file
    if not os.path.exists(full_path) or not os.path.isfile(full_path):
        return b"404 Not Found", "404 Not Found", [("Content-Type", "text/plain")]

    # 5. Read the file and determine its MIME type
    try:
        with open(full_path, "rb") as f:
            content = f.read()
    except IOError:
        return b"500 Internal Server Error", "500 Internal Server Error", [("Content-Type", "text/plain")]

    content_type = mimetypes.guess_type(full_path)[0] or "application/octet-stream"
    headers = [("Content-Type", content_type)]

    return content, "200 OK", headers