=====================
How to run migrations
=====================

Overview
===============

Listed beloe are the commands you can use to run the migrations from scratch

Common Commands
===============

Initialise migrations (first time only):

.. code-block:: bash

   flask db init

Generate a new migration after changing ``models.py``:

.. code-block:: bash

   flask db migrate -m "message/changes you made"

Apply migrations to the database:

.. code-block:: bash

   flask db upgrade

Roll back the last migration:

.. code-block:: bash

   flask db downgrade

Roll back all migrations to a blank database:

.. code-block:: bash

   flask db downgrade base