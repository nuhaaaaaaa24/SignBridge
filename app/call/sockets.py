"""WebSocket event handlers for call rooms.

Manages the full real-time lifecycle of a call session: participant
joining and departure, WebRTC signalling, chat messaging, and
sign-language transcript relay. All events are handled via
:data:`~extensions.socketio` (Flask-SocketIO over gevent).

**In-memory state**

Room occupancy and session identity are stored in three module-level
dictionaries that are kept consistent under :data:`room_lock`:

- :data:`rooms` — maps each active room code to the set of Socket.IO
  session IDs (SIDs) currently in that room.
- :data:`sid_to_room` — reverse lookup from SID to room code, used
  during disconnect cleanup.
- :data:`sid_to_username` — maps each SID to the display name chosen
  at join time.

Note:
    In-memory state is **process-local**. Deployments that run more
    than one gevent worker process must replace these dictionaries with
    a shared backend (e.g. Redis via Flask-SocketIO's ``message_queue``
    option) to ensure all workers see consistent room state.

Attributes:
    rooms (dict[str, set[str]]): Active room codes mapped to the set of
        SIDs currently occupying each room.
    sid_to_room (dict[str, str]): SID → room code reverse index.
    sid_to_username (dict[str, str]): SID → display name index.
    room_lock (threading.Lock): Mutex serialising all mutations to
        :data:`rooms`, :data:`sid_to_room`, and :data:`sid_to_username`.
"""

import sqlalchemy as sa
from datetime import datetime, timezone
from threading import Lock

from flask import request
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room

from app.models import Message, Room
from extensions import db, socketio

# ---------------------------------------------------------------------------
# In-memory state
# ---------------------------------------------------------------------------

rooms: dict[str, set[str]] = {}
sid_to_room: dict[str, str] = {}
sid_to_username: dict[str, str] = {}
room_lock = Lock()

# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _get_room(code: str) -> Room | None:
    """Fetch a :class:`~app.models.Room` by its room code.

    Args:
        code (str): The normalised (upper-case, stripped) room code to
            look up.

    Returns:
        app.models.Room | None: The matching room, or ``None`` if no
        row with that code exists.
    """
    return db.session.scalar(
        sa.select(Room).where(Room.room_code == code)
    )


def _iso_utc_now() -> str:
    """Return the current UTC time as an ISO 8601 string.

    Used to timestamp outbound ``chat_message`` events so that all
    clients receive a canonical, timezone-aware value regardless of
    their local clock.

    Returns:
        str: Current UTC datetime in ISO 8601 format, e.g.
        ``"2026-04-18T14:32:01.123456+00:00"``.
    """
    return datetime.now(timezone.utc).isoformat()


def _sender_name() -> str:
    """Resolve the display name for the current Socket.IO connection.

    Returns:
        str: :attr:`~app.models.User.username` of the authenticated
        user, or ``'Guest'`` for unauthenticated connections.
    """
    if current_user and current_user.is_authenticated:
        return current_user.username
    return 'Guest'


def _persist_message(room: Room, content: str) -> None:
    """Persist a chat message to the database.

    Silently rolls back and swallows any exception so that a database
    error never propagates to the Socket.IO event loop and disrupts
    the live call.

    Args:
        room (app.models.Room): The room the message belongs to.
        content (str): The text body of the message (pre-validated and
            truncated by the caller).
    """
    try:
        user_id = (
            current_user.id
            if (current_user and current_user.is_authenticated)
            else None
        )
        msg = Message(msg_content=content, user_id=user_id, room_id=room.id)
        db.session.add(msg)
        db.session.commit()
    except Exception:
        db.session.rollback()


