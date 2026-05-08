==============================
Introduction to Flask-Migrate
==============================

Overview
=========

SignBridge uses Flask-migrate to manage database schema changes. It uses Alembic and integrates with Flask-SQLAlchemy, allowing you to make changes to the database scheme without losing data. 

Migrations files are in the ``migrations/versions/`` folder. Each migration has an ``upgrade()`` and ``downgrade()`` function.

Current Migration
=================

The initial migration (``25738a72190b``) creates the following tables:

* ``user``
* ``room``
* ``message``
* ``room_participant``
* ``transcript``

Workflow
=================

Whenever you make changes to the file ``model.py``, follow these steps:

1. Make the changes you want to your ``models.py``.
2. Run ``flask db migrate -m "Description"`` to generate the migration script.
3. Review the generated file in ``migrations/versions/`` to make sure everything looks correct.
4. Run ``flask db upgrade`` to apply it.

.. Warning::

    Always review the auto-generated migrations before applying it. Alembic sometimes misses changes or generates incorrect SQL. particularly for complex relationships.

Local vs Production
===================

* **Local (SQLite)**: run ``flask db upgrade`` directly in your terminal.
* **Production (PostgreSQL)**: run ``flask db upgrade`` from the Shell tab in the Render dashboard after deploying.

Resetting the database
======================

To wipe and rebuild the database from scratch locally:


.. code-block:: bash
    rm app.db
    rm -rf migrations
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade

.. Warning::
    This deletes all data. Never do this in production

