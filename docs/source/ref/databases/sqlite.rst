============================
SQLite for Local Development
============================

Overview
========

SQLite is used for local development. It requires no setup — Flask-SQLAlchemy
creates the ``app.db`` file automatically in the project root when you run
migrations.

Setup
=====

Set ``DATABASE_URL`` in your ``.env`` file:

.. code-block:: text

   DATABASE_URL=sqlite:///app.db

.. Note::

    Please copy the path of your ``app.db`` file and paste it into the ``DATABASE_URL`` value in ``.env``.

Then run:

.. code-block:: bash

   flask db upgrade

The ``app.db`` file will be created in the project root.

Resetting the Database
======================

To wipe and rebuild from scratch:

You need to delete the existing ``app.db`` and the ``migrations`` directory. You can do this manually or with the following commands:

.. code-block:: bash
   
   rm app.db
   rm -rf migrations
   flask db init
   flask db migrate -m "initial migration"
   flask db upgrade

.. warning::

   This deletes all data. Never do this in production.

Viewing the Database
====================

Use the flask shell to inspect data:

.. code-block:: bash

   flask shell

.. code-block:: python

   from app.models import User
   users = User.query.all()
   for u in users:
       print(u.id, u.username, u.email, u.is_admin)