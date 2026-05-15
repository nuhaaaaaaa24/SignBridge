===================
REST API Reference
===================

Overview
========

SignBridge exposes a REST API under the ``api/`` blueprint for programmatic access to users, rooms, and tokens. All endpoints require authentication.

Tokens
========

``POST /api/tokens``
--------------------

Obtain an API token. Requires Basic Auth.

.. code-block:: text

    POST /api/tokens

Returns:

.. code-block:: JSON

    {"token": "your token here"}

``DELETE /api/tokens``
--------------------

Revokw the current token. Requires Bearer Tokens

.. code-block:: JSON

    DELETE /api/tokens

Returns ``204 Not content``

Users
========

``GET /api/users``
------------------

Returns all registered users. Requires Bearer Token

.. code-block:: text

   GET /api/users

Returns:

.. code-block:: text

    {"items": [...], "total": 2}

``GET /api/users/<id>``
-----------------------

Returns a single user by ID. Requires Bearer Tokens

.. code-block:: text

   GET /api/users/1

Returns ``404`` if the user does not 

Rooms
========

``GET /api/rooms``
-----------------------

Returns all rooms created in the system. Requires bearer Tokens

.. code-block:: text

   GET /api/rooms

Returns:

.. code-block:: json

   {"items": [...], "total": 5}

``GET /api/rooms/<id>``
-----------------------

Returns a single room by ID. Requires Bearer Tokens

.. code-block:: text

   GET /api/rooms/1

Returns 404 if the room does not exist.

``GET /api/rooms/<id>/messages``
---------------------------------

Returns the messages sent in one particular room. Requires Bearer Tokens

.. code-block:: text

   GET /api/rooms/1/messages

Returns:

.. code-block:: json

   {"items": [...], "total": 10}

Error Responses
===============

All errors return a JSON response in this format:

.. code-block:: json

   {"error": "bad request", "message": "..."}

Common status codes:

* ``400`` — Bad request
* ``401`` — Unauthorized, invalid or missing credentials
* ``404`` — Resource not found
* ``429`` — Rate limit exceeded