=====================
Authentication Emails
=====================

Overview
--------

``auth/email.py`` contains helper functions for sending authenticantion emails such as reset password. 

Functions
---------

send_password_reset_email
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   send_password_reset_email(user)

This block of code generates a password reset token for ``user`` and then sends an email to the user's registered email.

**Parameters**

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``user``
     - User model
     - The user requesting a password reset. Must implement
       :meth:`get_reset_password_token`.

Associated Templates
--------------------

**Templates**

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Template
     - Purpose
   * - ``email/reset_password.txt``
     - Plain-text fallback body.
   * - ``email/reset_password.html``
     - HTML body with reset link.

