Route Protection
----------------
 
To protect API routes you have to use ``@token_auth.login_required`` on all protected routes. Basic Auth is
only for ``POST /tokens``, every other endpoint should require a bearer token.
 
**Standard protected route**
 
.. code-block:: python
 
   @api_bp.route('/some-resource', methods=['GET'])
   @token_auth.login_required
   def get_resource():
       user = token_auth.current_user()
       ...
 
**Accessing the current user**
 
.. list-table::
   :widths: 40 60
   :header-rows: 1
 
   * - Context
     - Call
   * - Inside a token-protected route
     - ``token_auth.current_user()``
   * - Inside ``POST /tokens`` only
     - ``basic_auth.current_user()``