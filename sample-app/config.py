# config.py
import os

APP_NAME = "Sample-app"
DEBUG = True
VERSION = "0.1.0"
SECRET_KEY = "c104bfac97e621f22d8039401d58e94b"  # Crucial for session security
TEMPLATE_FOLDER = "templates"
STATIC_URL = "/static"
STATIC_DIR = "static"
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'jsweb.db')}"
HOST = "127.0.0.1"
PORT = 8000