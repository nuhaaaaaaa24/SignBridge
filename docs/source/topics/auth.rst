.. _auth-overview:

Authentication Overview
=======================

SignBridge has an authentication system which manages all the user life cycles. This includes user registration, login, session management, and secure password reset mechanism. It features a token-base system for securing the REST API. 

The core logic for authentication is primarily located in ``app/auth/routes.py`` and the ``User`` model in ``app/models.py``.

Key Features
------------

*   **Login and Registration**: Standard flows for new user registration and existing user logins.
*   **Secure Password Hashing**: User passwords are never stored in plaintext. They get securely hashed with ``Flask-bcrypt``.
*   **Rate Limiting**: Help slow down brute-force attacks and server exhaustion by limiting login, registration, and password reset attempts.
*   **Account Blocking**: Automatically blocks user accounts after too many consecutive failed login attempts.
*   **Password Reset**: A secure, email-based flow for users to reset forgotten passwords using JWT tokens.
*   **API Token Authentication**: The expiring tokens are used to protect API endpoints and they are automatically renewed for active sessions.
