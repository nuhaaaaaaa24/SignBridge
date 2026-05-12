.. _auth-password-reset:

Password Reset via Email
========================

The application allows users to request a password reset. The process utilises a secure, password reset mechanismto reset forgotten passwords via email verification. The mechanism utilises time-limited JSON Web Tokens (JWT) to securely validate password reset requests. The logic is handled in ``app/auth/routes.py``.

Requesting a Password Reset
---------------------------

This flow is initiated when a user requests to reset their forgotten password.

Route Definition
^^^^^^^^^^^^^^^^
Initialises the route for the password reset request page, allowing both ``GET`` and ``POST`` request methods.

.. code-block:: python

    @auth_bp.route('/reset_password_request', methods=['GET', 'POST'])

Rate Limiting
^^^^^^^^^^^^^
Limit spam password reset requests to 5 per minute to avoid unncessary load and suspicious activity.

.. code-block:: python

    @limiter.limit('5 per minute', methods=['POST'])

Authenticated User Validation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Prevents authenticated (logged-in) users from accessing the password reset request page.

.. code-block:: python

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

Form Validation
^^^^^^^^^^^^^^^
Validates the submitted email address using ``ResetPasswordRequestForm`` from ``app/auth/forms.py``.

.. code-block:: python

    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        email = form.email.data.lower().strip()

Database Lookup
^^^^^^^^^^^^^^^
Checks whether the entered email exists in the current database using the ``User`` model.

.. code-block:: python

    user = db.session.scalar(sa.select(User).where(User.email == email))

Email Delivery and Token Generation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If the user exists, it calls ``send_password_reset_email`` from ``app/auth/email.py``. This function generates a temporary password reset token using the ``get_reset_password_token()`` method from the ``User`` model and sends the email.

.. code-block:: python

    if user:
        send_password_reset_email(user)

Resetting the Password
----------------------

This flow is triggered when the user clicks the link in the reset email.

Route Definition
^^^^^^^^^^^^^^^^
Defines the route that accepts the reset token from the URL.

.. code-block:: python

    @auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])

Rate Limiting
^^^^^^^^^^^^^
Restricts repeated password reset submissions to 3 per minute.

.. code-block:: python

    @limiter.limit('3 per minute', methods=['POST'])

Token Validation
^^^^^^^^^^^^^^^^
Validates the password reset token using the static method ``User.verify_reset_password_token()`` from the ``User`` model.

.. code-block:: python

    user = User.verify_reset_password_token(token)

Invalid Token Handling
^^^^^^^^^^^^^^^^^^^^^^
Rejects invalid or expired password reset requests.

.. code-block:: python

    if not user:
        return redirect(url_for('auth.login'))

Password Reuse Prevention
^^^^^^^^^^^^^^^^^^^^^^^^^
Prevents users from reusing their previous password by checking it against the stored hash.

.. code-block:: python

    if user.check_password(form.password.data):
        return redirect(url_for('auth.reset_password', token=token))

Password Update
^^^^^^^^^^^^^^^
Securely updates the user's password using the ``set_password()`` method on the ``User`` model.

.. code-block:: python

    user.set_password(form.password.data)

Database Commit
^^^^^^^^^^^^^^^
Saves the updated password to the database.

.. code-block:: python

    db.session.commit()

Redirection After Reset
^^^^^^^^^^^^^^^^^^^^^^^
Redirects the user to the login page after the password reset process is completed.

.. code-block:: python

    return redirect(url_for('auth.login'))