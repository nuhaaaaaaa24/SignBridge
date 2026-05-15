"""Route handlers for the admin blueprint.

All routes in this module are protected by both :func:`~flask_login.login_required`
and :func:`~app.admin.utils.admin_required`, so unauthenticated users are
redirected to the login page and non-admin users receive a 403 before any
view logic runs.
"""

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app import db
from app.admin import admin_bp
from app.admin.forms import DeleteUserForm, ToggleAdminForm, UnblockUserForm
from app.admin.utils import admin_required
from app.models import User


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Render the admin dashboard with all registered users.

    Fetches every :class:`~app.models.User` record ordered alphabetically
    by username and instantiates one form per user-action type so that
    each row in the dashboard table has its own CSRF-protected submission
    token.

    Returns:
        flask.Response: A rendered ``admin/admin-dashboard.html`` template
        populated with:

        - **users** (*list[User]*) — all users, ordered by username.
        - **toggle_form** (:class:`~app.admin.forms.ToggleAdminForm`)
        - **unblock_form** (:class:`~app.admin.forms.UnblockUserForm`)
        - **delete_form** (:class:`~app.admin.forms.DeleteUserForm`)
    """
    users = User.query.order_by(User.username).all()
    toggle_form = ToggleAdminForm()
    unblock_form = UnblockUserForm()
    delete_form = DeleteUserForm()
    return render_template(
        'admin/admin-dashboard.html',
        title='Admin Dashboard',
        users=users,
        toggle_form=toggle_form,
        unblock_form=unblock_form,
        delete_form=delete_form,
    )


@admin_bp.route('/user/<int:id>/toggle-admin', methods=['POST'])
@login_required
@admin_required
def toggle_admin(id):
    """Toggle the admin privileges of a user account.

    Flips :attr:`~app.models.User.is_admin` between ``True`` and
    ``False``. The following conditions abort the operation and redirect
    back to the dashboard with an explanatory flash message:

    - The CSRF token fails validation.
    - The target user is the currently authenticated admin (self-demotion
      is not permitted).
    - The target user is currently blocked (admin status of blocked
      accounts must not be changed until the block is lifted).

    Args:
        id (int): Primary key of the :class:`~app.models.User` to update.
            Supplied by Flask from the ``<int:id>`` URL segment.

    Returns:
        flask.Response: A redirect to ``admin.dashboard`` in all cases.
        A :func:`~flask.flash` message communicates the outcome to the
        user.

    Raises:
        werkzeug.exceptions.NotFound: (HTTP 404) If no
            :class:`~app.models.User` with the given *id* exists.
    """
    form = ToggleAdminForm()
    if not form.validate_on_submit():
        flash('Invalid request.')
        return redirect(url_for('admin.dashboard'))

    user = User.query.get_or_404(id)

    if user == current_user:
        flash('You cannot change your own admin status.')
        return redirect(url_for('admin.dashboard'))

    if user.is_blocked:
        flash(
            f'Cannot change admin status of a blocked user. '
            f'Unblock {user.username} first.'
        )
        return redirect(url_for('admin.dashboard'))

    user.is_admin = not user.is_admin
    db.session.commit()
    flash(f'Admin status updated for {user.username}.')
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/user/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    """Permanently delete a user account and all associated rooms.

    Iterates over :attr:`~app.models.User.rooms` and deletes each room
    before removing the user row itself, as a precaution against
    foreign-key constraint violations on databases that do not cascade
    deletes automatically. The entire operation runs inside a single
    transaction; any exception triggers a rollback so the database is
    never left in a partially deleted state.

    The following conditions abort the operation before touching the
    database:

    - The CSRF token fails validation.
    - The target user is the currently authenticated admin (self-deletion
      is not permitted).

    Args:
        id (int): Primary key of the :class:`~app.models.User` to delete.
            Supplied by Flask from the ``<int:id>`` URL segment.

    Returns:
        flask.Response: A redirect to ``admin.dashboard`` in all cases.
        A :func:`~flask.flash` message communicates the outcome or any
        error to the user.

    Raises:
        werkzeug.exceptions.NotFound: (HTTP 404) If no
            :class:`~app.models.User` with the given *id* exists.
    """
    form = DeleteUserForm()
    if not form.validate_on_submit():
        flash('Invalid request.')
        return redirect(url_for('admin.dashboard'))

    user = User.query.get_or_404(id)

    if user == current_user:
        flash('You cannot delete yourself.')
        return redirect(url_for('admin.dashboard'))

    try:
        for room in user.rooms:
            db.session.delete(room)
        db.session.delete(user)
        db.session.commit()
        flash(f'User {user.username} deleted.')
    except Exception:
        db.session.rollback()
        flash('Error deleting user.')

    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/user/<int:id>/unblock', methods=['POST'])
@login_required
@admin_required
def unblock_user(id):
    """Lift a block on a user account and reset their login failure counter.

    Clears :attr:`~app.models.User.is_blocked`, nullifies
    :attr:`~app.models.User.blocked_until`, and resets
    :attr:`~app.models.User.failed_login_attempts` to ``0`` so that the
    user can attempt to log in again immediately with a clean slate.

    The following conditions abort the operation:

    - The CSRF token fails validation.
    - The target user is not currently blocked.

    Args:
        id (int): Primary key of the :class:`~app.models.User` to unblock.
            Supplied by Flask from the ``<int:id>`` URL segment.

    Returns:
        flask.Response: A redirect to ``admin.dashboard`` in all cases.
        A :func:`~flask.flash` message communicates the outcome to the
        user.

    Raises:
        werkzeug.exceptions.NotFound: (HTTP 404) If no
            :class:`~app.models.User` with the given *id* exists.
    """
    form = UnblockUserForm()
    if not form.validate_on_submit():
        flash('Invalid request.')
        return redirect(url_for('admin.dashboard'))

    user = User.query.get_or_404(id)

    if not user.is_blocked:
        flash(f'{user.username} is not blocked.')
        return redirect(url_for('admin.dashboard'))

    user.is_blocked = False
    user.blocked_until = None
    user.failed_login_attempts = 0
    db.session.commit()
    flash(f'User {user.username} has been unblocked.')
    return redirect(url_for('admin.dashboard'))