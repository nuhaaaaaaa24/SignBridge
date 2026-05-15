"""Integration and unit tests for authentication routes and the contact form.

Authentication tests exercise the ``/register``, ``/login``, and
``/logout`` endpoints through the test client with redirects followed.
Contact form tests instantiate :class:`~app.main.forms.ContactForm`
directly, bypassing HTTP, to validate WTForms field-level constraints
in isolation.

.. warning::
    Two issues in this file should be addressed:

    - ``test_contact_form_valid`` is defined twice. Python silently
      replaces the first definition with the second, so the first
      (which lacks an application context) is never executed.
    - ``test_contact_form_missing_subject`` calls ``form.validate()``
      *outside* the ``with app.app_context():`` block, so the
      assertion runs without an active context and may produce
      unexpected results.
"""

from app.main.forms import ContactForm


# auth routes

def test_register(client):
    """Registration endpoint creates a new account and returns 200.

    Posts valid registration data to ``/register`` and follows the
    success redirect. Asserts that the final response is ``200 OK``,
    confirming the account was created and the user was redirected to
    the login page without error.

    Note:
        These credentials (``Nuharilwan`` / ``Nuharilwan@24``) are
        independent of the :func:`~tests.conftest.test_user` fixture
        and are created fresh by this request.

    Args:
        client (flask.testing.FlaskClient): The test client provided by
            :func:`~tests.conftest.client`.
    """
    response = client.post(
        '/register',
        data={
            'username': 'Nuharilwan',
            'email': 'nuha@gmail.com',
            'password': 'Nuharilwan@24',
            'password2': 'Nuharilwan@24',
        },
        follow_redirects=True,
    )
    assert response.status_code == 200


def test_login(client, test_user):
    """Login endpoint returns 200 after a successful authentication attempt.

    Posts credentials to ``/login`` and follows the redirect to the
    user dashboard. Asserts ``200 OK`` on the final response.

    Note:
        The credentials submitted here (``Nuharilwan`` /
        ``Nuharilwan@24``) do not match the
        :func:`~tests.conftest.test_user` fixture account
        (``testuser`` / ``password123``). This test will pass the HTTP
        layer check but the login itself will fail with
        ``'Invalid username or password'`` unless a separate
        ``test_register`` call has already seeded the ``Nuharilwan``
        account in the same database session. Consider aligning
        credentials with the fixture to make this test self-contained.

    Args:
        client (flask.testing.FlaskClient): The test client provided by
            :func:`~tests.conftest.client`.
        test_user (app.models.User): The seeded user provided by
            :func:`~tests.conftest.test_user`. Declared to ensure the
            database is initialised, but not directly used.
    """
    response = client.post(
        '/login',
        data={
            'username': 'Nuharilwan',
            'password': 'Nuharilwan@24',
        },
        follow_redirects=True,
    )
    assert response.status_code == 200


def test_login_wrong_password(client, test_user):
    """Login endpoint flashes an error message for an incorrect password.

    Posts a valid username with the wrong password to ``/login`` and
    asserts that the response body contains the expected error string,
    confirming that failed authentication is surfaced to the user
    rather than silently succeeding or returning an error status code.

    Args:
        client (flask.testing.FlaskClient): The test client provided by
            :func:`~tests.conftest.client`.
        test_user (app.models.User): The seeded user provided by
            :func:`~tests.conftest.test_user`. Declares a database
            dependency; credentials must match a seeded account for the
            username-found / password-wrong branch to be reached.
    """
    response = client.post(
        '/login',
        data={
            'username': 'Nuharilwan',
            'password': 'Nuharilwan@11',
        },
        follow_redirects=True,
    )
    assert b'Invalid username or password' in response.data

# contact form

