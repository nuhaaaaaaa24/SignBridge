"""Flask extension instances and supporting utilities.

This file is used to initialize extensions to the application.
It exists to solve the problem of circular dependencies when
importing certain modules (e.g. socketio, database) directly
from the app. Each extension is bound to
the real application later by the :func:`app.create_app` factory via the
standard ``ext.init_app(app)`` pattern.

Note:
    Never import from :mod:`app` directly in this module. Doing so
    re-introduces the circular dependency this module exists to break.

Example:
    Importing extensions elsewhere in the package::

        from app.extensions import db, limiter, socketio
"""

import os

from flask import request
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
"""Shared SQLAlchemy database instance.

Bound to the application by :func:`app.create_app`. Import this object
wherever ORM models or raw queries are needed instead of creating a
second :class:`~flask_sqlalchemy.SQLAlchemy` instance.
"""

migrate = Migrate()
"""Alembic-backed migration engine.

Manages schema migrations via ``flask db`` CLI commands. Must be
initialised after :data:`db` inside the application factory.
"""

login = LoginManager()
"""Flask-Login manager that handles session-based authentication.

``login.login_view`` is set to ``'auth.login'`` so that
:func:`~flask_login.login_required` redirects unauthenticated users to
the correct blueprint endpoint automatically.
"""

csrf = CSRFProtect()
"""Global CSRF protection applied to every state-changing request.

Tokens are validated automatically for all ``POST``/``PUT``/``PATCH``/
``DELETE`` form submissions. Individual views or blueprints can opt out
with :func:`~flask_wtf.csrf.exempt`.
"""

mail = Mail()
"""Flask-Mail instance for sending transactional email.

Connection settings (server, port, TLS, credentials) are driven by the
``MAIL_*`` keys in :class:`~config.Config`.
"""

moment = Moment()
"""Flask-Moment integration for client-side timestamp formatting.

Injects the `Moment.js <https://momentjs.com/>`_ library and a helper
into Jinja2 templates, enabling timezone-aware rendering.
"""

socketio = SocketIO()
"""Flask-SocketIO instance for WebSocket and long-polling support.

The application is started via :meth:`~flask_socketio.SocketIO.run`
rather than ``app.run`` so that the gevent WSGI server handles async
I/O correctly. See ``signbridge.py`` for the entry point.
"""

bcrypt = Bcrypt()
"""Flask-Bcrypt wrapper for password hashing and verification.

All password hashes stored in the database should be produced and
checked through this instance to ensure a consistent work factor across
the application.
"""


def get_ip():
    """Extract the real client IP address from a potentially proxied request.

    Render forwards requests through a load
    balancer that appends the original client IP to the
    ``X-Forwarded-For`` header as the leftmost value.

    Returns:
        str: The leftmost IP address in ``X-Forwarded-For`` if the
        header is present, otherwise :attr:`flask.Request.remote_addr`.

    Example:
        ``X-Forwarded-For: 203.0.113.5, 10.0.0.1`` → ``"203.0.113.5"``
    """
    xff = request.headers.get("X-Forwarded-For", request.remote_addr)
    if xff and "," in xff:
        return xff.split(",")[0].strip()
    return xff


def user_or_ip_key():
    """Return a rate-limit bucket key scoped to the current user or IP.

    Authenticated users are bucketed by their database ID so that a
    single account cannot circumvent per-IP limits by rotating IP
    addresses (e.g. via a VPN). Unauthenticated requests fall back to
    the real client IP resolved by :func:`get_ip`.

    Returns:
        str: ``"user:<id>"`` for authenticated sessions, or
        ``"ip:<address>"`` for anonymous requests.
    """
    if current_user.is_authenticated:
        return f"user:{current_user.id}"
    return f"ip:{get_ip()}"


limiter = Limiter(
    key_func=user_or_ip_key,
    strategy="moving-window",
)
"""Flask-Limiter instance with a per-user-or-IP moving-window strategy.

The moving-window strategy counts every request inside a rolling time
window (configured via ``RATELIMIT_STORAGE_URI`` and default limit
strings in :class:`~config.Config`), giving a smoother enforcement
curve than a fixed window. The bucket key is determined by
:func:`user_or_ip_key`.
"""

login.login_view = 'auth.login'
"""Endpoint name that :func:`~flask_login.login_required` redirects to.

Set to the ``login`` view inside the ``auth`` blueprint so that
unauthenticated access to protected routes returns a redirect rather
than a ``401``.
"""

login.login_message = 'Please log in to access this page.'
"""Flash message displayed when a user is redirected to the login page."""