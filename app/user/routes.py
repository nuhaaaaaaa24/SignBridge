"""Route handlers for the user blueprint.

Manages authenticated user account operations: viewing the dashboard
and profile, editing account details, and initiating self-service
account deletion. All routes require an active login session enforced
by :func:`~flask_login.login_required`.
"""

from datetime import datetime, timedelta, timezone

from flask import current_app, flash, redirect, render_template, request, url_for, session, jsonify
from flask_login import current_user, login_required, logout_user
from app.models import User
from app.user import user_bp
from app.user.forms import DeleteUserForm, EditProfileForm, EmptyForm
from extensions import db, limiter


@user_bp.route('/dashboard')
@login_required
def dashboard():
    """Render the authenticated user's dashboard.

    Passes an :class:`~app.user.forms.EmptyForm` to the template so
    that any one-click actions on the dashboard (e.g. toggles or
    quick-submit buttons) have a CSRF token without requiring a
    dedicated form definition.

    Returns:
        flask.Response: The rendered ``user/dashboard.html`` template.
    """
    form = EmptyForm()
    return render_template('user/dashboard.html', title='Dashboard', form=form)


@user_bp.route('/profile')
@login_required
def profile():
    """Render the current user's account overview page.

    Supplies both an :class:`~app.user.forms.EmptyForm` (for
    CSRF-protected quick actions) and a
    :class:`~app.user.forms.DeleteUserForm` (for the account deletion
    confirmation widget) so both can be rendered on the same page
    without a redirect.

    Returns:
        flask.Response: The rendered ``user/user.html`` template,
        with ``user``, ``form``, and ``delete_form`` in context.
    """
    form = EmptyForm()
    delete_form = DeleteUserForm()
    return render_template(
        'user/user.html',
        title='Your Account',
        user=current_user,
        form=form,
        delete_form=delete_form,
    )


@user_bp.route('/edit_profile', methods=['GET', 'POST'])
@limiter.limit('5 per minute', methods=['POST'])
@login_required
def edit_profile():
    """Display the profile-edit form and apply submitted changes.

    ``GET`` renders the form pre-populated with the current user's
    existing values via ``obj=current_user``. On a valid ``POST``,
    only fields that contain data are applied — allowing a user to
    change just their username without touching their email or
    password. Each change is recorded in a log entry without
    exposing the new values to anyone viewing the logs.

    Field update rules:

    - **username** — replaced with the submitted value if non-empty.
    - **email** — replaced with the submitted value if non-empty.
    - **password** — updated only when :attr:`~app.user.forms.EditProfileForm.new_password`
      is present; cross-field validation in
      :meth:`~app.user.forms.EditProfileForm.validate` ensures the
      current password is verified first.

    Rate limited to **5 POST requests per minute** per remote IP.

    Returns:
        flask.Response: The rendered ``user/edit-profile.html``
        template on ``GET`` or failed validation, otherwise a
        redirect to :func:`profile` on success.
    """
    form = EditProfileForm(current_user.username, current_user.email, obj=current_user)

    if form.validate_on_submit():
        changes = []

        if form.username.data:
            changes.append(
                f"username {current_user.username} has changed to new username: {form.username.data}"
            )
            current_user.username = form.username.data

        if form.email.data:
            changes.append(
                f"email {current_user.email} has changed to new email: {form.email.data}"
            )
            current_user.email = form.email.data

        if form.new_password.data:
            changes.append("password has been updated")
            current_user.set_password(form.new_password.data)

        db.session.commit()
        current_app.logger.info(
            f"Profile updated: user_id={current_user.id} "
            f"changes={changes} ip={request.remote_addr}"
        )
        flash("Profile updated successfully")
        return redirect(url_for('user.profile'))

    return render_template(
        'user/edit-profile.html',
        title='Edit Profile',
        form=form,
        user=current_user,
    )


