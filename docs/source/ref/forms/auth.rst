=============
auth/forms.py
=============

Overview
========

The ``auth/forms.py`` contains authentication related forms used
throughout the SignBridge application.

These forms are implemented using Flask-WTF and WTForms and provide secure
handling of user authentication workflows such as:

* account registration
* login
* password reset requests
* password reset confirmation

It also integrates CSRF protection and Google reCAPTCHA validation.

Dependencies
============

``auth/forms.py`` uses:

* Flask-WTF
* WTForms
* Flask-Login
* custom validators from ``app.core.validators``

Implemented Forms
=================

The ``SignupForm`` handles user account registration.

Fields:

.. list-table::
   :header-rows: 1
   :widths: 30 50

   * - Field
     - Purpose

   * - Email
     - User email address

   * - Username
     - Unique username

   * - Password
     - User password

   * - repeat_password
     - Password confirmation

   * - reCAPTCHA
     - Bot protection validation

Validation Features:

* required field validation
* email format validation
* password complexity validation
* unique username validation
* unique email validation
* password confirmation matching
* google reCAPTCHA verfication

LoginForm
=========

The ``LoginForm`` handles user authentication.

Fields:

.. list-table::
   :header-rows: 1
   :widths: 30 50

   * - Field
     - Purpose

   * - Username
     - Username input

   * - Password
     - Password input

   * - remember_me
     - Persistent login option

   * - reCAPTCHA
     - Bot protection validation

Validation Features:

* required field validation
* google reCAPTCHA verification

ResetPasswordRequestForm
========================

The ``ResetPasswordRequestForm`` handles password reset email requests.

.. list-table::
   :header-rows: 1
   :widths: 30 50

   * - Field
     - Purpose

   * - Email
     - User email address

Validation Features:

* required field validation
* email format validation

ResetPasswordForm
=================

The ``ResetPasswordForm`` handles password reset submission.

.. list-table::
   :header-rows: 1
   :widths: 30 50

   * - Field
     - Purpose

   * - Password
     - New password

   * - repeat_password
     - Password confirmation

Validation Features:

* required field validation
* password confirmation matching

Security Features
=================

The module includes several security focused protections.

These include:

* CSRF protection through Flask-WTF
* password complexity validation
* unique credential validation
* google reCAPTCHA integration