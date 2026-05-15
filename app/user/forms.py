"""Server-side form definitions for the user blueprint.

Defines :class:`~flask_wtf.FlaskForm` subclasses used in user account
management views. Authentication-related forms (login, registration,
password reset) live in :mod:`app.auth.forms` instead.

All forms inherit CSRF protection automatically from
:class:`~flask_wtf.FlaskForm`.
"""

from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Optional, ValidationError

from app.core.validators import password_complexity, unique_email, unique_username
from app.models import User


class EditProfileForm(FlaskForm):
    """Form for editing a user's profile details in place.

    All fields are optional individually so that a user can update only
    their username, only their email, or only their password without
    touching the others. Cross-field password validation is enforced by
    the overridden :meth:`validate` method rather than by individual
    field validators, as the rules span three fields simultaneously.

    Uniqueness validators for :attr:`username` and :attr:`email` are
    injected at construction time via :meth:`__init__` so that the
    current user's existing values are exempt from the uniqueness check
    — allowing a user to submit the form with their current username or
    email unchanged without triggering a conflict error.

    Attributes:
        username (StringField): Optional new username. Validated for
            uniqueness against all other accounts, but not against the
            current user's existing username.
        email (StringField): Optional new email address. Validated for
            correct format and uniqueness against all other accounts,
            but not against the current user's existing email.
        current_password (PasswordField): The user's existing password,
            required only when a new password is being set.
        new_password (PasswordField): The desired new password. Must
            satisfy :func:`~app.core.validators.password_complexity`
            when provided.
        repeat_new_password (PasswordField): Confirmation of
            :attr:`new_password`; must match exactly.
        submit (SubmitField): Form submission button labelled
            ``'Submit'``.
    """

    username = StringField(
        'Change your username:',
        validators=[Optional()],
        render_kw={"class": "input", "placeholder": "Username"},
    )
    email = StringField(
        'Change your e-mail:',
        validators=[Optional(), Email()],
        render_kw={"class": "input", "placeholder": "E-mail"},
    )
    current_password = PasswordField(
        'Enter your current password:',
        validators=[Optional()],
        render_kw={"class": "input", "placeholder": "Password"},
    )
    new_password = PasswordField(
        'Enter your new password:',
        validators=[Optional(), password_complexity],
        render_kw={"class": "input", "placeholder": "New Password"},
    )
    repeat_new_password = PasswordField(
        'Repeat your new password:',
        validators=[Optional(), EqualTo('new_password', message='Passwords must match.')],
        render_kw={"class": "input", "placeholder": "Repeat New Password"},
    )
    submit = SubmitField('Submit')

    def __init__(self, original_username: str, original_email: str, *args, **kwargs):
        """Initialise the form and inject current-value-aware uniqueness validators.

        Passes *original_username* and *original_email* to
        :func:`~app.core.validators.unique_username` and
        :func:`~app.core.validators.unique_email` respectively so that
        those validators skip the database check when the submitted
        value is identical to the user's current value.

        Args:
            original_username (str): The current user's username at the
                time the form is rendered. Typically
                ``current_user.username``.
            original_email (str): The current user's email address at
                the time the form is rendered. Typically
                ``current_user.email``.
            *args: Positional arguments forwarded to
                :class:`~flask_wtf.FlaskForm`.
            **kwargs: Keyword arguments forwarded to
                :class:`~flask_wtf.FlaskForm`.
        """
        super().__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email
        self.username.validators = [
            *self.username.validators,
            unique_username(original_username),
        ]
        self.email.validators = [
            *self.email.validators,
            unique_email(original_email),
        ]

    def validate(self, extra_validators=None) -> bool:
        """Run cross-field password validation before standard WTForms validation.

        Enforces the following rules when either :attr:`new_password` or
        :attr:`repeat_new_password` contains data:

        1. :attr:`current_password` must be provided.
        2. :attr:`current_password` must match the user's stored password
           hash, verified via :meth:`~app.models.User.check_password`.
        3. Both :attr:`new_password` and :attr:`repeat_new_password` must
           be filled (guards against one field being cleared after the
           other is populated).

        If all three checks pass, control is delegated to
        :meth:`~flask_wtf.FlaskForm.validate` for standard per-field
        validation. Errors are appended directly to the relevant field's
        :attr:`~wtforms.Field.errors` tuple so they surface in the
        template alongside other field errors.

        Args:
            extra_validators (dict | None): Optional mapping of field
                names to additional validators, forwarded verbatim to
                :meth:`~flask_wtf.FlaskForm.validate`.

        Returns:
            bool: ``True`` if all cross-field checks and standard
            per-field validation pass, ``False`` otherwise.
        """
        if self.new_password.data or self.repeat_new_password.data:
            if not self.current_password.data:
                self.current_password.errors += (
                    "Enter your current password to set a new password.",
                )
                return False
            if not current_user.check_password(self.current_password.data):
                self.current_password.errors += ("Current password is incorrect.",)
                return False
            if not self.new_password.data or not self.repeat_new_password.data:
                self.new_password.errors += (
                    "Both new password fields must be filled out.",
                )
                return False
        return super().validate(extra_validators)


class EmptyForm(FlaskForm):
    """Minimal CSRF-protected form with a single submit button.

    Used wherever an action requires only CSRF protection with no
    additional user input — for example, a one-click toggle or
    confirmation that should not be triggerable via a plain ``<a>``
    link.

    Attributes:
        submit (SubmitField): Form submission button labelled
            ``'Submit'``.
    """

    submit = SubmitField('Submit')


class DeleteUserForm(FlaskForm):
    """Form for self-service account deletion with password confirmation.

    Requires the user to re-enter their current password before the
    deletion is processed, providing a friction step that prevents
    accidental or CSRF-induced deletion.

    Attributes:
        password (PasswordField): The user's current password, used to
            confirm intent before the account is permanently removed.
        submit (SubmitField): Form submission button labelled
            ``'Delete'``.
    """

    password = PasswordField(
        "Confirm Password",
        validators=[DataRequired()],
        render_kw={"class": "input", "placeholder": "Password"},
    )
    submit = SubmitField('Delete')