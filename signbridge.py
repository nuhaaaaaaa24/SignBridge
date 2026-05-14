"""Application entry point and local development server.

This module bootstraps the Flask application and starts the
``flask-socketio`` development server when executed directly. In
production on Render, the WSGI host imports :data:`app`
directly and this module's ``__main__`` block is never reached.

.. important::
    ``gevent.monkey.patch_all()`` **must** be the very first call in
    this module. Importing any stdlib networking primitive before the
    patch is applied will leave it unpatched, causing subtle
    concurrency bugs that are difficult to reproduce.

Example:
    Start the local development server::

        python signbridge.py
    
    If the FLASK_APP variable has been set to signbridge.py, run::

        flask run

    Open a Flask shell with a pre-populated database context::

        flask shell
        >>> db.session.execute(sa.select(User)).scalars().all()
"""

# import monkeypatch before everything else so gevent can
# patch stdlib networking with gevent-friendly equivalents asap.
from gevent import monkey
monkey.patch_all()

import signal
import sys

import sqlalchemy as sa
import sqlalchemy.orm as so

from app import create_app, db, socketio
from app.models import User

app = create_app()
"""Flask application instance.

Created via the :func:`app.create_app` factory. Imported by Render's
WSGI runner (and by ``flask`` CLI tooling) without executing the
``__main__`` block below.
"""

HOST = "127.0.0.1"
"""Loopback address bound by the local development server."""

PORT = 5000
"""TCP port bound by the local development server."""

@app.shell_context_processor
def make_shell_context():
    """Inject common database symbols into the Flask shell session.

    Decorated with :func:`flask.Flask.shell_context_processor` so that
    ``flask shell`` pre-imports these names automatically, removing
    boilerplate from interactive database queries.

    Returns:
        dict[str, object]: A mapping of name → object exposed in the
        shell. Includes:

        - ``sa`` — the :mod:`sqlalchemy` module.
        - ``so`` — the :mod:`sqlalchemy.orm` module.
        - ``db`` — the :class:`flask_sqlalchemy.SQLAlchemy` extension
          instance bound to :data:`app`.
        - ``User`` — the :class:`app.models.User` ORM model.
    """
    return {'sa': sa, 'so': so, 'db': db, 'User': User}

def handle_shutdown(sig, frame):
    """Handle ``SIGINT`` (Ctrl-C) with a clean, logged shutdown.

    Registered as the ``SIGINT`` handler only when the module is run
    directly (see ``__main__`` below). Allows in-flight requests and
    gevent greenlets to observe the exit rather than being killed
    abruptly by the default handler.

    Args:
        sig (int): Signal number forwarded by :mod:`signal`
            (always :data:`signal.SIGINT` here).
        frame (types.FrameType): Current stack frame at the point the
            signal was received. Not used directly but required by the
            :mod:`signal` handler protocol.
    """
    print("\nShutting down server...")
    app.logger.info("Received shutdown signal")
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_shutdown)
    app.logger.info(f"Development server URL: http://{HOST}:{PORT}")
    socketio.run(app, host=HOST, port=PORT, debug=True, use_reloader=True)