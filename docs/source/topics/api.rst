===============
Authentication
===============

The API supports two different authentication methods:

Basic Auth
----------------

* **Basic Auth** - Used only to obtain a token via ``POST /api/tokens``. Pass your username and password.

Bearer Tokens
----------------

* **Bearer Tokens** - Used for all other endpoints. Pass the token in the ``Authorization`` header. 

.. code-block:: text

    Authorization: Bearer <your-token>

Token Lifecycle
----------------

* Generated automatically when a user registers to the system.
* Valid for **1 hour** .
* Reused if more than 60 seconds remain on the existing token.
* If less than 30 seconds remain, a new token is generated and the old token is revoked.