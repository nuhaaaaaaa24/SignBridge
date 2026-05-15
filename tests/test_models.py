"""Unit tests for ORM model methods and call-room utilities.

Tests in this module operate directly on model instances and service
functions rather than through the HTTP layer, keeping them fast and
independent of routing or template logic.
"""

from app.call.services import generate_room_code
from app.models import User


def test_password_hashing(app):
    """Password hashing and verification work correctly for valid and invalid inputs.

    Constructs an unsaved :class:`~app.models.User` instance, sets a
    password via :meth:`~app.models.User.set_password`, and asserts
    that :meth:`~app.models.User.check_password` returns ``True`` for
    the correct password and ``False`` for an incorrect one. The user
    is not persisted — this test exercises only the bcrypt hashing
    logic.

    Args:
        app (flask.Flask): The test application instance provided by
            :func:`~tests.conftest.app`, used to push an application
            context required by Flask-Bcrypt.
    """
    with app.app_context():
        u = User(username='test', email='t@t.com')
        u.set_password('mypassword')
        assert u.check_password('mypassword') is True
        assert u.check_password('wrongpassword') is False


def test_token_generation(app, test_user):
    """Token generation produces a 32-character string that is immediately verifiable.

    Re-fetches the :func:`~tests.conftest.test_user` by primary key
    within the active session (required because SQLAlchemy model
    instances are not safe to share across sessions), calls
    :meth:`~app.models.User.get_token`, and asserts three properties:

    - The returned value is not ``None``.
    - It is exactly 32 characters long, matching the token format
      defined in :class:`~app.models.User`.
    - :meth:`~app.models.User.check_token` can immediately verify
      the token and returns a non-``None`` result.

    Args:
        app (flask.Flask): The test application instance provided by
            :func:`~tests.conftest.app`, used to push an application
            context.
        test_user (app.models.User): The seeded user provided by
            :func:`~tests.conftest.test_user`. Only its primary key is
            used; the instance itself is not referenced directly inside
            the context.
    """
    with app.app_context():
        from extensions import db
        u = db.session.get(User, test_user.id)
        token = u.get_token()
        assert token is not None
        assert len(token) == 32
        assert User.check_token(token) is not None


def test_room_code_format():
    """Generated room codes conform to the expected ``XXXX-0000`` format.

    Calls :func:`~app.call.services.generate_room_code` and splits the
    result on ``'-'``. Asserts that:

    - The code contains exactly two hyphen-separated segments.
    - The first segment (letters) is exactly 4 characters.
    - The second segment (digits) is exactly 4 characters.

    No application context is required because
    :func:`~app.call.services.generate_room_code` performs no database
    queries and has no Flask dependencies.
    """
    code = generate_room_code()
    parts = code.split('-')
    assert len(parts) == 2
    assert len(parts[0]) == 4
    assert len(parts[1]) == 4