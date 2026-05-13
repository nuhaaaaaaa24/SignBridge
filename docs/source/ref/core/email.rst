===============
Email Utilities
===============

Overview
--------

``core/email.py`` contains reusable email helper functions shared across all blueprints. Sends mail
asynchronously via a background thread so the request is not blocked.

Functions
---------

send_email
~~~~~~~~~~

.. code-block:: python

   send_email(subject, sender, recipients, text_body, html_body)

Builds a :class:`Message` and dispatches it in a background thread.

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Parameter
     - Description
   * - ``subject``
     - Email subject line.
   * - ``sender``
     - Sender address string.
   * - ``recipients``
     - List of recipient address strings.
   * - ``text_body``
     - Plain-text email body.
   * - ``html_body``
     - HTML email body.

send_async_email
~~~~~~~~~~~~~~~~

.. code-block:: python

   send_async_email(app, msg)

Internal helper. Pushes an application context and calls ``mail.send(msg)``.
Called only by :func:`send_email` via :class:`threading.Thread` — do not
call directly.