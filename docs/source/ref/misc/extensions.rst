Extensions Reference
====================

.. automodule:: extensions
    :members:

This page provides an overview of the extensions used in SignBridge, including their purpose. 

Flask-SQLAlchemy
------------------

* SQLAlchemy lets you define database tables as Pyhton classes instead of writing raw SQL. 
* All models are defined in ``models.py``. 

Flask-migrate
------------------

* Handle database schema changes safely using using Alembic. 
* Wihtout it, every time you add a column or table you'd have to drop and recreate the database, which means you lose all the data.

Flask-login
------------------

* Manages user sessions. 
* Tracking who is logged in, protecting routes with ``@login_required``. 
* Handles the login/logout flow.

Flask-login
------------------

* Adds CSRF protection to all forms. 
* Form classes are defined in each blueprint's ``forms.py``

Flask-mail
------------------

* Handles sending emails through the app
* Mainly used for **reset password** links. 

Flask-moment
------------------

* Moment converts UTC timestamps stored in the database to the user's local timezone in the browser. 

FLask-limiter
------------------

* Limiter prevents brute force attacks by limiting the number of requests a user or IP can make in a time window.
* Applied to authentication and API routes. 

FLask-SocketIO
------------------

* Used as a signalling server for WebRTC connection establishment.
* Also handles real-time chat messaging between users in a call room. 

Flask-bcrypt
------------------

* Designed specifically for password hashing.
* Used when registering and authenticating users. 


Flask-httpauth
------------------

* Token-based authentication for protecting REST API endpoints.