"""Server-side form definitions for the auth blueprint.

Defines :class:`~flask_wtf.FlaskForm` subclasses used in authentication
views. All forms inherit CSRF protection automatically from
:class:`~flask_wtf.FlaskForm`. Forms that are publicly reachable
(signup, login) additionally include a :class:`~flask_wtf.RecaptchaField`
to mitigate automated abuse.

Note:
    reCAPTCHA validation requires ``RECAPTCHA_PUBLIC_KEY`` and
    ``RECAPTCHA_PRIVATE_KEY`` to be set in the application config.
    See :class:`~config.Config` for details.
"""

from flask_login import current_user
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

from app.core.validators import password_complexity, unique_email, unique_username


class SignupForm(FlaskForm):
    """Registration form for new user accounts.

    Validates that the submitted email address and username are not
    already taken (via :func:`~app.core.validators.unique_email` and
    :func:`~app.core.validators.unique_username`), that the password
    meets the application's complexity requirements (via
    :func:`~app.core.validators.password_complexity`), and that both
    password fields match. A reCAPTCHA challenge prevents automated
    registrations.

    Attributes:
        email (StringField): The user's email address. Validated for
            correct format and uniqueness across existing accounts.
        username (StringField): The user's chosen display name.
            Validated for uniqueness across existing accounts.
        password (PasswordField): The desired password. Must satisfy
            :func:`~app.core.validators.password_complexity`.
        repeat_password (PasswordField): Confirmation field that must
            match :attr:`password` exactly.
        recaptcha (RecaptchaField): Google reCAPTCHA v2 challenge to
            block automated signups.
        submit (SubmitField): Form submission button labelled
            ``'Sign Up'``.
    """

    email = StringField(
        validators=[DataRequired(), Email(), unique_email()],
        render_kw={"class": "input", "placeholder": "E-mail"},
    )
    username = StringField(
        'Username',
        validators=[DataRequired(), unique_username()],
        render_kw={"class": "input", "placeholder": "Username"},
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), password_complexity],
        render_kw={"class": "input", "placeholder": "Password", "id": "password"},
    )
    repeat_password = PasswordField(
        'Repeat Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords do not match.'),
        ],
        render_kw={"class": "input", "placeholder": "Repeat password"},
    )
    recaptcha = RecaptchaField()
    submit = SubmitField(
        'Sign Up',
        render_kw={"class": "btn btn-primary btn-block"},
    )


class LoginForm(FlaskForm):
    """Login form for existing user accounts.

    Requires only a username and password; email is not used for login.
    An optional ``remember_me`` flag extends the session cookie lifetime
    beyond the browser session. A reCAPTCHA challenge limits brute-force
    login attempts before the account lockout threshold is reached.

    Attributes:
        username (StringField): The account's username.
        password (PasswordField): The account's password.
        remember_me (BooleanField): When checked, the session persists
            across browser restarts for the duration configured in
            ``PERMANENT_SESSION_LIFETIME``.
        recaptcha (RecaptchaField): Google reCAPTCHA v2 challenge to
            slow automated credential-stuffing attacks.
        submit (SubmitField): Form submission button labelled
            ``'Log In'``.
    """

    username = StringField(
        'Username',
        validators=[DataRequired()],
        render_kw={"class": "input", "placeholder": "Username"},
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()],
        render_kw={"class": "input", "placeholder": "Password"},
    )
    remember_me = BooleanField('Remember Me')
    recaptcha = RecaptchaField()
    submit = SubmitField(
        'Log In',
        render_kw={"class": "btn btn-primary btn-block"},
    )


class ResetPasswordRequestForm(FlaskForm):
    """Form for requesting a password reset email.

    Accepts any valid email address without checking whether it belongs
    to a registered account. The view is responsible for the conditional
    dispatch so that the response gives no hint about which addresses are
    registered (preventing account enumeration).

    Attributes:
        email (StringField): The email address to send the reset link to.
            Validated for correct format only; existence is not checked
            at the form level.
        submit (SubmitField): Form submission button labelled
            ``'Request Password Reset'``.
    """

    email = StringField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw={"class": "input", "placeholder": "E-mail"},
    )
    submit = SubmitField(
        'Request Password Reset',
        render_kw={"class": "btn btn-primary btn-block"},
    )


class ResetPasswordForm(FlaskForm):
    """Form for setting a new password via a reset link.

    Presented after a valid signed reset token has been verified by the
    auth view. Enforces that both password fields match.

    Attributes:
        password (PasswordField): The new password to set.
        repeat_password (PasswordField): Confirmation field that must
            match :attr:`password` exactly.
        submit (SubmitField): Form submission button labelled
            ``'Request Password Reset'``.
    """

    password = PasswordField(
        'Password',
        validators=[DataRequired(), password_complexity],
        render_kw={"class": "input", "placeholder": "Password"},
    )
    repeat_password = PasswordField(
        'Repeat Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords do not match.'),
        ],
        render_kw={"class": "input", "placeholder": "Repeat Password"},
    )
    submit = SubmitField(
        'Request Password Reset',
        render_kw={"class": "btn btn-primary btn-block"},
    )