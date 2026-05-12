====================
Seeding Initial Data
====================

Overview
========

SignBridge does not have an automated seed script. Initial data such as an
admin user can be created manually via the flask shell.

Creating an Admin User
======================

Open the flask shell:

.. code-block:: bash

   flask shell

To create an admin user, follow the steps below:

.. code-block:: python

   from app.models import User
   from extensions import db

   u = User(username='admin', email='admin@example.com', is_admin=True)
   u.set_password('your-password') # adhere to password policy
   db.session.add(u)
   db.session.commit()

To create a regular user, follow the steps below:

.. code-block:: python

   from app.models import User
   from extensions import db

   u = User(username='regularuser', email='regularuser@example.com', is_admin=False)
   u.set_password('your-password') # adhere to password policy
   db.session.add(u)
   db.session.commit()

Verifying
=========

You can verify the user was created successfully:

.. code-block:: python

   from app.models import User
   u = User.query.filter_by(username='admin').first()
   print(u.username, u.is_admin)

.. warning::

   Use a strong password for the admin account, especially in production.