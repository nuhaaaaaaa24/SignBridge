"""Custom HTTP error handlers for the application.

All handlers are registered in :func:`app.create_app` via
:meth:`~flask.Flask.register_error_handler`. They are defined here
rather than inline in the factory to keep the factory readable and to
allow the handlers to be imported and tested independently.
"""

from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_wtf.csrf import CSRFError

from extensions import db


def page_not_found(e) -> tuple:
    """Render a custom 404 page.

    Args:
        e (werkzeug.exceptions.NotFound): The exception raised by Flask
            when no route matches the requested URL.

    Returns:
        tuple[flask.Response, int]: The rendered ``errors/404.html``
        template and the ``404`` status code.
    """
    return render_template("errors/404.html", title='404 Page Not Found'), 404


def ratelimit_exceeded(e) -> tuple:
    """Handle HTTP 429 rate-limit violations.

    Responds differently depending on the client's accepted content
    types and the endpoint that triggered the limit:

    - **JSON clients** (``Accept: application/json`` without HTML) —
      returns a ``429`` JSON payload so that API consumers receive a
      machine-readable error rather than a redirect.
    - **Login endpoint** — flashes an extended warning that mentions
      the risk of account blocking, since repeated failures on
      ``auth.login`` trigger the automatic lockout logic in
      :func:`~app.auth.routes.login`.
    - **All other endpoints** — flashes a generic slow-down message.

    In both non-JSON cases the user is redirected to the referring page,
    falling back to ``main.index`` if no ``Referer`` header is present.

    Args:
        e (flask_limiter.errors.RateLimitExceeded): The exception raised
            by Flask-Limiter when a configured limit is breached.

    Returns:
        tuple[flask.Response, int]: A JSON error response with status
        ``429`` for API clients, or a redirect response for browser
        clients (the redirect itself carries no explicit status code,
        defaulting to ``302``).
    """
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return jsonify(
            error="rate_limit_exceeded",
            message="Too many requests. Please slow down.",
        ), 429

    if request.endpoint == 'auth.login':
        flash(
            "Too many requests. Please slow down. "
            "If this continues, your account may be blocked.",
            "warning",
        )
    else:
        flash("Too many requests. Please slow down.", "warning")

    return redirect(request.referrer or url_for('main.index'))


def internal_error(e) -> tuple:
    """Render a custom 500 page and roll back any open database transaction.

    The session rollback is performed unconditionally before rendering
    so that a database inconsistency that caused the error does not
    leave a broken transaction open, which would make every subsequent
    request on the same connection fail until the session was manually
    cleaned up.

    Args:
        e (Exception): The unhandled exception that triggered the 500
            response.

    Returns:
        tuple[flask.Response, int]: The rendered ``errors/500.html``
        template and the ``500`` status code.
    """
    db.session.rollback()
    return render_template('errors/500.html', title='500 Internal Server Error'), 500


def handle_csrf_error(e) -> object:
    """Redirect CSRF validation failures caused by session expiry.

    Registered as the :class:`~flask_wtf.csrf.CSRFError` handler in
    :func:`app.create_app`. When a user's session cookie expires due to
    inactivity, the CSRF token embedded in any open form becomes invalid.
    Showing the raw 400 response is confusing; this handler redirects to
    the login page with an explanatory flash message instead.

    Args:
        e (flask_wtf.csrf.CSRFError): The exception raised by Flask-WTF's
            CSRF middleware on token mismatch or absence.

    Returns:
        flask.Response: A redirect to ``auth.login`` with a ``'warning'``
        category flash message.
    """
    flash(
        'Your session expired due to inactivity. Please log in again.',
        'warning',
    )
    return redirect(url_for('auth.login'))