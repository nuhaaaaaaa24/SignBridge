.. _auth-flows:

Login and Registration Flows
============================

This document explains the registration, login, and logout flows used in the SignBridge authentication system. The main logic is placed in ``app/auth/routes.py``.

Registration
------------

The registration flow creates a new user account.

Route Definition
^^^^^^^^^^^^^^^^

Defines the registration route and allows both ``GET`` and ``POST`` requests.

.. code-block:: python

    @auth_bp.route('/register', methods=['GET', 'POST'])

Rate Limiting
^^^^^^^^^^^^^

Limits registration attempts to 5 POST requests per minute.

.. code-block:: python

    @limiter.limit("5 per minute", methods=['POST'])

Authenticated User Check
^^^^^^^^^^^^^^^^^^^^^^^^

Redirects to the dashboard page if the user is already authenticated (logged in).

.. code-block:: python

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

Form Validation
^^^^^^^^^^^^^^^
Validates the submitted registration form using ``SignupForm`` from ``app/auth/forms.py``. This form employs custom validators defined in ``app/core/validators.py`` to ensure password complexity and unique emails/usernames..

.. code-block:: python

    form = SignupForm()

    if form.validate_on_submit():

Creating the User
^^^^^^^^^^^^^^^^^
Creates a new ``User`` object (defined in ``app/models.py``) using the submitted username and email address. Email addresses are converted to lowercase and removed of leading whitespace.

.. code-block:: python

    user = User(
        username=form.username.data,
        email=form.email.data.lower().strip()
    )

Password Hashing (With Flask-Bcrypt).
^^^^^^^^^^^^^^^^
Hashes the user's password using the ``set_password()`` method from the ``User`` model in ``app/models.py``.

.. code-block:: python

    user.set_password(form.password.data)

Adding the User
^^^^^^^^^^^^^^^

Adds the user to the database session.

.. code-block:: python

    db.session.add(user)

Database Flush
^^^^^^^^^^^^^^

Flushes the session to obtain an unique ID for the new user before committing to the database.

.. code-block:: python

    db.session.flush()

Token Generation
^^^^^^^^^^^^^^^^
Generates an API token for the new user via the ``get_token()`` method on the ``User`` model.

.. code-block:: python

    user.get_token()

Saving Changes
^^^^^^^^^^^^^^

Commits the registration data to the database.

.. code-block:: python

    db.session.commit()

Duplicate User Handling
^^^^^^^^^^^^^^^^^^^^^^^

Handles duplicate usernames or email addresses by catching the ``IntegrityError`` exception from SQLAlchemy and rolling back the session.

.. code-block:: python

    except sa.exc.IntegrityError:
        db.session.rollback()
        flash('Username or email already exists.')

Redirecting After Registration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Redirects the user to the login page after successful registration.

.. code-block:: python

    flash('Congratulations, you are now a registered user!')
    return redirect(url_for('auth.login'))

Login
-----

The login flow authenticates users and creates a session.

Route Definition
^^^^^^^^^^^^^^^^

Defines the login route and allows both ``GET`` and ``POST`` requests.

.. code-block:: python

    @auth_bp.route('/login', methods=['GET', 'POST'])

Rate Limiting
^^^^^^^^^^^^^

Limits login attempts to 5 POST requests per minute.

.. code-block:: python

    @limiter.limit("5 per minute", key_func=login_key, methods=['POST'])

Authenticated User Check
^^^^^^^^^^^^^^^^^^^^^^^^

Redirects authenticated users to the dashboard.

.. code-block:: python

    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))

Form Validation
^^^^^^^^^^^^^^^
Validates the submitted login form using ``LoginForm`` from ``app/auth/forms.py``.

.. code-block:: python

    form = LoginForm()

    if form.validate_on_submit():

Finding the User
^^^^^^^^^^^^^^^^
Searches for a matching user account using the ``User`` model from ``app/models.py``.

.. code-block:: python

    user = db.session.scalar(
        sa.select(User).where(User.username == form.username.data)
    )

Blocked Account Check
^^^^^^^^^^^^^^^^^^^^^
Checks the ``is_blocked`` attribute on the ``User`` model.

.. code-block:: python

    if user.is_blocked:
        flash('Your account has been blocked.')

Password Verification
^^^^^^^^^^^^^^^^^^^^^
Verifies the user entered password against the stored hash using the ``check_password()`` method from the ``User`` model.

.. code-block:: python

    if not user.check_password(form.password.data):

Failed Login Attempts
^^^^^^^^^^^^^^^^^^^^^
Increments the ``failed_login_attempts`` counter on the ``User`` model.

.. code-block:: python

    user.failed_login_attempts += 1

Account Blocking
^^^^^^^^^^^^^^^^
Blocks the account by setting the ``is_blocked`` flag on the ``User`` model after exceeding the initialised maximum failed login attempts.

.. code-block:: python

    if user.failed_login_attempts >= MAX_LOGIN_ATTEMPTS:
        user.is_blocked = True

Resetting Failed Attempts
^^^^^^^^^^^^^^^^^^^^^^^^^
Resets the ``failed_login_attempts`` counter on the ``User`` model after successful authentication.

.. code-block:: python

    user.failed_login_attempts = 0

Token Refresh
^^^^^^^^^^^^^
Generates a new API token after successful login using the ``get_token()`` method on the ``User`` model.

.. code-block:: python

    user.get_token()

Creating the Session
^^^^^^^^^^^^^^^^^^^^
Creates a login session for the authenticated user using ``login_user`` from the ``Flask-Login`` extension.

.. code-block:: python

    login_user(user, remember=form.remember_me.data)

Redirecting After Login
^^^^^^^^^^^^^^^^^^^^^^^

Redirects the user to the dashboard after successful login.

.. code-block:: python

    return redirect(url_for('user.dashboard'))

Logout
------

The logout flow terminates the user's session.

Route Definition
^^^^^^^^^^^^^^^^

Defines the logout route.

.. code-block:: python

    @auth_bp.route('/logout')

Logging Out the User
^^^^^^^^^^^^^^^^^^^^
Removes the user's authenticated session using ``logout_user`` from the ``Flask-Login`` extension.

.. code-block:: python

    logout_user()

Redirecting After Logout
^^^^^^^^^^^^^^^^^^^^^^^^

Redirects the user to the home page after logout.

.. code-block:: python

    return redirect(url_for('main.index'))