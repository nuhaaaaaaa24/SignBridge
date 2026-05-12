.. _auth-tokens:

Generating and Revoking API Tokens
==================================

API tokens are used to authenticate requests to the REST API. The application uses a secure token system where tokens are generated per user, have a defined expiration time, and can be revoked. The core logic is handled by methods within the ``User`` model in ``app/models.py``.

Token Generation
----------------

Tokens are generated using the ``get_token()`` method. A token is automatically created or refreshed upon user registration, login, or when an existing token is close to expiring.

Method Definition
^^^^^^^^^^^^^^^^^
Defines the method for generating a token, with a default expiration of 1 hour (3600 seconds).

.. code-block:: python

    def get_token(self, expires_in=3600):

Existing Token Check
^^^^^^^^^^^^^^^^^^^^
Returns the existing token if it is still valid for more than 60 seconds, avoiding unnecessary regeneration.

.. code-block:: python

    now = datetime.now(timezone.utc)
    if self.token and self.token_expiration and \
        self.token_expiration.replace(tzinfo=timezone.utc) > now + timedelta(seconds=60):
        return self.token

New Token Creation
^^^^^^^^^^^^^^^^^^
Generates a new, cryptographically secure 32-character hexadecimal token.

.. code-block:: python

    self.token = secrets.token_hex(16)

Set Expiration
^^^^^^^^^^^^^^
Sets the expiration timestamp for the new token.

.. code-block:: python

    self.token_expiration = now + timedelta(seconds=expires_in)

Token Revocation
----------------

Revoking a token invalidates it immediately. This is handled by the ``revoke_token()`` method.

Method Definition
^^^^^^^^^^^^^^^^^
Defines the method for revoking a user's current API token.

.. code-block:: python

    def revoke_token(self):

Invalidate Expiration
^^^^^^^^^^^^^^^^^^^^^
Sets the token's expiration date to a time in the past, effectively invalidating it.

.. code-block:: python

    self.token_expiration = datetime.now(timezone.utc) - timedelta(seconds=1)

Token Verification and Auto-Renewal
-----------------------------------

API routes are protected using a token verification mechanism. The static method ``User.check_token()`` is used to validate incoming tokens.

Method Definition
^^^^^^^^^^^^^^^^^
Defines the static method that checks the validity of a given token.

.. code-block:: python

    @staticmethod
    def check_token(token):

User Lookup
^^^^^^^^^^^
Finds the user associated with the provided token.

.. code-block:: python

    user = db.session.scalar(sa.select(User).where(User.token == token))

Expiration Check
^^^^^^^^^^^^^^^^
Returns ``None`` if the user does not exist or if the token has expired.

.. code-block:: python

    if user is None or user.token_expiration.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        return None

