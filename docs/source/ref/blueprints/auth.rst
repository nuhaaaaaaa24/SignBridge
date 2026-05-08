==============
Auth Blueprint
==============

Overview
========

The ``auth`` blueprint handles all authentication related functionality including
login, logout, registration, and password reset. It is registered under the ``/auth`` URL prefix.

Routes
======

.. list-table::
   :header-rows: 1
   :widths: 30 10 60

   * - URL
     - Method
     - Description
   * - ``/auth/login``
     - GET, POST
     - Renders the login form. Validates credentials, tracks failed attempts, and redirects to dashboard on success.
   * - ``/auth/logout``
     - GET
     - Logs out the current user and redirects to the main index.
   * - ``/auth/register``
     - GET, POST
     - Renders the registration form. Creates a new user and generates an API token on success.
   * - ``/auth/reset_password_request``
     - GET, POST
     - Accepts an email address and sends a password reset link if the account exists.
   * - ``/auth/reset_password/<token>``
     - GET, POST
     - Validates the reset token and allows the user to set a new password.

Access Control
==============

* Authenticated users are redirected away from ``/login``, ``/register``, and ``/reset_password_request``.
* Blocked users are automatically logged out on any request via ``before_app_request``.

Rate Limiting
=============

* ``/login`` — 5 requests per minute, keyed by username to prevent case sensitivity abuse.
* ``/register`` — 5 requests per minute, keyed by IP.
* ``/reset_password_request`` — 5 requests per minute, keyed by IP.
* ``/reset_password/<token>`` — 3 requests per minute, keyed by IP.

Forms
=====

* ``LoginForm`` — username, password, remember me
* ``SignupForm`` — username, email, password
* ``ResetPasswordRequestForm`` — email
* ``ResetPasswordForm`` — new password, confirm password

Templates
=========

* ``auth/login.html``
* ``auth/register.html``
* ``auth/reset_password_request.html``
* ``auth/reset_password.html``

Security Notes
==============

* Failed login attempts are tracked per user. After 10 failed attempts the account is automatically blocked.
* Admin accounts are exempt from the failed attempt counter to prevent lockout.
* Password reset emails are sent regardless of whether the email is registered, to prevent account enumeration.
* Users cannot reuse their previous password on reset.
* Sessions are permanent with a 30 minute inactivity timeout set in ``config.py``.