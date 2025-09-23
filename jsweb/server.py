from jsweb.utils import get_local_ip
import socket
import time
from wsgiref.simple_server import make_server
import logging
import sys
from jsweb.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

def run(app, host="127.0.0.1", port=8000):
    """
    Runs the WSGI application server with a confirmation on shutdown.
    """
    print_startup_message = True
    while True:
        try:
            with make_server(host, port, app) as httpd:
                if print_startup_message:
                    if host in ("0.0.0.0", "::"):
                        local_ip = get_local_ip()
                        logger.info("🚀 JsWeb server running on:")
                        logger.info(f"   • http://localhost:{port}")
                        logger.info(f"   • http://{local_ip}:{port}  (LAN access)")
                    else:
                        logger.info(f"🚀 JsWeb server running on http://{host}:{port}")
                    logger.info("⏹  Press Ctrl+C to stop the server")
                    print_startup_message = False

                # This interval is key to making the server responsive to Ctrl+C.
                httpd.serve_forever(poll_interval=0.5)

        except KeyboardInterrupt:
            try:
                confirm = input("\n🛑 Do you want to stop the server? [y/N]: ").strip().lower()
                if confirm == 'y':
                    logger.info("✅ Server stopping...")
                    break  # Exit the while loop to shut down.
                else:
                    logger.info("✅ Server restarting...")
                    print_startup_message = True # Ensure startup message is printed again
                    continue # Continue the while loop, restarting the server.
            except KeyboardInterrupt:
                # If Ctrl+C is pressed again at the prompt, just exit.
                logger.info("🛑 Server stopped by user (Ctrl+C during prompt).")
                break
        except OSError as e:
            if e.errno == 98:  # Address already in use
                logger.error(f"\n❌ Error: Port {port} is already in use. Please try again in a moment.")
                time.sleep(2)
            else:
                logger.error(f"\n❌ An unexpected startup error occurred: {e}")
                break # Exit on other errors
        except Exception as e:
            logger.error(f"❌ An unexpected error occurred: {e}")
            break

    logger.info("✅ Server stopped successfully.")
