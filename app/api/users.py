'''
app/auth/users.py
Created by Nuha Rilwan
Last modified 22/04/2026


'''

import sqlalchemy as sa
from flask import request
from extensions import db
from app.models import User
from app.api import api_bp
from app.api.auth import token_auth
from app.api.errors import bad_request

@api_bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    users = db.session.scalars(sa.select(User)).all()
    return {'items': [u.to_dict() for u in users], 'total': len(users)}

@api_bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return db.get_or_404(User, id).to_dict()