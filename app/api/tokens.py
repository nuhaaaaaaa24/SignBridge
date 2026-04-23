'''
app/auth/tokens.py
Created by Nuha Rilwan
Last modified 22/04/2026


'''

from extensions import db
from app.api import api_bp
from app.api.auth import basic_auth, token_auth

@api_bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return {'token': token}

@api_bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    token_auth.current_user().revoke_token()
    db.session.commit()
    return '', 204