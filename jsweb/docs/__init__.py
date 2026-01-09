"""
jsweb OpenAPI Documentation System

Automatic Swagger/ReDoc generation with NestJS-style decorators.

Features:
- Automatic OpenAPI 3.0 schema generation
- NestJS-style decorators for route documentation
- Swagger UI and ReDoc interfaces
- Framework-wide request/response validation
- Type-safe with Pydantic internally
"""

from .decorators import (
    api_operation,
    api_response,
    api_body,
    api_query,
    api_header,
    api_security,
    api_tags,
)
from .setup import setup_openapi_docs, configure_openapi, add_security_scheme
from .registry import openapi_registry
from .auto_validation import disable_auto_validation

__all__ = [
    # Decorators
    "api_operation",
    "api_response",
    "api_body",
    "api_query",
    "api_header",
    "api_security",
    "api_tags",
    # Setup functions
    "setup_openapi_docs",
    "configure_openapi",
    "add_security_scheme",
    # Utilities
    "disable_auto_validation",
    # Registry (for advanced usage)
    "openapi_registry",
]
