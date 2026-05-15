"""Server-side form definitions for the main blueprint.

Defines the :class:`ContactForm` used on the public contact page.
The form inherits CSRF protection automatically from
:class:`~flask_wtf.FlaskForm` and is accessible to both authenticated
and unauthenticated visitors.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    """Form for sending a message to the site administrators.

    Accessible to any visitor regardless of authentication status.
    Submitted messages are dispatched via
    :func:`~app.core.email.send_email` in the corresponding view;
    no data is persisted to the database.

    Attributes:
        name (StringField): The sender's display name. Required;
            maximum 100 characters.
        email (StringField): The sender's email address. Required;
            must be a valid email format so that admins can reply.
        subject (StringField): A brief description of the enquiry.
            Required; maximum 150 characters.
        message (TextAreaField): The body of the message. Required;
            minimum 10 characters to prevent empty or trivially short
            submissions.
        submit (SubmitField): Form submission button labelled
            ``'Send Message'``.
    """

    name = StringField(
        'Your Name',
        validators=[DataRequired(), Length(max=100)],
        render_kw={"class": "input", "placeholder": "Your Name"},
    )
    email = StringField(
        'Your Email',
        validators=[DataRequired(), Email()],
        render_kw={"class": "input", "placeholder": "Your E-mail"},
    )
    subject = StringField(
        'Subject',
        validators=[DataRequired(), Length(max=150)],
        render_kw={"class": "input", "placeholder": "Subject"},
    )
    message = TextAreaField(
        'Message',
        validators=[DataRequired(), Length(min=10)],
        render_kw={"class": "input", "placeholder": "Your Message"},
    )
    submit = SubmitField(
        'Send Message',
        render_kw={"class": "btn btn-primary btn-block"},
    )