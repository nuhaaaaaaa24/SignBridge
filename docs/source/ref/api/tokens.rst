====================
Token Authentication
====================

Overview
--------

Provides two REST endpoints for managing bearer tokens used in token-based
authentication. Tokens are issued against valid HTTP Basic credentials and
can be explicitly revoked by an authenticated token holder.

Endpoints
---------

POST /tokens
--------------

Issues a new bearer token for the authenticated user.

- **Authentication:** HTTP Basic (``Authorization: Basic <token>``)
- **Request body:** None
- **Decorator:** ``@basic_auth.login_required``

**Response**

.. code-block:: json

   {
     "token": "<bearer-token-string>"
   }

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Status
     - Meaning
   * - ``200 OK``
     - Token created and returned.
   * - ``401 Unauthorized``
     - Missing or invalid Basic Auth credentials.

**Example**

.. code-block:: bash

   curl -X POST https://example.com/api/tokens \
        -u username:password

----

DELETE /tokens
--------------

Revokes the current bearer token, invalidating it immediately.

- **Authentication:** Bearer Token (``Authorization: Bearer <token>``)
- **Request body:** None
- **Decorator:** ``@token_auth.login_required``

**Response**

Empty body, ``204 No Content``.

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Status
     - Meaning
   * - ``204 No Content``
     - Token successfully revoked.
   * - ``401 Unauthorized``
     - Missing or invalid bearer token.

**Example**

.. code-block:: bash

   curl -X DELETE https://example.com/api/tokens \
        -H "Authorization: Bearer <token>"

