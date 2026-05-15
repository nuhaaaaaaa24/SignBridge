========================
Pre-Deployment Checklist
========================

Overview
========

Before deploying SignBridge to a production environment, several configuration
and validation steps must be completed to ensure the stability, security,
and compatibility of the system.

Environment Configuration
=========================

Verify that all required environment variables are configured correctly.

Required variables include:

* SECRET_KEY
* DATABASE_URL
* MAIL_SERVER
* MAIL_USERNAME
* MAIL_PASSWORD
* RECAPTCHA_PUBLIC_KEY
* RECAPTCHA_PRIVATE_KEY
* RATELIMIT_STORAGE_URI
* RATELIMIT_STRATEGY

The application validates required environment variables during startup using ``config.py``.

Dependency Installation
=======================

Install all required Python dependencies using:

.. code-block:: bash

   pip install -r requirements.txt

The project dependencies are defined in ``requirements.txt``.

Database Setup
==============

Before deployment:

* configure PostgreSQL
* verify database connectivity
* run all migrations
* confirm schema creation

Run migrations using:

.. code-block:: bash

   flask db upgrade

Socket.IO Compatibility
=======================

Verify that asynchronous support libraries are installed:

* gevent
* gevent-websocket

The application uses gevent-based asynchronous Socket.IO communication.


Frontend Assets
================

Ensure all frontend assets are present within the static directory.

Required assets include:

* CSS stylesheets
* JavaScript modules
* TensorFlow.js model shards
* MediaPipe assets
* images and icons

Security Checks
===============

Before deployment:

* disable debug mode
* verify HTTPS configuration
* verify CSRF protection
* verify password hashing
* confirm security headers are enabled

Production security headers are configured in ``app/__init__.py``.

Testing
=======

Run automated tests before deployment.

Pytest:

.. code-block:: bash

   pytest tests/ --ignore=tests/test_selenium.py -v

Selenium tests:

.. code-block:: bash

   pytest tests/test_selenium.py -v