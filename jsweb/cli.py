# jsweb/cli.py
import argparse
import os
import socket
import sys
import importlib.util
from sqlalchemy.schema import CreateTable
from sqlalchemy import text, inspect

from jsweb.server import run
from jsweb import __VERSION__
# We need to interact with the database for migrations
from jsweb.database import init_db, Base, get_engine

JSWEB_DIR = os.path.dirname(__file__)
TEMPLATE_FILE = os.path.join(JSWEB_DIR, "templates", "starter_template.html")
STATIC_FILE = os.path.join(JSWEB_DIR, "static", "global.css")


def create_project(name):
    """Creates a new project scaffold."""
    os.makedirs(name, exist_ok=True)
    os.makedirs(os.path.join(name, "templates"), exist_ok=True)
    os.makedirs(os.path.join(name, "static"), exist_ok=True)
    # The migration system needs a home
    os.makedirs(os.path.join(name, "migrations"), exist_ok=True)

    # Copy template and CSS
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        starter_html = f.read()
    with open(os.path.join(name, "templates", "welcome.html"), "w", encoding="utf-8") as f:
        f.write(starter_html)
    with open(STATIC_FILE, "r", encoding="utf-8") as f:
        css = f.read()
    with open(os.path.join(name, "static", "global.css"), "w", encoding="utf-8") as f:
        f.write(css)

    # Create a more complete models.py
    with open(os.path.join(name, "models.py"), "w", encoding="utf-8") as f:
        f.write("""
from jsweb.database import ModelBase, String, Integer, Column

# Example Model
class User(ModelBase):
    __tablename__ = 'users' # Explicit table name is good practice
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, nullable=False)
""")
    # Create a config.py file
    with open(os.path.join(name, "config.py"), "w", encoding="utf-8") as f:
        f.write(f"""
# config.py
import os

APP_NAME = "{name.capitalize()}"
DEBUG = True
VERSION = "0.1.0"

# Use an absolute path for SQLite to avoid ambiguity
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# ✅ FIX: Escaped the inner f-string's curly braces with {{ and }}
DATABASE_URL = f"sqlite:///{{os.path.join(BASE_DIR, 'jsweb.db')}}"
# DATABASE_URL = "postgresql://user:pass@host:port/dbname"

HOST = "127.0.0.1"
PORT = 8000
""")
    # Create an app.py that does NOT manage the database
    with open(os.path.join(name, "app.py"), "w", encoding="utf-8") as f:
        f.write(f"""
from jsweb import JsWebApp, run, __VERSION__, render
import config
import models

app = JsWebApp(static_url=config.STATIC_URL, static_dir=config.STATIC_DIR, template_dir=config.TEMPLATE_FOLDER)

@app.route("/")
def home(req):
    return render("welcome.html", {{"name": config.APP_NAME, "version":config.VERSION, "library_version": __VERSION__}})

if __name__ == "__main__":
    # Initialize the database connection when running the app
    from jsweb.database import init_db
    init_db(config.DATABASE_URL)
    run(app, host=config.HOST, port=config.PORT)
""")

    print(f"✔️ Project '{name}' created successfully in '{os.path.abspath(name)}'.")
    print(
        f"👉 To get started, run:\n  cd {name}\n  jsweb db makemigrations -m \"Initial migration\"\n  jsweb db migrate\n  jsweb run")


# --- Helper functions (check_port, get_local_ip, display_qr_code) remain the same ---
def check_port(host, port):
    """Checks if a port is available on the given host."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
        return True
    except OSError:
        return False


def get_local_ip():
    """Tries to determine the local IP address of the machine for LAN access."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


def display_qr_code(url):
    """Generates and prints a QR code for the given URL to the terminal."""
    import qrcode
    qr = qrcode.QRCode()
    qr.add_data(url)
    qr.make(fit=True)
    print("📱 Scan the QR code to access the server on your local network:")
    qr.print_tty()
    print("-" * 40)


# --- NEW MIGRATION LOGIC ---

def handle_makemigrations(message):
    """Generates a new SQL migration file from the current models."""
    print("🔎 Finding model changes...")
    migrations_dir = "migrations"

    # Dynamically load the user's models and config
    try:
        # This ensures that the models are registered with SQLAlchemy's Base.metadata
        importlib.import_module("models")
    except ImportError as e:
        print(f"❌ Error: Could not import 'models.py'. Make sure you are in the project root. Details: {e}")
        return

    # ✅ --- THIS IS THE FIX ---
    # Inspect the database to see which tables already exist.
    engine = get_engine()
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    print(f"ℹ️  Tables already in database: {existing_tables}")

    # Generate SQL only for tables that are NOT already in the database.
    sql_commands = []
    new_tables_found = False
    for table in Base.metadata.sorted_tables:
        if table.name not in existing_tables:
            new_tables_found = True
            print(f"  + Found new model to create table for: '{table.name}'")
            sql_commands.append(str(CreateTable(table).compile(dialect=engine.dialect)).strip() + ";")

    if not new_tables_found:
        print("✅ No new models found to create tables for.")
        return

    # Create the new migration file
    existing_migrations = [f for f in os.listdir(migrations_dir) if f.endswith(".sql")]
    next_migration_num = len(existing_migrations) + 1
    # Sanitize message for filename
    safe_message = "".join(c if c.isalnum() else "_" for c in message.lower())
    migration_name = f"{next_migration_num:03d}_{safe_message}.sql"
    migration_path = os.path.join(migrations_dir, migration_name)

    with open(migration_path, "w", encoding="utf-8") as f:
        f.write(f"-- Migration: {message}\n-- Generated by JsWeb\n\n")
        f.write("\n\n".join(sql_commands))

    print(f"✨ Migration created: {migration_path}")
    print("⚠️  Note: This simple system only creates tables. For column changes, you may need to write SQL manually.")


