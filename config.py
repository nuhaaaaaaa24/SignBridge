"""Configuration file for application settings.

This module defines the :class:`Config` class, which defines all
environment variables for the Flask application. Values are
loaded from an ``.env`` file at startup.

Example:
    Typical usage with a Flask application factory::

        from config import Config

        def create_app():
            app = Flask(__name__)
            app.config.from_object(Config)
            return app

Note:
    All required environment variables must be present in the ``.env``
    file or the shell before the module is imported. This is because 
    missing variables raise a :exc:`RuntimeError` at startup rather 
    than silently failing at runtime.
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    """Flask application configuration populated from environment variables.

    All attributes are resolved eagerly at import time via
    :meth:`get_env_variable`. If any required variable is absent the
    application will refuse to start, preventing misconfigured deployments
    from reaching production.

    Attributes:
        SECRET_KEY (str): Cryptographic secret used to sign sessions and
            generate CSRF tokens. Must be a long, random string.
        PERMANENT_SESSION_LIFETIME (str): Duration of user inactivity before
            a session expires. Passed directly from the environment. The
            recommended value is ``1800`` seconds (30 minutes).
        SQLALCHEMY_DATABASE_URI (str): SQLAlchemy-compatible database
            connection string. ``postgres://`` schemes are automatically
            rewritten to ``postgresql+psycopg2://`` for compatibility with
            SQLAlchemy.
        RATELIMIT_STORAGE_URI (str): Backend URI used by Flask-Limiter
            to persist rate-limit counters. Kept separate from 
            :attr:`SQLALCHEMY_DATABASE_URI`.
        RATELIMIT_STRATEGY (str): Rate-limiting algorithm applied by
            Flask-Limiter. Use ``"moving-window"`` to enforce a rolling
            one-minute window.
        MAIL_SERVER (str): Hostname of the outgoing SMTP server used to
            deliver admin and error notification emails.
        MAIL_PORT (str): Port number for the SMTP connection (e.g. ``587``
            for TLS, ``465`` for SSL).
        MAIL_USE_TLS (str): Whether to upgrade the SMTP connection with
            STARTTLS. Accepts ``"True"`` or ``"False"`` as a string.
        MAIL_USERNAME (str): SMTP authentication username.
        MAIL_PASSWORD (str): SMTP authentication password.
        ADMINS (str): Comma-separated list of administrator email addresses
            that receive error reports and system notifications.
        RECAPTCHA_PUBLIC_KEY (str): Site key issued by Google reCAPTCHA,
            embedded in HTML forms and sent to the client.
        RECAPTCHA_PRIVATE_KEY (str): Secret key used server-side to verify
            reCAPTCHA challenge responses with Google's API.
    """

    def get_env_variable(var_name):
        """Retrieve a mandatory environment variable or abort startup.

        Designed to be called when the module is first imported,
        rather than raising an error after the application has launched.

        Args:
            var_name (str): The name of the environment variable to read.

        Returns:
            str: The value of the environment variable.

        Raises:
            RuntimeError: If the variable is unset or evaluates to an empty
                string.

        Example:
            ::

                SECRET_KEY = get_env_variable('SECRET_KEY')
        """
        value = os.environ.get(var_name)
        if not value:
            raise RuntimeError(f"{var_name} is not set. Aborting launch sequence.")
        return value

    SECRET_KEY = get_env_variable('SECRET_KEY')
    PERMANENT_SESSION_LIFETIME = get_env_variable('PERMANENT_SESSION_LIFETIME')

    uri = get_env_variable('DATABASE_URL')
    if uri.startswith("postgres://"):
        # replace to allow sqlalchemy to handle the database
        uri = uri.replace("postgres://", "postgresql+psycopg2://", 1)
    SQLALCHEMY_DATABASE_URI = uri

    RATELIMIT_STORAGE_URI = get_env_variable("RATELIMIT_STORAGE_URI")
    RATELIMIT_STRATEGY = get_env_variable("RATELIMIT_STRATEGY")

    MAIL_SERVER = get_env_variable('MAIL_SERVER')
    MAIL_PORT = get_env_variable('MAIL_PORT')
    MAIL_USE_TLS = get_env_variable('MAIL_USE_TLS')
    MAIL_USERNAME = get_env_variable('MAIL_USERNAME')
    MAIL_PASSWORD = get_env_variable('MAIL_PASSWORD')
    ADMINS = ['admin.signbridge+errors@gmail.com']

    RECAPTCHA_PUBLIC_KEY = get_env_variable("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = get_env_variable("RECAPTCHA_PRIVATE_KEY")