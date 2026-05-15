"""Route handlers for the call blueprint.

Manages the full call-room lifecycle: joining an existing room,
creating a new one, and accessing the live call page. Room occupancy
is tracked in real time via the :data:`~app.call.sockets.rooms`
dictionary maintained by the Socket.IO event handlers, so all three
views consult it to enforce capacity and host-presence rules.

All state-changing endpoints (``POST``) are rate-limited via
:data:`~extensions.limiter` to prevent automated room creation and
join-flooding.
"""

from flask import (
    abort, current_app, flash, redirect,
    render_template, request, url_for,
)
from flask_login import current_user, login_required

import sqlalchemy as sa

from app.call import call_bp
from app.call.forms import CreateRoomForm, JoinForm
from app.call.services import generate_unique_room_code
from app.call.sockets import rooms
from app.models import Room
from extensions import db, limiter


@call_bp.route('/join', methods=['GET', 'POST'])
@limiter.limit('10 per minute', methods=['POST'])
def join():
    """Display the join form and validate a room-join attempt.

    ``GET`` renders the join page with both a :class:`~app.call.forms.JoinForm`
    and an inline :class:`~app.call.forms.CreateRoomForm`. On a valid
    ``POST``, the submitted room code is normalised (stripped and
    upper-cased) and the following checks are applied in order:

    1. The room code must correspond to an existing
       :class:`~app.models.Room` row.
    2. If the host is not currently present in the Socket.IO
       :data:`~app.call.sockets.rooms` dictionary, only the room owner
       may proceed; guests are blocked until the host joins.
    3. The room must have fewer than two active participants.

    Passing all checks redirects the user to :func:`call` for the
    actual session.

    Rate limited to **10 POST requests per minute** per remote IP.

    Returns:
        flask.Response: A rendered ``call/join.html`` template on
        ``GET`` or failed validation, otherwise a redirect to
        :func:`call` on success or back to :func:`join` on any
        failed check.
    """
    form = JoinForm()
    if form.validate_on_submit():
        code = form.room_code.data.strip().upper()
        current_app.logger.info(
            f"Room join attempt: code={code} ip={request.remote_addr}"
        )

        room = db.session.scalar(
            sa.select(Room).where(Room.room_code == code)
        )

        if not room:
            current_app.logger.warning(
                f"Failed room join (not found): code={code} ip={request.remote_addr}"
            )
            flash('Room not found. Check the code and try again.')
            return redirect(url_for('call.join'))

        is_owner = current_user.is_authenticated and current_user.id == room.owner_id

        if code not in rooms or len(rooms.get(code, set())) == 0:
            if not is_owner:
                current_app.logger.warning(
                    f"Failed room join (owner unavailable): code={code} ip={request.remote_addr}"
                )
                flash("This room is currently unavailable because the host is not in the call.")
                return redirect(url_for('call.join'))

        if len(rooms.get(code, set())) >= 2:
            current_app.logger.warning(
                f"Failed room join (room full): code={code} ip={request.remote_addr}"
            )
            flash("This room is already full.")
            return redirect(url_for('call.join'))

        return redirect(url_for('call.call', room=code))

    create_form = CreateRoomForm()
    return render_template(
        'call/join.html',
        title='Join A Room',
        form=form,
        create_form=create_form,
    )


@call_bp.route('/create-room', methods=['POST'])
@limiter.limit('5 per minute', methods=['POST'])
@login_required
def create_room():
    """Create a new call room and redirect the owner to it.

    Generates a collision-free room code via
    :func:`~app.call.services.generate_unique_room_code`, persists a
    new :class:`~app.models.Room` row with the current user set as
    owner, then redirects straight to :func:`call` so the owner enters
    the room immediately without an intermediate confirmation step.

    CSRF validation is provided by the submitted
    :class:`~app.call.forms.CreateRoomForm` token rather than by any
    user-supplied fields. If validation fails (e.g. a stale token), the
    user is silently redirected back to :func:`join` without an error
    message, since the most likely cause is a double-submit or an
    expired session.

    Rate limited to **5 POST requests per minute** per remote IP —
    stricter than :func:`join` to limit room proliferation.

    Returns:
        flask.Response: A redirect to :func:`call` on success, or to
        :func:`join` if CSRF validation fails.
    """
    form = CreateRoomForm()

    if form.validate_on_submit():
        code = generate_unique_room_code()
        room = Room(room_code=code, owner_id=current_user.id)
        db.session.add(room)
        db.session.commit()
        current_app.logger.info(
            f"Room created: code={code} owner_id={current_user.id} "
            f"ip={request.remote_addr}"
        )
        return redirect(url_for('call.call', room=code))

    return redirect(url_for('call.join'))


@call_bp.route('/call')
@limiter.limit('10 per minute')
def call():
    """Validate room access and render the live call page.

    Reads the target room code from the ``room`` query parameter,
    normalises it, and applies the same host-presence and capacity
    checks as :func:`join`. This view is reached by redirects from both
    :func:`join` and :func:`create_room`, but is also directly
    accessible via URL, so the checks must be enforced here
    independently.

    The owner is exempt from the host-presence check so they can
    rejoin a room that has temporarily emptied (e.g. after a page
    refresh), without being blocked by their own absence from the
    Socket.IO :data:`~app.call.sockets.rooms` dictionary.

    Rate limited to **10 requests per minute** per remote IP (``GET``
    and ``POST``).

    Args:
        room (str): Room code passed as a query parameter
            (``?room=<code>``). Normalised to uppercase by this view;
            callers need not pre-normalise.

    Returns:
        flask.Response: A rendered ``call/call.html`` template on
        success, otherwise a redirect to :func:`join` with an
        explanatory flash message.
    """
    code = request.args.get('room', '').strip().upper()
    current_app.logger.info(
        f"Call page access attempt: code={code} ip={request.remote_addr}"
    )

    room = db.session.scalar(
        sa.select(Room).where(Room.room_code == code)
    )

    if not room:
        current_app.logger.warning(
            f"Failed call access (not found): code={code} ip={request.remote_addr}"
        )
        flash('Room not found. Check the code and try again.')
        return redirect(url_for('call.join'))

    is_owner = current_user.is_authenticated and current_user.id == room.owner_id

    if code not in rooms or len(rooms.get(code, set())) == 0:
        if not is_owner:
            current_app.logger.warning(
                f"Failed call access (owner unavailable): code={code} ip={request.remote_addr}"
            )
            flash("This room is currently unavailable because the host is not in the call.")
            return redirect(url_for('call.join'))

    if len(rooms.get(code, set())) >= 2:
        current_app.logger.warning(
            f"Failed call access (room full): code={code} ip={request.remote_addr}"
        )
        flash("This room is already full.")
        return redirect(url_for('call.join'))

    current_app.logger.info(
        f"Room accessed: code={code} user_id={getattr(current_user, 'id', None)}"
    )
    return render_template('call/call.html', room_code=code, title='Meeting Room')