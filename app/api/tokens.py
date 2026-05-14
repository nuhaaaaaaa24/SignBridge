'''
app/auth/tokens.py
Created by Nuha Rilwan
Last modified 22/04/2026


'''

from extensions import db
from app.api import api_bp
from app.api.auth import basic_auth, token_auth

# POST /api/tokens
# Requires HTTP Basic Auth (username + password).
# Generates and returns a bearer token for the authenticated user.
# Token expires after 1 hour but is auto-renewed if still valid.
@api_bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return {'token': token}

# DELETE /api/tokens
# Requires bearer token auth.
# Revokes the current user's token by setting its expiration to the past.
# Returns 204 No Content on success.
@api_bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    token_auth.current_user().revoke_token()
    db.session.commit()
    return '', 204