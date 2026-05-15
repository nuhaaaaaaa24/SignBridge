=======================
Configuration Reference
=======================

.. warning::

   Add your ``.env`` to ``.gitignore`` to avoid accidentally committing sensitive information.

.. automodule:: config
    :members:

Overview
=========

This section provides a reference for the configuration settings used in SignBridge. All configurations are defined in the ``config.py`` file. 
Values are loaded from ``.env`` file using the ``python-dotenv`` package.

.. warning::

   Add your ``.env`` to ``.gitignore`` to avoid accidentally committing sensitive information.

Configuration Classes
======================

config
-------
A single base ``Config`` class is used for all environments. All variables are required — if any are missing, the application raises a ``RuntimeError`` and will not start.

Core Settings
==============

SECRET_KEY
----------

Used for secure signing of session cookies and other security-related needs.

.. code-block:: python

    SECRET_KEY = os.environ.get('SECRET_KEY')

PERMANENT_SESSION_LIFETIME
--------------------------

Session will expire after the configured number of minutes of inactivity.

.. code-block:: python

    PERMANENT_SESSION_LIFETIME = timedelta(minutes=int(os.environ.get('PERMANENT_SESSION_LIFETIME', 30)))

Database
=========

SQLALCHEMY_DATABASE_URI
------------------------

Loaded from ``DATABASE_URL`` in ``.env``.

* **Development:** Uses SQLite locally

.. code-block:: python

    'sqlite:///' + os.path.join(basedir, 'app.db')

* **Production:** Uses PostgreSQL on Render

.. code-block:: python

    uri = uri.replace("postgres://", "postgresql+psycopg2://", 1)

.. warning::

   ``DATABASE_URL`` is required. If not set, the application raises a ``RuntimeError`` and will not start.

Email
======

MAIL_SERVER
-----------

Hostname of the SMTP server used to send emails. Required.

MAIL_PORT
---------

SMTP port number. Required — must be set in ``.env``.

MAIL_USE_TLS
------------

Enables TLS encryption. Set to ``1`` to enable.

MAIL_USERNAME / MAIL_PASSWORD
------------------------------

SMTP credentials loaded from ``.env``. Required for sending emails. For Gmail, generate an App Password at `myaccount.google.com/apppasswords <https://myaccount.google.com/apppasswords>`_.

ADMINS
------

List of admin emails that receive error notifications.

.. code-block:: python

    ADMINS = ['admin.signbridge+errors@gmail.com']

Rate Limiting
==============

RATELIMIT_STORAGE_URI
----------------------

Storage backend for rate limiting. Required.

.. code-block:: python

    RATELIMIT_STORAGE_URI = os.environ.get('RATELIMIT_STORAGE_URI')

RATELIMIT_STRATEGY
------------------

Rate limiting strategy. Set to ``fixed-window`` for a fixed time window.

.. code-block:: python

    RATELIMIT_STRATEGY = os.environ.get('RATELIMIT_STRATEGY')

reCAPTCHA
==========

RECAPTCHA_PUBLIC_KEY / RECAPTCHA_PRIVATE_KEY
---------------------------------------------

Keys for Google reCAPTCHA. Required.

.. note::

   For development, use Google's test keys which always pass automatically:

   - ``RECAPTCHA_PUBLIC_KEY=6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI``
   - ``RECAPTCHA_PRIVATE_KEY=6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe``

Environment Variables
======================

All of the following must be set in your ``.env`` file:

.. code-block:: bash

    SECRET_KEY='your-secret-key'
    DATABASE_URL='your-database-url'
    PERMANENT_SESSION_LIFETIME='30'
    MAIL_SERVER='your-mail-server'
    MAIL_PORT='587'
    MAIL_USE_TLS='1'
    MAIL_USERNAME='your-email-username'
    MAIL_PASSWORD='your-email-password'
    RECAPTCHA_PUBLIC_KEY='your-recaptcha-public-key'
    RECAPTCHA_PRIVATE_KEY='your-recaptcha-private-key'
    RATELIMIT_STORAGE_URI='memory://'
    RATELIMIT_STRATEGY='fixed-window'