"""Application factory and extension/blueprint registration.

This module contains :func:`create_app`, the Flask application factory.
All extensions, blueprints, error handlers, background schedulers, and
Socket.IO event handlers are registered here so that the application can
be constructed multiple times (e.g. for testing) without sharing global
state.

Note:
    Import from :mod:`extensions` rather than from this module directly
    to avoid circular imports. See :mod:`extensions` for the extension
    instances themselves.

Example:
    Creating the application in a WSGI entry point::

        from app import create_app

        app = create_app()
"""

from flask import Flask, redirect, url_for, flash
from flask_wtf.csrf import CSRFError
from werkzeug.middleware.proxy_fix import ProxyFix
from apscheduler.schedulers.background import BackgroundScheduler
from config import Config
from extensions import db, migrate, login, csrf, mail, moment, limiter, socketio, bcrypt
from app.errors.handlers import ratelimit_exceeded, page_not_found, internal_error
from app.tasks import process_pending_deletions, cleanup_deleted_users

import logging
import os
import sqlalchemy as sa
from datetime import timedelta
from logging.handlers import SMTPHandler, RotatingFileHandler


def create_app(config_class=Config):
    """Create and configure a Flask application instance.

    Implements the `application factory pattern
    <https://flask.palletsprojects.com/en/latest/patterns/appfactories/>`_
    so that multiple isolated instances can be created during testing
    without sharing extension or blueprint state.

    The factory performs the following steps in order:

    1. Instantiate :class:`~flask.Flask` and apply reverse-proxy middleware.
    2. Load configuration from *config_class*.
    3. Bind all extensions via ``init_app``.
    4. Register blueprints with their URL prefixes.
    5. Attach error and rate-limit handlers.
    6. Register the CSRF session-expiry handler.
    7. Start the :class:`~apscheduler.schedulers.background.BackgroundScheduler`
       for deferred user-deletion tasks.
    8. Register Socket.IO event handlers.
    9. Configure SMTP and rotating-file logging (production only).
    10. Attach security-header middleware (production only).

    Args:
        config_class (type): Configuration class to load via
            :meth:`~flask.Flask.config.from_object`. Defaults to
            :class:`~config.Config`.

    Returns:
        flask.Flask: A fully configured Flask application instance, ready
        to be served by a WSGI/ASGI host or the Socket.IO development
        runner in ``run.py``.
    """
    app = Flask(__name__, static_folder="static", static_url_path="/static")

    # Trust two levels of X-Forwarded-For headers set by Render's load
    # balancer so that rate limiting and IP logging see the real client
    # address rather than the proxy's internal IP.
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=2, x_proto=1, x_host=1)

    app.config.from_object(config_class)

    # Disabled in development to avoid SSL certificate issues with the
    # reCAPTCHA widget when running over plain HTTP.
    app.config['RECAPTCHA_USE_SSL'] = False

    # Convert the raw integer from the environment variable into a
    # timedelta so Flask-Login can use it directly for cookie expiry.
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(
        minutes=int(os.environ.get("PERMANENT_SESSION_LIFETIME", 30))
    )

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    socketio.init_app(app, async_mode='gevent', cors_allowed_origins='*')
    bcrypt.init_app(app)
    limiter.init_app(app)

    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.errors import errors_bp
    app.register_blueprint(errors_bp, url_prefix='/errors')

    from app.call import call_bp
    app.register_blueprint(call_bp)

    from app.help import help_bp
    app.register_blueprint(help_bp, url_prefix='/help')

    from app.main import main_bp
    app.register_blueprint(main_bp)

    from app.user import user_bp
    app.register_blueprint(user_bp, url_prefix='/your-account')

    from app.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Override Flask-Limiter's default 429 handler with our custom view
    # so the response matches the rest of the application's error pages.
    limiter._rate_limit_exceeded_handler = ratelimit_exceeded
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(429, ratelimit_exceeded)
    app.register_error_handler(500, internal_error)

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        """Intercept CSRF validation failures caused by session expiry.

        WTForms raises a :class:`~flask_wtf.csrf.CSRFError` when a form
        is submitted after the session cookie has expired, because the
        CSRF token embedded in the form no longer matches the one stored
        in the (now-empty) session. Showing the raw 400 page is
        confusing; this handler redirects to the login page with an
        explanatory flash message instead.

        Args:
            e (flask_wtf.csrf.CSRFError): The exception raised by
                Flask-WTF's CSRF validation middleware.

        Returns:
            werkzeug.wrappers.Response: A redirect to ``auth.login``
            with a ``'warning'`` flash message.
        """
        flash('Your session expired due to inactivity. Please log in again.', 'warning')
        return redirect(url_for('auth.login'))

    scheduler = BackgroundScheduler()

    # Soft-deleted users are not removed immediately; this job processes
    # the deletion queue hourly so that the window for account recovery
    # remains open between the user's request and final removal.
    scheduler.add_job(
        func=process_pending_deletions,
        args=[app],
        trigger='interval',
        hours=1,
        id='process_pending_deletions',
        replace_existing=True,
    )

    # A second pass removes any database rows left over from users whose
    # deletion was already processed but whose related records were not
    # fully cleaned up (e.g. due to a prior error or restart).
    scheduler.add_job(
        func=cleanup_deleted_users,
        args=[app],
        trigger='interval',
        hours=1,
        id='cleanup_deleted_users',
        replace_existing=True,
    )

    scheduler.start()

    # Imported for side effects: registering @socketio.on decorators
    # defined in app.call.sockets against the socketio instance above.
    from app.call import sockets  # noqa: F401

    if not app.debug and not app.testing:
        _configure_logging(app)

        @app.after_request
        def add_security_headers(response):
            """Attach OWASP-recommended security headers to every response.

            Runs as an ``after_request`` hook so that headers are applied
            uniformly regardless of which blueprint or view produced the
            response.

            The headers set are:

            - ``Strict-Transport-Security``: Forces HTTPS for one year,
              including all subdomains (HSTS).
            - ``X-Frame-Options``: Prevents the page from being embedded
              in a cross-origin ``<iframe>`` (clickjacking mitigation).
            - ``X-Content-Type-Options``: Stops browsers from MIME-type
              sniffing responses away from the declared ``Content-Type``.

            Args:
                response (flask.Response): The outgoing HTTP response
                    object, passed in automatically by Flask.

            Returns:
                flask.Response: The same response object with security
                headers appended.
            """
            response.headers['Strict-Transport-Security'] = (
                'max-age=31536000; includeSubDomains'
            )
            response.headers['X-Frame-Options'] = 'SAMEORIGIN'
            response.headers['X-Content-Type-Options'] = 'nosniff'
            return response

    from app import models  # noqa: F401 — ensures ORM models are registered

    return app