def _load_history(room: Room, limit: int = 50) -> list[dict]:
    """Load recent chat history for a room in chronological order.

    Fetches up to *limit* messages ordered by descending
    :attr:`~app.models.Message.created_at` (newest first), then
    reverses the list so callers receive messages oldest-first, matching
    the natural display order in the chat pane.

    Args:
        room (app.models.Room): The room whose history to load.
        limit (int): Maximum number of messages to return. Defaults to
            ``50``.

    Returns:
        list[dict]: A list of message dicts, each with the keys:

        - ``sender`` (*str*) — username, or ``'Guest'`` if no linked user.
        - ``message`` (*str*) — message body.
        - ``timestamp`` (*str*) — ISO 8601 creation time.
    """
    messages = db.session.scalars(
        sa.select(Message)
        .where(Message.room_id == room.id)
        .order_by(Message.created_at.desc())
        .limit(limit)
    ).all()
    return [
        {
            'sender': m.user.username if m.user else 'Guest',
            'message': m.msg_content,
            'timestamp': m.created_at.isoformat(),
        }
        for m in reversed(messages)
    ]


def _get_other_username(code: str, my_sid: str) -> str:
    """Return the display name of the other participant in a room.

    Acquires :data:`room_lock` and iterates over the SIDs registered
    for *code*, returning the username of the first SID that is not
    *my_sid*. Used when emitting ``role_and_ready`` to the callee so
    they know who they are connected to before WebRTC negotiation
    begins.

    Args:
        code (str): Normalised room code.
        my_sid (str): The SID of the participant whose counterpart is
            being looked up.

    Returns:
        str: The display name of the other participant, or
        ``'Participant'`` if none is found.
    """
    with room_lock:
        for sid in rooms.get(code, set()):
            if sid != my_sid:
                return sid_to_username.get(sid, 'Participant')
    return 'Participant'


# ---------------------------------------------------------------------------
# Join
# ---------------------------------------------------------------------------

@socketio.on('join_room')
def on_join(data: dict) -> None:
    """Handle a ``join_room`` Socket.IO event.

    Validates the room code, enforces the two-participant capacity
    limit, registers the new SID in :data:`rooms`,
    :data:`sid_to_room`, and :data:`sid_to_username` under
    :data:`room_lock`, and then emits the following events:

    - ``chat_history`` (to joining client only) — the last 50
      persisted messages, if any exist.
    - ``role_and_ready`` — signals the WebRTC role for each
      participant:

      - First participant → ``'caller'`` with ``peer_username: None``.
      - Second participant → ``'callee'`` to the joiner with the host's
        username; ``'caller'`` to the existing participant with the
        joiner's username (so the host initiates the WebRTC offer).

    - ``chat_message`` with ``sender: 'system'`` (broadcast to room,
      excluding joiner) — notifies existing participants of the new
      arrival.

    Args:
        data (dict): Payload from the client. Expected keys:

            - ``room`` (*str*) — the room code to join.
    """
    code = (data.get('room') or '').strip().upper()
    sid = request.sid

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
            sid_to_username[sid] = _sender_name()
            participants = len(rooms[code])

    join_room(code)

    history = _load_history(room)
    if history:
        emit('chat_history', {'messages': history})

    if participants == 1:
        emit('role_and_ready', {'role': 'caller', 'peer_username': None})
    elif participants == 2:
        emit(
            'role_and_ready',
            {'role': 'callee', 'peer_username': _get_other_username(code, sid)},
            to=sid,
        )
        emit(
            'role_and_ready',
            {'role': 'caller', 'peer_username': _sender_name()},
            to=code,
            include_self=False,
        )
        emit(
            'chat_message',
            {
                'sender': 'system',
                'message': f'{_sender_name()} joined the chat',
                'timestamp': _iso_utc_now(),
            },
            to=code,
            include_self=False,
        )


# ---------------------------------------------------------------------------
# Signalling
# ---------------------------------------------------------------------------

