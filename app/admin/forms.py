"""Server-side form definitions for the admin blueprint.

Defines :class:`~flask_wtf.FlaskForm` subclasses used in admin views.
All forms inherit CSRF protection automatically from
:class:`~flask_wtf.FlaskForm` — no additional configuration required.
"""

from flask_wtf import FlaskForm
from wtforms import SubmitField


class ToggleAdminForm(FlaskForm):
    """Form for toggling a user's admin privileges.

    Rendered once per user row in the admin user table. Submitting
    promotes a standard user to admin, or demotes an admin back to a
    standard user, depending on the current value of
    :attr:`~app.models.User.is_admin`.

    Attributes:
        submit (SubmitField): Confirmation button labelled
            ``'Toggle Admin'``.
    """

    submit = SubmitField('Toggle Admin')


class DeleteUserForm(FlaskForm):
    """Form for permanently removing a user from the system.

    Provides a CSRF-protected submission mechanism for admin-initiated
    account deletion. The associated view is responsible for any
    additional confirmation or soft-delete logic before committing the
    removal.

    Attributes:
        submit (SubmitField): Confirmation button labelled ``'Delete'``.
    """

    submit = SubmitField('Delete')


class UnblockUserForm(FlaskForm):
    """Form for lifting an existing block on a user account.

    Used in the admin user table to restore access for a user whose
    account was previously suspended. Submitting clears the blocked
    status on the associated :class:`~app.models.User` record.

    Attributes:
        submit (SubmitField): Confirmation button labelled
            ``'Unblock User'``.
    """

    submit = SubmitField('Unblock User')