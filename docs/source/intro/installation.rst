Installation (local)
====================================

To run this on a local development server, you will need to set the environment variables defined in ``config.py``.

If you do not know how to do this, contact Shivangi at https://github.com/ssrithw/ or ssrith@proton.me for assistance.

1) Clone the repository to your local drive
-------------------------------------------

.. code-block:: bash

   git clone https://github.com/nuhaaaaaaa24/SignBridge.git

2) Navigate to the folder you just created
------------------------------------------

.. code-block:: bash

   cd your/path/here/SignBridge

3) Create a Python virtual environment
---------------------------------------

In your terminal, run the following command:

.. code-block:: bash

   python3 -m venv venv

4) Activate the virtual environment
------------------------------------

Windows Command Prompt:

.. code-block:: bash

   venv\Scripts\activate

Windows PowerShell:

.. code-block:: bash

   venv\Scripts\Activate.ps1

macOS:

.. code-block:: bash

   source venv/bin/activate

Linux:

.. code-block:: bash

   source venv/bin/activate

5) Install the required dependencies
-------------------------------------

Run ONE of the following commands:

.. code-block:: bash

   pip install -r requirements.txt

or:

.. code-block:: bash

   python3 -m pip install -r requirements.txt

6) Run the development server
-----------------------------

.. code-block:: bash

   python signbridge.py

Testing
-------

Pytest (excluding Selenium tests):

.. code-block:: bash

   pytest tests/ --ignore=tests/test_selenium.py -v

Selenium tests:

.. code-block:: bash

   pytest tests/test_selenium.py -v