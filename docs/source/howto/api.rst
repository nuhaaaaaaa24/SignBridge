=================
API How-To Guides
=================

How to obtain an API token
==========================

.. code-block:: bash

   curl -X POST http://localhost:5000/api/tokens \
     -u your_username:your_password

How to make an authenticated request
======================================

.. code-block:: bash

   curl http://localhost:5000/api/users \
     -H "Authorization: Bearer your-token-here"

How to revoke a token
======================

.. code-block:: bash

   curl -X DELETE http://localhost:5000/api/tokens \
     -H "Authorization: Bearer your-token-here"

How to add a new endpoint
==========================

1. Inside the folder ``app/api/``, choose the relevant file and add a new function. 
2. Decorate it with ``@api_bp.route()`` and ``@token_auth.login_required``.
3. Return a dictionary, where Flask will automatically convert it to JSON.

.. code-block:: python

   @api_bp.route('/example', methods=['GET'])
   @token_auth.login_required
   def get_example_function():
       return {'message': 'hello'}