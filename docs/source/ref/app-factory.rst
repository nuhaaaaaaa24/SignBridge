===========
App Factory
===========

.. automodule:: app
    :members:

Overview
========

SignBridge uses the application factory pattern. The ``create_app()`` function
in ``app/__init__.py`` initialises all extensions, registers blueprints, and
sets up error handlers and logging. This pattern allows the app to be created
with different configurations, which is useful for testing.

.. code-block:: python

   from config import Config
   app = create_app(Config)

Extensions
==========

Extensions are initialized in this oder:

.. code-block:: python

    db.init_app(app)
    migrate.init_app(app)
    csrf.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    socketio.init_app(app, async_mode'gevent', cors_allowed_origins='*')
    bcrypt.init_app(app)
    limit.init_app(app)

All of these extensions are defined in ``extensions.py`` and are imported here to avoid circular imports.

Blueprint Registration
======================

The table below shows the registered order of the blueprintd with their URL prefixes:

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Blueprint
     - URL Prefix
     - Description
   * - ``auth_bp``
     - (none)
     - Login, logout, register, password reset
   * - ``errors_bp``
     - ``/errors``
     - Custom error handlers
   * - ``call_bp``
     - (none)
     - Session joining and call room
   * - ``help_bp``
     - ``/help``
     - Help pages and SLSL chart
   * - ``main_bp``
     - (none)
     - Landing page, about, contact
   * - ``user_bp``
     - ``/your-account``
     - User profile and dashboard
   * - ``admin_bp``
     - ``/admin``
     - Admin dashboard
   * - ``api_bp``
     - ``/api``
     - REST API

Error handling
==============

* ``404``: Page not found
* ``429``: Rate limit exceeded
* ``500``: Internal server error

The rate limit handler is also set directly on the limiter:

.. code-block:: python

   limiter._rate_limit_exceeded_handler = ratelimit_exceeded

Logging
==============

Logging is only active when the app is not in debug or testing mode. 

**Email logging** — errors are emailed to ``admin.signbridge+errors@gmail.com``
via SMTP when ``MAIL_SERVER`` is configured.

**File logging** — logs are written to ``app/logs/signbridge.log`` using a
rotating file handler with a max size of 10KB and 10 backup files.

Log format:

.. code-block:: text

   %(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]

Security Headers
================

In production, the following headers are added to every response:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Header
     - Purpose
   * - ``Strict-Transport-Security``
     - Forces HTTPS for 1 year including subdomains.
   * - ``X-Frame-Options: SAMEORIGIN``
     - Prevents clickjacking by blocking iframe embedding from other origins.
   * - ``X-Content-Type-Options: nosniff``
     - Prevents MIME type sniffing vulnerabilities.

Proxy Handling
==============

``ProxyFix`` is applied to handle reverse proxy headers correctly when
deployed behind Nginx on Render:

.. code-block:: python

   app.wsgi_app = ProxyFix(app.wsgi_app, x_for=2, x_proto=1, x_host=1)
