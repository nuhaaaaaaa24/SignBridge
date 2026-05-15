"""Custom WTForms validators shared across the application.

Provides reusable field validators for password complexity and
uniqueness checks on username and email. All validators follow the
WTForms calling convention and raise
:class:`~wtforms.validators.ValidationError` on failure.

Note:
    All functions in this module must be called within an active Flask
    application context, as the uniqueness validators query the database
    via :data:`~extensions.db`.
"""

import re

import sqlalchemy as sa
from wtforms.validators import ValidationError

from app.models import User
from extensions import db


def password_complexity(form, field) -> None:
    """Validate that a password meets the application's complexity rules.

    Intended to be passed directly as a WTForms validator reference
    (without calling it), e.g. ``validators=[password_complexity]``.
    Silently passes if the field is empty, deferring to
    :class:`~wtforms.validators.DataRequired` to handle the empty case.

    The following rules are enforced simultaneously; all failures are
    collected and reported in a single :class:`~wtforms.validators.ValidationError`
    rather than one at a time:

    - Minimum length of 12 characters.
    - At least one uppercase letter (``A–Z``).
    - At least one lowercase letter (``a–z``).
    - At least one digit (``0–9``).
    - At least one special character from ``!@#$%^&*``.

    Args:
        form (wtforms.Form): The parent form instance. Not used
            directly but required by the WTForms validator protocol.
        field (wtforms.Field): The password field being validated.
            Its :attr:`~wtforms.Field.data` attribute is inspected.

    Raises:
        wtforms.validators.ValidationError: If one or more complexity
            rules are not satisfied. The message lists every failing
            requirement in a single sentence so the user can correct
            them all at once.

    Example:
        Using as a field validator in a form::

            from app.core.validators import password_complexity

            password = PasswordField(
                'Password',
                validators=[DataRequired(), password_complexity],
            )
    """
    if not field.data:
        return

    password = field.data
    errors = []

    if len(password) < 12:
        errors.append("at least 12 characters")
    if not re.search(r'[A-Z]', password):
        errors.append("at least one uppercase letter (A-Z)")
    if not re.search(r'[a-z]', password):
        errors.append("at least one lowercase letter (a-z)")
    if not re.search(r'[0-9]', password):
        errors.append("at least one number (0-9)")
    if not re.search(r'[!@#$%^&*]', password):
        errors.append("at least one special character (!@#$%^&*)")

    if errors:
        raise ValidationError(
            "Password must include: " + ", ".join(errors) + "."
        )


def unique_username(original: str | None = None):
    """Validator factory that enforces username uniqueness.

    Returns a WTForms-compatible validator that checks whether the
    submitted username already exists in the database. Passing
    *original* allows the validator to skip the check when the user
    submits their current username unchanged, which is required by
    profile-edit forms where keeping the same username must not be
    treated as a conflict.

    Args:
        original (str | None): The user's current username, used to
            short-circuit the uniqueness check on profile-edit forms.
            Pass ``None`` (the default) on registration forms where no
            prior value exists.

    Returns:
        Callable[[Form, Field], None]: A WTForms validator that raises
        :class:`~wtforms.validators.ValidationError` if the submitted
        username is already taken by another account.

    Example:
        Registration form (no prior username)::

            username = StringField(validators=[DataRequired(), unique_username()])

        Profile-edit form (allow keeping the current username)::

            username = StringField(
                validators=[DataRequired(), unique_username(original=current_user.username)]
            )
    """
    def validator(form, field) -> None:
        if original and field.data == original:
            return
        user = db.session.scalar(
            sa.select(User).where(User.username == field.data)
        )
        if user is not None:
            raise ValidationError(
                'This username is taken! Please use a different username.'
            )
    return validator


def unique_email(original: str | None = None):
    """Validator factory that enforces email address uniqueness.

    Returns a WTForms-compatible validator that checks whether the
    submitted email address already exists in the database. Passing
    *original* allows the validator to skip the check when the user
    submits their current email unchanged, which is required by
    profile-edit forms where keeping the same address must not be
    treated as a conflict.

    Args:
        original (str | None): The user's current email address, used
            to short-circuit the uniqueness check on profile-edit forms.
            Pass ``None`` (the default) on registration forms where no
            prior value exists.

    Returns:
        Callable[[Form, Field], None]: A WTForms validator that raises
        :class:`~wtforms.validators.ValidationError` if the submitted
        email address is already registered to another account.

    Example:
        Registration form (no prior email)::

            email = StringField(validators=[DataRequired(), Email(), unique_email()])

        Profile-edit form (allow keeping the current email)::

            email = StringField(
                validators=[DataRequired(), Email(), unique_email(original=current_user.email)]
            )
    """
    def validator(form, field) -> None:
        if original and field.data == original:
            return
        user = db.session.scalar(
            sa.select(User).where(User.email == field.data)
        )
        if user is not None:
            raise ValidationError(
                'This email is taken! Please use a different email address.'
            )
    return validator