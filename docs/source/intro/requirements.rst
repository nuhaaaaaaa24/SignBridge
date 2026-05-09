============
Requirements
============

Python
======

SignBridge requires Python 3.14 or above.

.. note::
   You can get it from `python.org <https://www.python.org/downloads/>`_.

Browser
=======

SignBridge is compatible with all modern browsers:

* Chrome (recommended)
* Firefox
* Safari
* Edge

.. note::

   Camera and microphone permissions must be granted in your browser to use
   the video call and sign language recognition features. WebRTC is required
   for peer-to-peer video — older browsers may not support this.

Processing Power
================

Sign language recognition runs a MobileNet model locally in the browser via
TensorFlow.js. A modern CPU is sufficient for most devices, but performance
may vary on older or low-end hardware.

* **Windows** — Windows 10 or above recommended
* **macOS** — macOS 11 (Big Sur) or above recommended
* **Linux** — Any modern distribution with a supported browser

.. note::

   A dedicated GPU is not required, but may improve inference speed on
   supported devices.

Database
========

SignBridge uses different databases depending on the environment:

* **Development** — SQLite (no setup required, file-based)
* **Production** — PostgreSQL (recommended for reliability and performance)

Dependencies
============

All Python dependencies are listed in ``requirements.txt`` and can be
installed with:

.. code-block:: bash

   pip install -r requirements.txt

Key dependencies include Flask, Flask-SocketIO, SQLAlchemy, and Flask-Migrate.
See ``requirements.txt`` for the full list.