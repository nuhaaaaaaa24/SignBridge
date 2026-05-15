"""Integration tests for the API blueprint.

Covers token issuance and the two protected resource endpoints
(``/api/users`` and ``/api/rooms``). All requests that require Basic
Auth use the pre-encoded credentials for the ``test_user`` fixture
(``testuser:password123``).

Note:
    The Base64 string ``dGVzdHVzZXI6cGFzc3dvcmQxMjM=`` decodes to
    ``testuser:password123`` and must stay in sync with the credentials
    set in the :func:`~tests.conftest.test_user` fixture. If those
    credentials change, re-encode with::

        python -c "import base64; print(base64.b64encode(b'testuser:password123').decode())"
"""

import json


def test_get_token(client, test_user):
    """Token endpoint issues a bearer token for valid Basic Auth credentials.

    Sends a ``POST`` to ``/api/tokens`` with a pre-encoded Basic Auth
    header and asserts that the response is ``200 OK`` and the JSON body
    contains a ``token`` key.

    Args:
        client (flask.testing.FlaskClient): The test client provided by
            :func:`~tests.conftest.client`.
        test_user (app.models.User): The seeded user whose credentials
            are encoded in the Authorization header, provided by
            :func:`~tests.conftest.test_user`.
    """
    response = client.post(
        '/api/tokens',
        headers={'Authorization': 'Basic dGVzdHVzZXI6cGFzc3dvcmQxMjM='},
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'token' in data


def test_get_users_without_token(client):
    """User list endpoint rejects unauthenticated requests with 401.

    Sends a ``GET`` to ``/api/users`` with no Authorization header and
    asserts that the API returns ``401 Unauthorized``, confirming that
    the endpoint is not publicly accessible.

    Args:
        client (flask.testing.FlaskClient): The test client provided by
            :func:`~tests.conftest.client`.
    """
    response = client.get('/api/users')
    assert response.status_code == 401


def test_get_users_with_token(client, test_user):
    """User list endpoint returns 200 for a valid bearer token.

    Performs a two-step flow: first obtains a token via ``POST
    /api/tokens`` using Basic Auth, then uses that token as a Bearer
    credential in a ``GET /api/users`` request. Asserts that the
    authenticated request succeeds with ``200 OK``.

    Args:
        client (flask.testing.FlaskClient): The test client provided by
            :func:`~tests.conftest.client`.
        test_user (app.models.User): The seeded user whose credentials
            are used to obtain the token, provided by
            :func:`~tests.conftest.test_user`.
    """
    token_response = client.post(
        '/api/tokens',
        headers={'Authorization': 'Basic dGVzdHVzZXI6cGFzc3dvcmQxMjM='},
    )
    token = json.loads(token_response.data)['token']

    response = client.get(
        '/api/users',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 200


def test_get_rooms_with_token(client, test_user, test_room):
    """Room list endpoint returns 200 and includes seeded rooms for a valid token.

    Obtains a bearer token via Basic Auth, then issues a ``GET
    /api/rooms`` request with that token. Asserts ``200 OK``,
    confirming both that the endpoint is accessible to authenticated
    users and that the :func:`~tests.conftest.test_room` fixture room
    is visible in the response scope.

    Args:
        client (flask.testing.FlaskClient): The test client provided by
            :func:`~tests.conftest.client`.
        test_user (app.models.User): The room owner whose credentials
            are used to obtain the token, provided by
            :func:`~tests.conftest.test_user`.
        test_room (app.models.Room): A seeded room owned by
            *test_user*, provided by :func:`~tests.conftest.test_room`.
            Declared as a dependency to ensure the room exists in the
            database before the request is made.
    """
    token_response = client.post(
        '/api/tokens',
        headers={'Authorization': 'Basic dGVzdHVzZXI6cGFzc3dvcmQxMjM='},
    )
    token = json.loads(token_response.data)['token']

    response = client.get(
        '/api/rooms',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 200