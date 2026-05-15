=====================
Deploying with gevent
=====================

Overview
========

SignBridge uses gevent as the asynchronous mode for Flask-SocketIO. This is required for WebRTC signalling and real-time chat to work correctly in production.

Configuration
=============

The async mode is set in ``app/__init__.py``:

.. code-block:: python

   socketio.init_app(app, async_mode='gevent', cors_allowed_origins='*')

On Render
=========

Set the start command on your web service to:

.. code-block:: bash

   gunicorn --worker-class gevent --workers 1 --bind 0.0.0.0:$PORT signbridge:app

Known Issues
============

On Python 3.14, gevent raises an ``AssertionError`` from its for hooks when Flask reloader restarts the process: 

.. code-block:: text

   AssertionError: assert len(active) == 1

This is a known cgevent compatibility issue with Python 3.14 and this does not affect the functionality. To suppress it during development:

.. code-block:: python

   app.run(use_reloader=False)