def handle_migrate():
    """Applies all pending SQL migrations to the database."""
    migrations_dir = "migrations"
    log_file = os.path.join(migrations_dir, "migration_log.txt")

    if not os.path.exists(migrations_dir):
        print("✅ No migrations folder found. Nothing to migrate.")
        return

    # Get the set of already applied migrations
    applied_migrations = set()
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            applied_migrations = {line.strip() for line in f if line.strip()}

    # Get all available migrations and sort them to ensure order
    available_migrations = sorted([f for f in os.listdir(migrations_dir) if f.endswith(".sql")])

    # Find migrations that need to be applied
    migrations_to_run = [m for m in available_migrations if m not in applied_migrations]

    if not migrations_to_run:
        print("✅ Database is up to date. No new migrations to apply.")
        return

    print(f"🚀 Found {len(migrations_to_run)} new migration(s) to apply.")
    engine = get_engine()
    with engine.connect() as connection:
        for migration in migrations_to_run:
            print(f"  Applying {migration}...")
            migration_path = os.path.join(migrations_dir, migration)
            with open(migration_path, "r", encoding="utf-8") as f:
                sql_script = f.read()

            try:
                # Execute the entire SQL script within a transaction
                with connection.begin():
                    connection.execute(text(sql_script))

                # Log the successful migration
                with open(log_file, "a", encoding="utf-8") as lf:
                    lf.write(f"{migration}\n")
                print(f"  ✅ Applied {migration}")
            except Exception as e:
                print(f"  ❌ FAILED to apply {migration}. Transaction rolled back.")
                print(f"     Error: {e}")
                return  # Stop on first error

    print("✨ All migrations applied successfully.")


def cli():
    parser = argparse.ArgumentParser(prog="jsweb", description="JsWeb CLI - A lightweight Python web framework.")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__VERSION__}")
    sub = parser.add_subparsers(dest="command", help="Available commands", required=True)

    # --- Run Command ---
    run_cmd = sub.add_parser("run", help="Run the JsWeb application in the current directory.")
    run_cmd.add_argument("--host", default="127.0.0.1", help="Host address to bind to (default: 127.0.0.1)")
    run_cmd.add_argument("--port", type=int, default=8000, help="Port number to listen on (default: 8000)")
    run_cmd.add_argument("--qr", action="store_true", help="Display a QR code for the server's LAN address.")

    # --- New Command ---
    new_cmd = sub.add_parser("new", help="Create a new JsWeb project.")
    new_cmd.add_argument("name", help="The name of the new project")

    # --- DB Command Group ---
    db_cmd = sub.add_parser("db", help="Database migration tools")
    db_sub = db_cmd.add_subparsers(dest="subcommand", help="Migration actions", required=True)

    makemigrations_cmd = db_sub.add_parser("makemigrations", help="Generate a new migration file from model changes.")
    makemigrations_cmd.add_argument("-m", "--message", required=True,
                                    help="A short, descriptive message for the migration.")

    db_sub.add_parser("migrate", help="Apply pending migrations to the database.")

    args = parser.parse_args()
    sys.path.insert(0, os.getcwd())
    if args.command == "run":
        if args.qr:
            try:
                import qrcode
            except ImportError:
                print("❌ Error: The 'qrcode' library is required for the --qr feature.")
                print("   Please install it by running: pip install \"jsweb[qr]\"")
                return  # Exit gracefully

        if not os.path.exists("app.py"):
            print("❌ Error: Could not find 'app.py'. Ensure you are in a JsWeb project directory.")
            return
        if not check_port(args.host, args.port):
            print(f"❌ Error: Port {args.port} is already in use. Please specify a different port using --port.")
            return
        if args.qr:
            # For QR code, we need a specific LAN IP, not 0.0.0.0 or 127.0.0.1
            lan_ip = get_local_ip()
            url = f"http://{lan_ip}:{args.port}"
            display_qr_code(url)
        try:
            import importlib.util

            spec = importlib.util.spec_from_file_location("app", "app.py")
            if spec is None or spec.loader is None:
                raise ImportError("Could not load app.py")
            sys.path.insert(0, os.getcwd())

            app_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(app_module)

            if not hasattr(app_module, "app"):
                raise AttributeError("Application instance 'app' not found in app.py")
            run(app_module.app, host=args.host, port=args.port)

        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user.")
        except ImportError as e:
            print(f"❌ Error: Could not import application.  Check your app.py file. Details: {e}")
        except AttributeError as e:
            print(
                f"❌ Error: Invalid application file. Ensure 'app.py' defines a JsWebApp instance named 'app'. Details: {e}")
        except Exception as e:
            print(f"❌ Error: Failed to run app.  Details: {e}")

    elif args.command == "new":
        create_project(args.name)

    elif args.command == "db":
        try:
            import config
            init_db(config.DATABASE_URL)
        except ImportError:
            print("❌ Error: Could not find 'config.py'. Are you in a JsWeb project directory?")
            return

        if args.subcommand == "makemigrations":
            handle_makemigrations(args.message)
        elif args.subcommand == "migrate":
            handle_migrate()
