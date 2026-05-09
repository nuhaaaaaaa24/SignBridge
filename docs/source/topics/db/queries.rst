===========================
Making Queries with SQLAlchemy
===========================

Overview
========

SignBridge uses SQLAlchemy queries throughout the application.
All queries go through the ``db.session`` object provided by Flask-SQLAlchemy.

.. Note::
   In order to work with queries, you need to open Flask shell with the command ``flask shell``

Import
========

.. code-block:: python

   import sqlalchemy as sa
   from extensions import db
   from app.models import User, Room, Message

To view all users
=================

.. code-block:: python

   query = db.select(User)
   users = db.session.scalars(query)
   for u in users:
      print(u.id, u.username, u.email)


Selecting Multiple Records
==========================

Get all users ordered by username:

.. code-block:: python

   users = User.query.order_by(User.username).all()
   print (users)

Get all rooms:

.. code-block:: python

   rooms = db.session.scalars(sa.select(Room)).all()
   print (rooms)

Adding Records
==============

Add a new user:

.. code-block:: python

   user = User(username="example_name", email="example_email")
   user.set_password("signbridge123456789@") # Adhere to the password policy
   db.session.add(user)
   db.session.commit()

Add an admin user:

.. code-block:: python

   user = User(username="example_name", email="example_email", is_admin=True)
   user.set_password("signbridge123456789@") # Adhere to the password policy
   db.session.add(user)
   db.session.commit()


