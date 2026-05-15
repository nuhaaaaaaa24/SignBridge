================================
Running Migrations in Production
================================

Overview
========

After deploying to Render, database migrations must be run manually to apply any schema changes.

Running Migrations
==================

Migrations are run locally and pushed to GitHub

1. Make changes to your ``model.py`` 
2. Generate the migration locally:

.. code-block:: bash

   flask db migrate -m "describe your change"

3. Commit and push the updated codes to GitHub:

.. code-block:: bash

    git add .
    git commit -m "message"
    git push -u origin main

.. Note::
    You may have to manually redeploy in Render once the changes are committed to GitHub.

If the Revision ID Changes
==========================

If revision ID is out of sync, which can be due to resetting migrations locally, follow these steps:

.. code-block:: bash

   rm app.db
   rm instance/app.db
   rm -rf migrations
   flask db init
   flask db migrate -m "initial migration"
   flask db upgrade

Then push to GitHub:

.. code-block:: bash
    git add .
    git commit -m "message"
    git push -u origin main

.. Warning::
    This will wipe the database clean and you will have to repopulate the database from scratch.

After Every Deploy
==================

If you made any changes to ``models.py`` in your deployment: 

1. Generate the migration locally

.. code-block:: bash

   flask db migrate -m "comment"

2. Commit and push the migration files in ``migration/versions/``

3. After Render deploys, run ``flask db upgrade`` from the shell tab.

.. Warning::
    Never run ``flask db downgrade`` or delete files in production as this can cause data loss.

If a Migration Fails
====================

If ``flask db upgrade`` fails in production:

1. Check the error message as it usually tells you which column or table caused the issue.
2. Fix migration script locally and push again.