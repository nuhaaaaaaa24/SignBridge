=======
Logging
=======

Overview
========

SignBridge uses Python's built-in ``logging`` module integrated with Flask.
Logging is only active when the app is not in debug or testing mode.

There are two handlers configured in the system:

* **File handler** — writes to ``app/logs/signbridge.log``. Rotates at 10KB with 10 backups.
* **Email handler** — emails critical errors to the admin address via SMTP.

For full details on how logging is set up see :doc:`../ref/misc/app-factory`.