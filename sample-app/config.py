
# config.py
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

APP_NAME = "Sample-app"
DEBUG = False
VERSION = "0.1.0"
TEMPLATE_FOLDER = "templates"
STATIC_URL = "/static"
STATIC_DIR = "static"
# Use an absolute path for SQLite to avoid ambiguity

DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'jsweb.db')}"
# DATABASE_URL = "postgresql://user:pass@host:port/dbname"

HOST = "127.0.0.1"
PORT = 8000
