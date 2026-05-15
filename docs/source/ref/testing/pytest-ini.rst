=================
pytest.ini
=================

Overview
========

SignBridge uses a minimal ``pytest.ini`` configuration file to set up testing at the root of the project.

.. code-block:: ini

   [pytest]
   pythonpath = .

``pythonpath = .`` adds the project root to Python's path so that imports
like ``from app.models import User`` work correctly in tests without needing
to install the package. 