================
PostgreSQL Setup
================

Overview
========
PostgreSQL can be used for both local development and production on Render. Unlike SQLite, however,
PostgreSQL requires a running database server. This guide covers setup for both environments.

.. note::

   Ensure you have PostgreSQL installed locally before proceeding with the local setup.

   On Windows: Download the installer from `PostgreSQL.org <https://www.postgresql.org/download/windows/>`_

   On macOS: ``brew install postgresql@18``

   On Linux: ``sudo apt install postgresql``

----

Local Development
=================

Create the Database
-------------------

Start the PostgreSQL service and create a database for the project:

.. code-block:: bash

   # macOS (Homebrew)
   brew services start postgresql@18

   # Linux
   sudo service postgresql start

Then open the PostgreSQL shell and create the database and user:

.. code-block:: bash

   psql postgres

.. code-block:: 

   CREATE DATABASE your_db_name;
   CREATE USER your_db_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_db_user;
   \q

Configure Environment Variables
--------------------------------

Set ``DATABASE_URL`` in your ``.env`` file:

.. code-block:: text

   DATABASE_URL=postgresql://your_db_user:your_password@localhost:5432/your_db_name

Run Migrations
--------------

.. code-block:: bash

   flask db upgrade

Resetting the Local Database
-----------------------------

To wipe and rebuild from scratch:

.. code-block:: bash

   psql postgres -c "DROP DATABASE your_db_name;"
   psql postgres -c "CREATE DATABASE your_db_name;"
   psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_db_user;"

   rm -rf migrations
   flask db init
   flask db migrate -m "initial migration"
   flask db upgrade

.. warning::

   This deletes all data. Never do this in production!

Viewing the Local Database
--------------------------

Use the flask shell to inspect data:

.. code-block:: bash

   flask shell

.. code-block:: python

   from app.models import User
   users = User.query.all()
   for u in users:
       print(u.id, u.username, u.email, u.is_admin)

Or connect directly via ``psql``:

.. code-block:: bash

   psql postgresql://your_db_user:your_password@localhost:5432/your_db_name

.. code-block:: text

   \dt               -- list all tables
   SELECT * FROM user;
   \q                -- quit

----

Creating a PostgreSQL Database with Render
==========================================

Create Render Postgres Instance
-------------------------------

1. Log in to `Render <https://render.com>`_ and go to your dashboard.
2. Click **New** → **PostgreSQL**.
3. Fill in the details:

   - **Name**: choose a name (e.g. ``myapp-db``)
   - **Region**: match the region of your web service
   - **Plan**: Free (or paid for persistence beyond 90 days)

4. Click **Create Database**.
5. Once provisioned, open the database page and copy the **Internal Database URL** -
   use this for services running within Render.

   Use the **External Database URL** only for connecting from outside Render
   (e.g. from your local machine or a database GUI).

Configure Environment Variables on Render
------------------------------------------

In your Render **Web Service** settings:

1. Go to **Environment** → **Environment Variables**.
2. Add a new variable:

   .. code-block:: text

      DATABASE_URL=<paste Internal Database URL here>

   .. note::

      Render's PostgreSQL URL uses the ``postgres://`` scheme. SQLAlchemy requires
      ``postgresql://``. SignBridge automatically modifies the scheme if necessary.


Viewing the Production Database
--------------------------------

To inspect data on Render, connect using the **External Database URL** from your
local machine:

.. code-block:: bash

   psql <External Database URL>

.. code-block:: text

   \dt
   SELECT * FROM user;
   \q

You can also use a GUI tool such as `pgAdmin <https://www.pgadmin.org/>`_.

.. warning::

   Never run destructive commands (``DROP TABLE``, ``DELETE FROM``, etc.) against
   the production database without a backup.
