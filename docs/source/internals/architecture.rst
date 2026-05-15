=====================
Architecture Overview
=====================

Overview
========

SignBridge follows a layered architecture separating presentation, application
logic, business logic, and data storage.

.. image:: /_static/images/architecture.png
   :alt: SignBridge system architecture diagram

Presentation Layer
==================

The frontend is built with HTML, CSS, and JavaScript. The browser sends
HTTPS requests to the application layer and receives session data in return.
The sign language model runs entirely client-side via TensorFlow.js, meaning
no video data is sent to the server.

Application Layer
=================

The application layer handles all server-side logic using Python and Flask.
It consists of two main components:

* **WebRTC** — manages peer-to-peer video calling between users. Signalling
  is handled by the Socket.IO websocket server in ``call/sockets.py``.
* **Websocket Server** — built with Flask-SocketIO running on gevent, handles
  real-time events such as room joining, call signalling, and chat messages.

Business Logic
==============

Sign language recognition runs client-side in the browser using:

* **TensorFlow.js** — runs the SLSL classifier in the browser

Gesture frames are extracted from the user's webcam feed, passed through the
model, and the predicted letter is returned to the UI in real time. No video
data leaves the browser.

Data Layer
==========

* **Flask** — manages the application, blueprints, and database access via
  Flask-SQLAlchemy
* **SQLite** — used for local development
* **PostgreSQL** — used in production on Render

The ML model weights are loaded from ``static/models/``
directly by the browser — they are not served dynamically by Flask.