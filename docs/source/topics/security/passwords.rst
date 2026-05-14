================
Password Hashing
================

Overview
========

SignBridge does not store raw user passwords directly in the database.

Instead, the application uses Flask-Bcrypt to securely hash passwords before
storage.

This helps protect user credentials in case the database is compromised.

Bcrypt Hashing
==============

The application uses the bcrypt hashing algorithm provided by Flask-Bcrypt.

Bcrypt is a one-way cryptographic hashing algorithm designed specifically for
password security.

Hashed passwords cannot realistically be reversed back into their original
plain text form.

Salting
=======

Bcrypt automatically applies a unique salt to each password before hashing.

A salt is a randomly generated sequence of characters added to the password
during the hashing process.

This ensures that:

* identical passwords produce different hashes
* rainbow table attacks become significantly more difficult

Password Verification
=====================

When a user logs in:

1. the submitted password is hashed again
2. the generated hash is compared against the stored hash
3. authentication succeeds only if the hashes match

The original password is never retrieved from the database.

Example
=======

Password hashing workflow:

.. code-block:: python

   from flask_bcrypt import Bcrypt

   bcrypt = Bcrypt()

   password_hash = bcrypt.generate_password_hash(password)

Password verification:

.. code-block:: python

   bcrypt.check_password_hash(password_hash, password)

Security Benefits
=================

Password hashing helps protect against:

* credential leaks
* database breaches
* password theft
* rainbow table attacks