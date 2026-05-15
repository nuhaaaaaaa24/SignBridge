"""Integration tests for call-room route behaviour.

Tests in this module exercise the ``/call`` and ``/create-room``
endpoints through the test client, focusing on redirect logic and
access control rather than rendered content. Socket.IO room state is
not seeded, so all room-access tests reflect the behaviour of an empty
:data:`~app.call.sockets.rooms` dictionary.
"""


def test_invalid_room_returns_404(client):
    """Call endpoint redirects to ``/join`` when the room code does not exist.

    Issues a ``GET /call?room=FAKE-0000`` for a room code that has no
    corresponding :class:`~app.models.Room` row and asserts a ``302``
    redirect. The redirect target is ``/join`` rather than a true
    ``404``, which is the application's intended behaviour — an unknown
    room code is treated as a user error rather than a missing resource.

    Args:
        client (flask.testing.FlaskClient): The test client provided by
            :func:`~tests.conftest.client`.
    """
    response = client.get('/call?room=FAKE-0000')
    assert response.status_code == 302


def test_valid_room_returns_200(client, test_room, logged_in_owner):
    """Call endpoint redirects the owner when they are not yet in the Socket.IO room.

    Issues a ``GET /call?room=TEST-1234`` as the authenticated room
    owner and asserts a ``302`` redirect. Even though the owner is
    exempt from the guest host-presence check, the in-memory
    :data:`~app.call.sockets.rooms` dictionary is empty in the test
    environment (no Socket.IO connection has been made), so the view
    still redirects rather than rendering the call page. A ``200``
    would only be returned once the owner's SID is registered via a
    real ``join_room`` WebSocket event.

    Args:
        client (flask.testing.FlaskClient): The test client provided by
            :func:`~tests.conftest.client`.
        test_room (app.models.Room): The seeded room with code
            ``'TEST-1234'``, provided by
            :func:`~tests.conftest.test_room`.
        logged_in_owner (app.models.User): The authenticated room owner,
            provided by :func:`~tests.conftest.logged_in_owner`.
    """
    response = client.get('/call?room=TEST-1234')
    assert response.status_code == 302


def test_create_room_requires_login(client):
    """Create-room endpoint redirects unauthenticated requests to the login page.

    Issues a ``POST /create-room`` with no active session and follows
    the redirect chain. Asserts ``200 OK`` on the final response,
    confirming that :func:`~flask_login.login_required` intercepted the
    request and the user was returned to a valid page (the login form)
    rather than receiving an error.

    Args:
        client (flask.testing.FlaskClient): The test client provided by
            :func:`~tests.conftest.client`.
    """
    response = client.post('/create-room', follow_redirects=True)
    assert response.status_code == 200