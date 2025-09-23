# jsweb/security.py
"""
This module provides security-related helpers, abstracting the underlying libraries.
"""
from werkzeug.security import generate_password_hash, check_password_hash

__all__ = [
    "generate_password_hash",
    "check_password_hash"
]
