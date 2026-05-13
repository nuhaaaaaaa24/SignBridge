# import monkeypatch before everything else so gevent can 
# patch them with gevent-friendly functions asap
from gevent import monkey
monkey.patch_all()

import sqlalchemy as sa
import sqlalchemy.orm as so
from app import create_app, db, socketio
from app.models import User
import signal
import sys

# create the app - this is used by render
app = create_app()

# explicitly specify host and port for local server
HOST = "127.0.0.1"
PORT = 5000

# this context processor is used in database operations
@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User}

# gracefully handle shutdown 
def handle_shutdown(sig, frame):
    print("\nShutting down server...")
    app.logger.info("Received shutdown signal")
    sys.exit(0)

# this should only run locally
if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_shutdown)

    app.logger.info(f"Development server URL: http://{HOST}:{PORT}")

    socketio.run(app, host=HOST, port=PORT, debug=True, use_reloader=True)