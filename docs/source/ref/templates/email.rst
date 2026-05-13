===============
Email Templates
===============

| **Location:** ``app/templates/email/``

Overview
--------

Jinja2 templates for authentication-related emails such as password reset. Each email has both HTML (``.html``) and plain-text (``.txt``) versions.

Templates
---------

reset_password.txt / reset_password.html
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sent by :func:`app.auth.email.send_password_reset_email` when a user
requests a password reset.

**Context variables:**

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Variable
     - Description
   * - ``user``
     - The user requesting the reset.
   * - ``token``
     - Signed reset token from :meth:`get_reset_password_token`.