from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class JoinForm(FlaskForm):
    user_name = StringField(
        "Your Name", 
        validators=[DataRequired()],
        render_kw={"class": "input", "placeholder": "Your Name"}
    )
    room_code = StringField(
        "Room Code", 
        validators=[DataRequired()],
        render_kw={"class": "input", "placeholder": "Room Code"}
    )

    submit = SubmitField(
        "Start Call",
        render_kw={"class": "btn btn-primary btn-block"}
    )


class CreateRoomForm(FlaskForm):
    submit = SubmitField(
        "Create New Session",
        render_kw={"class": "btn btn-secondary btn-block"}
    )