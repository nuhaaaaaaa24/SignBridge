=====================
Architecture Overview
=====================

Overview
========

SignBridge follows a layered architecture separating presentation, application
logic, business logic, and data storage.

Presentation Layer
==================

The front is built using HTML, CSS and JavaScript. The browser sends HTTP requests to the application 
layer and then receives session data in return. Then the sign language model runs entirely in the client side via 
TensorFlow.js, which means that no video data is sent to the server.


Application Layer
=================

The application layer handles all server-side logic using Python and Flask.
It consists of two main components:

* **WebRTC** — This is used for peer-to-peer video calling and signalling is handled by SocketIO webscoket server in ``call/sockets.py``
* **Websocket Server** — built with Flask-SocketIO running on gevent, handles real-time events such as room joining, call signalling, and chat messages.

Business Logic
==============

Sign language recognition runs client-side in the browser using:

* **TensorFlow.js** — runs the SLSL classifier in the browser

Data Layer
==========

* **Flask** — manages the application, blueprints, and database access via
  Flask-SQLAlchemy
* **SQLite** — used for local development
* **PostgreSQL** — used in production on Render
