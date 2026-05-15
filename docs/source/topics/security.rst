=================
Security Overview
=================

Overview
========

Security is a critical component of the SignBridge application due to its use
of real-time communication, authentication systems, and user account
management.

The application implements multiple security controls to help protect user
accounts, reduce abuse of data and the application, and maintain secure communication 
between the client and server.

Implemented Security Features
=============================

The SignBridge security architecture includes:

* CSRF protection using Flask-WTF
* password hashing using Flask-Bcrypt
* endpoint-specific rate limiting
* account lockout protection
* session timeout management
* browser-level security headers
* role-based access control (RBAC)
* Google reCAPTCHA v2 integration

Authentication Security
=======================

Authentication-related protections include:

* strong password policies
* password hashing with salting
* brute-force protection through rate limiting
* automated account lockout after repeated failed login attempts

These controls help reduce the risk of:

* credential guessing
* automated attacks
* credential stuffing
* unauthorised access

Session Security
================

The application implements session timeout protection to reduce the risk of
unauthorised access from unattended devices.

Inactive sessions automatically expire after a period of inactivity.

Browser Security
================

Browser-level protections are implemented using HTTP security headers.

Examples:

* Strict-Transport-Security (HSTS)
* X-Frame-Options
* X-Content-Type-Options

These headers help reduce vulnerabilities such as:

* clickjacking
* MIME type sniffing
* man-in-the-middle attacks

Privacy Considerations
======================

The machine learning inference pipeline primarily operates client-side using
TensorFlow.js.

Video data is processed locally within the browser and is not permanently
stored on the server.

The application only stores essential user account information such as:

* username
* email address
* hashed passwords