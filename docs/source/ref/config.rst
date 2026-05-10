================
Configuration Reference
================

Overview
=========

This section provides a reference for the configuration settings used in SignBridge. All configurations are defined in the ``config.py`` file. 
Values are loaded from ``env`` file using the ``python-dotenv`` package.

.. Warning::

   * Add your ``.env`` to gitignore to avoid accidentally committing sensitive information.

Configuration Classes
======================

config
-------
A single base ``config`` class is used for all environmental variables. 

Core Settings
==============

SECRET_KEY
----------

* Used for secure signing of session cookies and other security-related needs.

.. code-block:: python

    SECRET_KEY = os.environ.get('SECRET_KEY')

PERMANENT_SESSION_LIFETIME
--------------------------

* Session will expire after 30 minutes of inactivity.

.. code-block:: python

    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)

Database
=========

SQLALCHEMY_DATABASE_URI
------------------------

Loaded from the ``DATABASE_URL`` in ``.env``. 

* **Development:** Uses SQLite locally

.. code-block:: python

    'sqlite:///' + os.path.join(basedir, 'app.db')

* **Production:** Uses PostgreSQL on Render

.. code-block:: python

    uri = uri.replace("postgres://", "postgresql+psycopg2://", 1)

.. Warning::

    * If the ``DATABASE_URL`` is not set, the application raises a ``RuntimeError`` and will not start.

Email
======

MAIL_SERVER
-----------

Hostname of the email server used to send emails (e.g. SMTP Server). 

MAIL_PORT
---------

SMTP Port number. Defaults to ``25`` if not set. 

MAIL_USE_TLS
------------

Enables TLS if environmental variable is set.

MAIL_USERNAME / MAIL_PASSWORD
------------------------------

SMTP Credentials loaded from ``.env``. Required for sending emails.

ADMINS
------

List of admin emails that will receive error notifications.

.. code-block:: python

     ADMINS = ['admin.signbridge+errors@gmail.com']

Rate Limiting
==============

RATELIMIT_STORAGE_URI
----------------------

Storage backend for rate limiting. Defaults to in-memory if not set.

.. code-block:: python

    RATELIMIT_STORAGE_URI = os.environ.get('RATELIMIT_STORAGE_URI', 'memory://')

RATELIMIT_STRATEGY
------------------

Uses ``moving-window`` strategy with a default time window of 1 minute.

Environment Variables
======================

The following variables must be set in your ``.env`` file:

.. code-block:: python

    SECRET_KEY='your-secret-key'
    DATABASE_URL='your-database-url'
    MAIL_SERVER='your-mail-server'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME='your-email-username'
    MAIL_PASSWORD='your-email-password'
    PERMANENT_SESSION_LIFETIME=30 # in minutes
    RECAPTCHA_PUBLIC_KEY='your-recaptcha-public-key'
    RECAPTCHA_PRIVATE_KEY='your-recaptcha-private-key'
    RATELIMIT_STORAGE_URI='memory://'
    RATELIMIT_STRATEGY='fixed-window'
