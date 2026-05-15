"""Server-side form definitions for the call blueprint.

Defines :class:`~flask_wtf.FlaskForm` subclasses used in call-room
views. All forms inherit CSRF protection automatically from
:class:`~flask_wtf.FlaskForm`.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class JoinForm(FlaskForm):
    """Form for joining an existing call room.

    Collects the display name the user wishes to appear as during the
    session and the room code of the call they wish to join. Neither
    field is tied to a database record — validation is intentionally
    lightweight so that unauthenticated guests can join a room using
    any name they choose.

    Attributes:
        user_name (StringField): The display name shown to other
            participants during the call. Required; no uniqueness
            constraint is enforced at the form level.
        room_code (StringField): The alphanumeric code identifying the
            target room. Required; existence of the room is verified by
            the view, not the form.
        submit (SubmitField): Form submission button labelled
            ``'Start Call'``.
    """

    user_name = StringField(
        "Your Name",
        validators=[DataRequired()],
        render_kw={"class": "input", "placeholder": "Your Name"},
    )
    room_code = StringField(
        "Room Code",
        validators=[DataRequired()],
        render_kw={"class": "input", "placeholder": "Room Code"},
    )
    submit = SubmitField(
        "Start Call",
        render_kw={"class": "btn btn-primary btn-block"},
    )


class CreateRoomForm(FlaskForm):
    """Form for creating a new call room.

    A submit-only form with no input fields. Room metadata (code,
    owner, timestamps) is generated entirely by the view, so no user
    input is needed beyond the authenticated user's identity. CSRF
    protection is still applied, preventing cross-site requests from
    silently creating rooms on a logged-in user's behalf.

    Note:
        This form requires the requesting user to be authenticated.
        Unauthenticated access to the corresponding view should be
        blocked by :func:`~flask_login.login_required` before the form
        is ever instantiated.

    Attributes:
        submit (SubmitField): Form submission button labelled
            ``'Create New Session'``.
    """

    submit = SubmitField(
        "Create New Session",
        render_kw={"class": "btn btn-secondary btn-block"},
    )