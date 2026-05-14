===============================
CSRF Protection with Flask-WTF
===============================

Overview
========

SignBridge uses CSRF (Cross-Site Request Forgery) protection through
Flask-WTF and WTForms.

CSRF protection helps prevent malicious third-party websites from submitting
unauthorised requests on behalf of authenticated users.

How CSRF Protection Works
=========================

Each form generated using Flask-WTF automatically includes a unique CSRF token.

When a form is submitted:

1. the token is sent together with the request
2. the server validates the token
3. invalid or missing tokens are rejected

This helps ensure that form submissions originate from legitimate application
pages.

Example
=======
Flask-WTF form:

.. code-block:: python

   class LoginForm(FlaskForm):
       username = StringField("Username")
       password = PasswordField("Password")
       submit = SubmitField("Login")

Example template usage:

.. code-block:: html

   <form method="POST">
       {{ form.hidden_tag() }}
   </form>

The ``hidden_tag()`` method automatically inserts the CSRF token into the
form.

Protected Forms
===============

CSRF protection is applied to state-changing forms such as:

* login
* registration
* password reset
* profile editing
* account management forms

Security Benefits
=================

CSRF protection helps prevent:

* forged form submissions
* unauthorised account actions
* malicious third-party request injection