@socketio.on('signal')
def on_signal(data: dict) -> None:
    """Relay a WebRTC signalling payload to the other participant.

    Forwards ``offer``, ``answer``, and ICE candidate messages between
    the two peers without inspecting their content. Two guard clauses
    prevent signal leakage: the sending SID must be registered in the
    target room, and the room must currently exist in :data:`rooms`.

    Args:
        data (dict): Payload from the client. Expected keys:

            - ``room`` (*str*) — the room code.
            - Any additional keys required by the WebRTC signalling
              protocol (``type``, ``sdp``, ``candidate``, etc.) are
              passed through verbatim.
    """
    code = (data.get('room') or '').strip().upper()
    sid = request.sid

    if sid_to_room.get(sid) != code:
        return
    if code not in rooms:
        return

    emit('signal', data, to=code, include_self=False)


# ---------------------------------------------------------------------------
# Disconnect
# ---------------------------------------------------------------------------

@socketio.on('disconnect')
def on_disconnect() -> None:
    """Clean up state when a Socket.IO connection closes.

    Removes the disconnected SID from :data:`rooms`,
    :data:`sid_to_room`, and :data:`sid_to_username` under
    :data:`room_lock`. If the room becomes empty it is deleted from
    :data:`rooms` entirely. If at least one participant remains, two
    events are broadcast to the room:

    - ``peer_left`` — triggers the WebRTC teardown on the remaining
      client's side.
    - ``chat_message`` with ``sender: 'system'`` — notifies the
      remaining participant that the other user has left.

    The :func:`~flask_socketio.leave_room` call is wrapped in a
    ``try/except`` because Flask-SocketIO may have already cleaned up
    the room context by the time this handler runs.
    """
    sid = request.sid
    name = sid_to_username.get(sid, 'Guest')
    notify = False
    code = None

    with room_lock:
        code = sid_to_room.pop(sid, None)
        sid_to_username.pop(sid, None)
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
            {
                'sender': 'system',
                'message': f'{name} left the call.',
                'timestamp': _iso_utc_now(),
            },
            to=code,
        )


# ---------------------------------------------------------------------------
# Chat
# ---------------------------------------------------------------------------

@socketio.on('chat_message')
def on_chat_message(data: dict) -> None:
    """Handle an incoming chat message and broadcast it to the room.

    Validates that the sender's SID is registered in the target room,
    silently drops messages exceeding 1 000 characters after truncation,
    persists the message via :func:`_persist_message`, and broadcasts
    the payload to all other participants in the room.

    The message is *not* echoed back to the sender (``include_self``
    defaults to ``False`` via ``to=code, include_self=False``); the
    client is expected to render its own outgoing messages immediately
    on send.

    Args:
        data (dict): Payload from the client. Expected keys:

            - ``room`` (*str*) — the target room code.
            - ``message`` (*str*) — the message body. Truncated to
              1 000 characters if longer.
    """
    code = (data.get('room') or '').strip().upper()
    message = (data.get('message') or '').strip()
    sid = request.sid

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
        include_self=False,
    )


# ---------------------------------------------------------------------------
# Transcript
# ---------------------------------------------------------------------------

@socketio.on('transcript_letter')
def on_transcript_letter(data: dict) -> None:
    """Relay a single recognised sign-language letter to the other participant.

    Receives individual letter predictions from the client-side ML
    model and forwards them to the other participant in real time,
    allowing a running transcript to be built up letter by letter on
    the receiver's side.

    No persistence is performed; transcript data is ephemeral for the
    duration of the call.

    Args:
        data (dict): Payload from the client. Expected keys:

            - ``room`` (*str*) — the target room code.
            - ``letter`` (*str*) — the recognised letter to relay.
    """
    code = (data.get('room') or '').strip().upper()
    letter = (data.get('letter') or '').strip()
    sid = request.sid

    if not code or not letter:
        return
    if sid_to_room.get(sid) != code:
        return

    emit(
        'transcript_letter',
        {'letter': letter, 'sender': _sender_name()},
        to=code,
        include_self=False,
    )