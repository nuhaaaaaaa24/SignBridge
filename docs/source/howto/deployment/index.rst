===================
Deployment Overview
===================

Overview
========

SignBridge is deployed as a Flask-based real-time web application using
Flask-SocketIO, PostgreSQL, and Gunicorn with gevent-based asynchronous
workers.

The deployment architecture supports:

* real-time video communication
* WebSocket-based signaling
* database persistence
* secure session management
* responsive frontend delivery

The application follows a production-ready layered deployment structure using:

* Flask
* Gunicorn
* gevent
* Flask-SocketIO
* PostgreSQL
* SQLAlchemy
* Flask-Migrate

Deployment Stack
================

The SignBridge deployment environment consists of:

.. list-table::
   :header-rows: 1
   :widths: 30 50

   * - Component
     - Purpose

   * - Flask
     - Main web application framework

   * - Gunicorn
     - Production WSGI application server

   * - gevent
     - Asynchronous concurrency support

   * - Flask-SocketID
     - Real-time WebSocket communication

   * - PostgreSQL
     - Production relational database

   * - SQLAlchemy
     - ORM database abstraction layer

   * - Flask-Migrate
     - Database schema migration management


Application Entry Point
=======================

The application entry point is defined in ``signbridge.py``.

The application is created using the Flask application factory pattern:

.. code-block:: python

   app = create_app()

The application starts using Flask-SocketIO rather than Flask's default
development server:

.. code-block:: python

   socketio.run(app)

This allows gevent to manage asynchronous communication for real-time
Socket.IO events.

Application Factory
===================

The application factory is implemented in ``app/__init__.py``.

The factory is responsible for:

* loading configuration
* registering blueprints
* initializing extensions
* configuring Socket.IO
* configuring logging
* applying security middleware
* starting background schedulers

Environment Variables
=====================

Configuration values are loaded from environment variables using ``config.py``.

Sensitive values such as:

* database credentials
* secret keys
* mail credentials
* reCAPTCHA keys

are stored outside the source code inside environment configuration files.

Database Deployment
===================

The production environment uses PostgreSQL as the primary database backend.

SQLAlchemy provides ORM integration while Flask-Migrate and Alembic manage
database schema migrations.

Frontend Assets
================

Frontend assets are served through Flask static routes.

Static assets include:

* CSS files
* JavaScript modules
* TensorFlow.js model files
* MediaPipe assets
* images and icons