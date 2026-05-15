=======================
Gunicorn Configuration
=======================

Overview
========

SignBridge uses Gunicorn as the production WSGI application server.

Gunicorn manages incoming HTTP requests and serves the Flask application in a
production environment.

The application uses gevent workers to support asynchronous Socket.IO
communication.

Dependencies
============

Required deployment dependencies include:

* gunicorn
* gevent
* gevent-websocket
* Flask-SocketIO

These dependencies are defined in ``requirements.txt``.

gevent Integration
==================

The application uses gevent-based concurrency for real-time communication.

The following initialization occurs before other imports:

.. code-block:: python

   from gevent import monkey
   monkey.patch_all()

This allows gevent to patch Python networking libraries for asynchronous I/O.

Example Gunicorn Command
========================

Example production startup command:

.. code-block:: bash

   gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker \
   -w 1 signbridge:app

Configuration Notes
===================

The deployment uses:

* gevent-based workers
* Flask-SocketIO integration
* asynchronous WebSocket handling

Gunicorn imports the Flask application instance directly from ``signbridge.py``.