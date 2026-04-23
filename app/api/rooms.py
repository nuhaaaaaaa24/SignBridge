'''
app/auth/rooms.py
Created by Nuha Rilwan
Last modified 22/04/2026


'''

import sqlalchemy as sa
from flask import request
from extensions import db
from app.models import Room, Message
from app.api import api_bp
from app.api.auth import token_auth
from app.api.errors import bad_request

@api_bp.route('/rooms', methods=['GET'])
@token_auth.login_required
def get_rooms():
    rooms = db.session.scalars(sa.select(Room)).all()
    return {'items': [r.to_dict() for r in rooms], 'total': len(rooms)}

@api_bp.route('/rooms/<int:id>', methods=['GET'])
@token_auth.login_required
def get_room(id):
    return db.get_or_404(Room, id).to_dict()

@api_bp.route('/rooms/<int:id>/messages', methods=['GET'])
@token_auth.login_required
def get_room_messages(id):
    room = db.get_or_404(Room, id)
    messages = db.session.scalars(
        sa.select(Message)
        .where(Message.room_id == room.id)
        .order_by(Message.created_at.asc())
    ).all()
    return {'items': [m.to_dict() for m in messages], 'total': len(messages)}