def _configure_logging(app):
    """Set up SMTP error alerts and a rotating file log for production.

    Extracted from :func:`create_app` to keep the factory readable.
    Only called when ``app.debug`` and ``app.testing`` are both
    ``False``.

    SMTP handler
        Sends an email to the admin address whenever a log record at
        ``ERROR`` level or above is emitted.  Requires ``MAIL_SERVER``,
        and optionally ``MAIL_USERNAME`` / ``MAIL_PASSWORD`` and
        ``MAIL_USE_TLS``, to be set in the application config.

    Rotating file handler
        Writes ``INFO``-and-above records to
        ``<app.root_path>/logs/signbridge.log``, rotating at 10 KB and
        keeping the ten most recent archives.

    Args:
        app (flask.Flask): The application instance whose
            :attr:`~flask.Flask.logger` will have handlers attached.
    """
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] and app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])

        secure = () if app.config['MAIL_USE_TLS'] else None

        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=["admin.signbridge+errors@gmail.com"],
            subject='SignBridge Failure',
            credentials=auth,
            secure=secure,
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    log_dir = os.path.join(app.root_path, 'logs')
    os.makedirs(log_dir, exist_ok=True)

    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'signbridge.log'),
        maxBytes=10_240,
        backupCount=10,
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('SignBridge startup complete')