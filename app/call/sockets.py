'''
app/call/sockets.py

Handles WebSocket events for call rooms, including joining/leaving rooms, signaling for WebRTC, and chat messages. Uses in-memory structures to track room participants and persists chat history in the database.
'''

import sqlalchemy as sa
from flask import request
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room
from extensions import db, socketio
from app.models import Room, Message
from threading import Lock
from datetime import datetime, timezone

# ================= STATE =================
rooms       = {}
sid_to_room = {}
room_lock   = Lock()

def _get_room(code: str):
    return db.session.scalar(
        sa.select(Room).where(Room.room_code == code)
    )

def _iso_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

def _sender_name() -> str:
    if current_user and current_user.is_authenticated:
        return current_user.username
    return 'Guest'

def _persist_message(room: Room, content: str) -> None:
    try:
        user_id = current_user.id if (current_user and current_user.is_authenticated) else None
        msg = Message(msg_content=content, user_id=user_id, room_id=room.id)
        db.session.add(msg)
        db.session.commit()
    except Exception:
        db.session.rollback()

def _load_history(room: Room, limit: int = 50) -> list:
    messages = db.session.scalars(
        sa.select(Message)
        .where(Message.room_id == room.id)
        .order_by(Message.created_at.desc())
        .limit(limit)
    ).all()
    messages = list(reversed(messages))
    return [
        {
            'sender': m.user.username if m.user else 'Guest',
            'message': m.msg_content,
            'timestamp': m.created_at.isoformat()
        }
        for m in messages
    ]


# ================= JOIN ROOM =================
@socketio.on('join_room')
def on_join(data):
    code = (data.get('room') or '').strip().upper()
    sid  = request.sid

    if not code:
        emit('error', {'message': 'Missing room code.'})
        return

    room = _get_room(code)
    if not room:
        emit('error', {'message': 'Invalid room code.'})
        return

    with room_lock:
        rooms.setdefault(code, set())
        if sid in rooms[code]:
            participants = len(rooms[code])
        else:
            if len(rooms[code]) >= 2:
                emit('error', {'message': 'Room is full.'})
                return
            rooms[code].add(sid)
            sid_to_room[sid] = code
            participants = len(rooms[code])

    join_room(code)

    # Send chat history to the joining user only
    history = _load_history(room)
    if history:
        emit('chat_history', {'messages': history})

    if participants == 1:
        emit('role', {'role': 'caller'})
    elif participants == 2:
        emit('role', {'role': 'callee'})
        emit('peer_ready', {}, to=code)
        emit(
            'chat_message',
            {'sender': 'system',
             'message': f'{_sender_name()} joined the chat',
             'timestamp': _iso_utc_now()},
            to=code,
            include_self=False
        )


# ================= SIGNALING =================
@socketio.on('signal')
def on_signal(data):
    code = (data.get('room') or '').strip().upper()
    sid  = request.sid

    if sid_to_room.get(sid) != code:
        return
    if code not in rooms:
        return

    emit('signal', data, to=code, include_self=False)


# ================= DISCONNECT CLEANUP =================
@socketio.on('disconnect')
def on_disconnect():
    sid  = request.sid
    name = _sender_name()

    notify = False
    code   = None
    with room_lock:
        code = sid_to_room.pop(sid, None)
        if code and code in rooms:
            rooms[code].discard(sid)
            if not rooms[code]:
                rooms.pop(code, None)
            else:
                notify = True

    if not code:
        return

    try:
        leave_room(code)
    except Exception:
        pass

    if notify:
        emit('peer_left', {}, to=code)
        emit(
            'chat_message',
            {'sender': 'system',
             'message': f'{name} left the chat',
             'timestamp': _iso_utc_now()},
            to=code
        )


# ================= CHAT =================
@socketio.on('chat_message')
def on_chat_message(data):
    code    = (data.get('room') or '').strip().upper()
    message = (data.get('message') or '').strip()
    sid     = request.sid

    if not code or not message:
        return
    if len(message) > 1000:
        message = message[:1000]
    if sid_to_room.get(sid) != code:
        return

    room = _get_room(code)
    if not room:
        return

    sender = _sender_name()
    _persist_message(room, message)

    emit(
        'chat_message',
        {'sender': sender, 'message': message, 'timestamp': _iso_utc_now()},
        to=code,
        include_self=False
    )