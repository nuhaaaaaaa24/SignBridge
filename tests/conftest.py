"""Shared pytest fixtures for the application test suite.

Provides the base :func:`app`, :func:`client`, and :func:`runner`
fixtures that configure an isolated Flask application for each test,
plus higher-level fixtures that seed common database state.

All database fixtures operate within the application context opened by
:func:`app` and must list ``app`` (or a fixture that depends on it) as
an argument to ensure that context is active — they should never open
a second ``app_context`` themselves.

Note:
    CSRF protection is disabled globally (``WTF_CSRF_ENABLED=False``)
    so that test clients can submit forms without generating valid
    tokens. This is intentional and must not be changed without
    updating every form-submitting test accordingly.
"""

import pytest

from app import create_app
from app.models import Room, User
from extensions import db


@pytest.fixture
def app():
    """Create and configure a Flask application instance for testing.

    Overrides the following configuration keys after construction so
    that tests are fully isolated from any production environment:

    - ``TESTING`` → ``True``: enables Flask's test-mode error
      propagation.
    - ``SQLALCHEMY_DATABASE_URI`` → ``sqlite:///:memory:``: each test
      session gets a fresh in-memory database that is dropped on
      teardown.
    - ``WTF_CSRF_ENABLED`` → ``False``: disables CSRF token validation
      so test clients can POST forms freely.
    - ``SECRET_KEY`` → a fixed test string (session signing does not
      need to be secure in tests).
    - ``MAIL_SERVER`` → ``None``: prevents any email dispatch during
      tests.

    Yields:
        flask.Flask: The configured application instance inside an
        active :meth:`~flask.Flask.app_context`. All tables are created
        before yielding and dropped on teardown (in-memory database
        only).
    """
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key',
        'MAIL_SERVER': None,
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        if app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:':
            db.drop_all()


@pytest.fixture
def client(app):
    """Return a test client for the application.

    Args:
        app (flask.Flask): The test application instance provided by
            :func:`app`.

    Returns:
        flask.testing.FlaskClient: A client that can issue HTTP requests
        against the application without starting a real server.
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """Return a CLI test runner for the application.

    Args:
        app (flask.Flask): The test application instance provided by
            :func:`app`.

    Returns:
        flask.testing.FlaskCliRunner: A runner that can invoke Click
        commands registered on the application via ``@app.cli.command``
        or ``flask.cli``.
    """
    return app.test_cli_runner()


@pytest.fixture
def test_user(app):
    """Seed a standard (non-admin) test user into the database.

    The ``app`` argument is declared to guarantee the application
    context opened by :func:`app` is active — do not open a second
    ``app_context`` inside this fixture.

    Args:
        app (flask.Flask): The test application instance. Used only to
            ensure context activation; not referenced directly.

    Returns:
        app.models.User: The persisted :class:`~app.models.User`
        instance with ``username='testuser'``,
        ``email='test@test.com'``, and password ``'password123'``.
    """
    user = User(username='testuser', email='test@test.com')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def logged_in_owner(client, test_user):
    """Seed a test user and authenticate them via the login endpoint.

    Posts credentials to ``/auth/login`` through the test client so
    that the resulting session cookie is retained for subsequent
    requests made with the same *client*. Tests that need an
    authenticated session should depend on this fixture rather than
    logging in manually.

    Args:
        client (flask.testing.FlaskClient): The test client provided
            by :func:`client`.
        test_user (app.models.User): The seeded user provided by
            :func:`test_user`.

    Returns:
        app.models.User: The authenticated :class:`~app.models.User`
        instance, identical to the one returned by :func:`test_user`.
    """
    client.post('/auth/login', data={
        'username': test_user.username,
        'password': 'password123',
    })
    return test_user


@pytest.fixture
def test_room(app, test_user):
    """Seed a call room owned by the test user into the database.

    The ``app`` argument is declared to guarantee the application
    context opened by :func:`app` is active — do not open a second
    ``app_context`` inside this fixture.

    Args:
        app (flask.Flask): The test application instance. Used only to
            ensure context activation; not referenced directly.
        test_user (app.models.User): The room owner, provided by
            :func:`test_user`.

    Returns:
        app.models.Room: The persisted :class:`~app.models.Room`
        instance with ``room_code='TEST-1234'`` and
        ``owner_id=test_user.id``.
    """
    room = Room(room_code='TEST-1234', owner_id=test_user.id)
    db.session.add(room)
    db.session.commit()
    return room