def test_contact_form_valid(app):
    """ContactForm validates successfully when all fields are correctly filled.

    Instantiates :class:`~app.main.forms.ContactForm` inside a test
    request context (required for WTForms CSRF machinery) with a full
    set of valid field values and asserts that ``validate()`` returns
    ``True``.

    Note:
        This definition supersedes the earlier ``test_contact_form_valid``
        defined without an application context in this module. The
        earlier definition is unreachable and should be removed.

    Args:
        app (flask.Flask): The test application instance provided by
            :func:`~tests.conftest.app`, used to push a request context.
    """
    with app.test_request_context():
        form = ContactForm(data={
            'name': 'Nuha',
            'email': 'nuha@gmail.com',
            'subject': 'Hello',
            'message': 'This is a valid message body',
        })
        assert form.validate()


def test_contact_form_missing_name(app):
    """ContactForm fails validation when the name field is empty.

    Submits a form payload with an empty ``name`` and asserts that
    ``validate()`` returns ``False``, confirming that the
    :class:`~wtforms.validators.DataRequired` constraint on
    :attr:`~app.main.forms.ContactForm.name` is enforced.

    Args:
        app (flask.Flask): The test application instance provided by
            :func:`~tests.conftest.app`, used to push an application
            context.
    """
    with app.app_context():
        form = ContactForm(data={
            'name': '',
            'email': 'nuha@gmail.com',
            'subject': 'Hello',
            'message': 'This is a valid message body',
        })
        assert form.validate() is False


def test_contact_form_short_message(app):
    """ContactForm fails validation when the message body is below the minimum length.

    Submits a message of fewer than 10 characters and asserts that
    ``validate()`` returns ``False``, confirming that the
    :class:`~wtforms.validators.Length` ``min=10`` constraint on
    :attr:`~app.main.forms.ContactForm.message` is enforced.

    Args:
        app (flask.Flask): The test application instance provided by
            :func:`~tests.conftest.app`, used to push an application
            context.
    """
    with app.app_context():
        form = ContactForm(data={
            'name': 'Nuha',
            'email': 'nuha@gmail.com',
            'subject': 'Hello',
            'message': 'short',
        })
        assert form.validate() is False


def test_contact_form_missing_subject(app):
    """ContactForm fails validation when the subject field is empty.

    Submits a form payload with an empty ``subject`` and asserts that
    ``validate()`` returns ``False``, confirming that the
    :class:`~wtforms.validators.DataRequired` constraint on
    :attr:`~app.main.forms.ContactForm.subject` is enforced.

    .. warning::
        The ``assert form.validate() is False`` call is currently
        positioned *outside* the ``with app.app_context():`` block,
        meaning it executes without an active application context. Move
        the assertion inside the block to ensure consistent behaviour::

            with app.app_context():
                form = ContactForm(data={...})
                assert form.validate() is False   # ← inside the block

    Args:
        app (flask.Flask): The test application instance provided by
            :func:`~tests.conftest.app`, used to push an application
            context.
    """
    with app.app_context():
        form = ContactForm(data={
            'name': 'Nuha',
            'email': 'nuha@gmail.com',
            'subject': '',
            'message': 'This is a valid message body',
        })
    assert form.validate() is False


def test_logout(client, test_user):
    """Logout endpoint redirects successfully and returns 200.

    Logs in via ``/login`` and then issues a ``GET /logout``, following
    the redirect. Asserts ``200 OK`` on the final response, confirming
    the session was cleared and the user was returned to a reachable
    page (typically ``main.index``).

    Note:
        The login attempt uses ``Nuharilwan`` credentials which, as in
        :func:`test_login`, do not match the
        :func:`~tests.conftest.test_user` fixture. The logout assertion
        will still pass (``/logout`` is a no-op when no session is
        active), but the test does not verify that an authenticated
        session was actually terminated. Aligning credentials with the
        fixture would make this a meaningful round-trip test.

    Args:
        client (flask.testing.FlaskClient): The test client provided by
            :func:`~tests.conftest.client`.
        test_user (app.models.User): The seeded user provided by
            :func:`~tests.conftest.test_user`. Declares a database
            dependency; not directly referenced.
    """
    client.post('/login', data={
        'username': 'Nuharilwan',
        'password': 'Nuharilwan@24',
    })
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200