@user_bp.route('/user/<int:id>/delete', methods=['POST'])
@limiter.limit('5 per minute', methods=['POST'])
@login_required
def delete_user(id):
    """Initiate a soft-delete of the current user's account.

    Implements a two-phase deletion model: rather than removing the
    account row immediately, a ``scheduled_deletion`` timestamp is set
    to 30 days in the future and the user is logged out. The
    background task :func:`~app.tasks.process_pending_deletions`
    finalises the deletion when that deadline elapses. Logging in
    before the deadline cancels the scheduled deletion automatically
    (handled in :func:`~app.auth.routes.login`).

    The following checks are applied before the deletion is scheduled:

    1. CSRF token must be valid.
    2. The target ``id`` must correspond to the currently authenticated
       user — preventing one user from deleting another's account.
    3. A deletion must not already be pending for this account.
    4. The submitted password must match the user's stored hash.

    On success, the user's API token is revoked via
    :meth:`~app.models.User.revoke_token`, the session is terminated,
    and the user is redirected to ``main.index``. Any database error
    triggers a rollback and a generic error flash; the exception is
    recorded with :meth:`~flask.app.Flask.logger.exception` so the
    full traceback is preserved in the log.

    Rate limited to **5 POST requests per minute** per remote IP.

    Args:
        id (int): Primary key of the :class:`~app.models.User` to
            delete. Supplied by Flask from the ``<int:id>`` URL segment.
            Must match :attr:`~flask_login.current_user`'s ``id`` or
            the request is rejected.

    Returns:
        flask.Response: A redirect to ``main.index`` on success, or to
        ``user.profile`` on any failed check or error.

    Raises:
        werkzeug.exceptions.NotFound: (HTTP 404) If no
            :class:`~app.models.User` with the given *id* exists.
    """
    form = DeleteUserForm()

    if not form.validate_on_submit():
        flash('Invalid request.')
        return redirect(url_for('user.profile'))

    user = User.query.get_or_404(id)

    if user != current_user:
        flash("You cannot delete other users' accounts.")
        return redirect(url_for('user.profile'))

    try:
        if user.scheduled_deletion is not None:
            remaining = (user.scheduled_deletion - datetime.now(timezone.utc)).days
            flash(
                f"Your account is already scheduled for deletion. "
                f"You have {remaining} days remaining."
            )
            return redirect(url_for('user.profile'))

        if not user.check_password(form.password.data):
            flash('Incorrect password.')
            return redirect(url_for('user.profile'))

        user.is_deleted = False
        user.scheduled_deletion = datetime.now(timezone.utc) + timedelta(days=30)
        user.revoke_token()
        db.session.commit()

        current_app.logger.info(
            f"User {user.username} has scheduled deletion of their account."
        )
        flash(
            'Your account has been scheduled for deletion in 30 days. '
            'Log in to cancel at any time before that.'
        )
        logout_user()
        return redirect(url_for("main.index"))

    except Exception:
        db.session.rollback()
        current_app.logger.exception(
            f"Account deletion failed for user_id={current_user.id}, "
            f"username={current_user.username}"
        )
        flash('An error has occurred. Please try again later.')
        return redirect(url_for('user.profile'))
    
@user_bp.route("/delete-session-data", methods=["POST"])
@limiter.limit("5 per minute", methods=["POST"])
@login_required
def delete_session_data():
    """Clear all server-side session data for the current user.

    Wipes every key stored in the Flask session, which removes
    ephemeral state (e.g. flash messages, wizard step, OAuth nonces)
    without logging the user out or touching the database. The user's
    :class:`~flask_login.current_user` identity is preserved because
    Flask-Login re-establishes it on the next request via the
    remember-me cookie or the session cookie that is re-issued
    after the clear.

    Rate limited to **5 POST requests per minute** per remote IP.

    Returns:
        flask.Response: A redirect to :func:`profile` with a success
        flash message confirming the session data was cleared.
    """
    session.clear()
    current_app.logger.info(
        f"Session data cleared: user_id={current_user.id} ip={request.remote_addr}"
    )
    flash('Your session data has been cleared successfully.')
    return redirect(url_for('user.dashboard'))