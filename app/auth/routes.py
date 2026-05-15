"""Route handlers for the auth blueprint.

Covers the full authentication lifecycle: login, logout, registration,
and the two-step password reset flow. All state-changing endpoints
(``POST``) are rate-limited via :data:`~extensions.limiter` to mitigate
brute-force and enumeration attacks.

Attributes:
    MAX_LOGIN_ATTEMPTS (int): Number of consecutive failed password
        checks before a non-admin account is automatically blocked.
        Currently ``10``.
    BLOCK_DURATION_MINS (int): Duration in minutes of an automatic
        account block triggered by :data:`MAX_LOGIN_ATTEMPTS` failures.
        Currently ``30``.
"""

from datetime import datetime, timedelta, timezone
from urllib.parse import urlsplit

import sqlalchemy as sa
from flask import (
    current_app, flash, redirect, render_template,
    request, session, url_for,
)
from flask_limiter.util import get_remote_address
from flask_login import current_user, login_user, logout_user

from app.auth import auth_bp
from app.auth.email import send_password_reset_email
from app.auth.forms import (
    LoginForm, ResetPasswordForm,
    ResetPasswordRequestForm, SignupForm,
)
from app.models import User
from extensions import db, limiter

MAX_LOGIN_ATTEMPTS = 10
BLOCK_DURATION_MINS = 30


def login_key():
    """Derive a rate-limit bucket key from the submitted username.

    Keying the login rate limit on username rather than IP prevents a
    single attacker from bypassing per-IP limits by rotating addresses
    (e.g. via a VPN), while still falling back to the remote IP when no
    username is present in the form data.

    Username values are lower-cased and stripped of surrounding
    whitespace before use so that case variations do not produce
    separate, cheaper buckets.

    Returns:
        str: ``"login:<normalised_username>"`` when a username field is
        present in the current form submission, otherwise the raw remote
        IP address as returned by
        :func:`~flask_limiter.util.get_remote_address`.
    """
    username = request.form.get("username")
    if username:
        return f"login:{username.lower().strip()}"
    return get_remote_address()


@auth_bp.before_app_request
def check_if_blocked():
    """Intercept every request and force-logout blocked accounts.

    Registered as a ``before_app_request`` hook so it runs across all
    blueprints, not just ``auth``. Marking the session as permanent here
    also ensures that ``PERMANENT_SESSION_LIFETIME`` (set in
    :class:`~config.Config`) takes effect for every session, including
    those created before this hook was added.

    If the current user is authenticated and their
    :attr:`~app.models.User.is_blocked` flag is ``True``, they are
    logged out immediately and redirected to the login page with an
    explanatory flash message.

    Returns:
        flask.Response | None: A redirect to ``auth.login`` if the
        current user is blocked, otherwise ``None`` (allowing the
        request to continue normally).
    """
    session.permanent = True
    if current_user.is_authenticated and current_user.is_blocked:
        logout_user()
        flash("Your account has been blocked. Contact an admin (admin.signbridge+support@gmail.com).")
        return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute", key_func=login_key, methods=['POST'])
def login():
    """Display the login form and authenticate the submitted credentials.

    ``GET`` renders the form. ``POST`` runs the following checks in
    order, redirecting back to the login page with a flash message if
    any check fails:

    1. User exists for the submitted username.
    2. Account has not been soft-deleted (:attr:`~app.models.User.is_deleted`).
    3. Scheduled deletion deadline has not already elapsed (if set, the
       account is finalised on the spot).
    4. Account is not currently blocked; if the block timer has expired
       it is lifted automatically.
    5. Password is correct; failure increments
       :attr:`~app.models.User.failed_login_attempts` and triggers a
       block once :data:`MAX_LOGIN_ATTEMPTS` is reached (admin accounts
       are exempt from auto-blocking).

    On success, any pending scheduled deletion is cancelled, the failure
    counter is reset, a new API token is issued via
    :meth:`~app.models.User.get_token`, and the user is redirected to
    the ``next`` query parameter (relative paths only) or
    ``user.dashboard``.

    Rate limited to **5 POST requests per minute** per
    :func:`login_key`.

    Returns:
        flask.Response: A rendered ``auth/login.html`` template on
        ``GET`` or failed validation, otherwise a redirect.
    """
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )

        if not user:
            current_app.logger.warning(
                f"Failed login attempt for username {form.username.data} "
                f"from IP {request.remote_addr}: User does not exist"
            )
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

        if user.is_deleted:
            flash('This account has been deleted.')
            current_app.logger.warning(
                f"Failed login attempt for username {form.username.data} "
                f"from IP {request.remote_addr}: User has been deleted."
            )
            return redirect(url_for('auth.login'))

        if user.scheduled_deletion is not None:
            if datetime.now(timezone.utc) >= user.scheduled_deletion:
                user.is_deleted = True
                user.scheduled_deletion = None
                db.session.commit()
                flash('This account has been deleted.')
                current_app.logger.warning(
                    f"Deleted account login attempt: {user.username} "
                    f"from IP {request.remote_addr}"
                )
                return redirect(url_for('auth.login'))

        if user.is_blocked:
            if user.blocked_until and datetime.now(timezone.utc) >= user.blocked_until:
                user.is_blocked = False
                user.blocked_until = None
                user.failed_login_attempts = 0
                db.session.commit()
            else:
                flash('Your account has been blocked. Contact an admin (admin.signbridge+support@gmail.com).')
                return redirect(url_for('auth.login'))

        if not user.check_password(form.password.data):
            if not user.is_admin:
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= MAX_LOGIN_ATTEMPTS:
                    user.is_blocked = True
                    user.blocked_until = (
                        datetime.now(timezone.utc)
                        + timedelta(minutes=BLOCK_DURATION_MINS)
                    )
                    current_app.logger.warning(
                        f"User {user.username} blocked until {user.blocked_until} "
                        f"due to too many failed logins."
                    )
                db.session.commit()

            current_app.logger.warning(
                f"Failed login attempt for username: {form.username.data} "
                f"from IP: {request.remote_addr} - Invalid password"
            )
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

        # Successful login — clean up any deferred state.
        if user.scheduled_deletion is not None:
            user.scheduled_deletion = None
            current_app.logger.info(
                f"User {user.username} logged in. Scheduled deletion cancelled."
            )

        user.failed_login_attempts = 0
        user.is_blocked = False
        user.blocked_until = None
        user.get_token()
        db.session.commit()

        login_user(user, remember=form.remember_me.data)
        current_app.logger.info(
            f"User {user.username} logged in from IP: {request.remote_addr}"
        )

        next_page = request.args.get('next')
        # Reject absolute URLs in the `next` parameter to prevent open
        # redirect attacks; only relative paths (empty netloc) are safe.
        if next_page and urlsplit(next_page).netloc == '':
            return redirect(next_page)

        return redirect(url_for('user.dashboard'))

    return render_template('auth/login.html', title='Log In', form=form)


@auth_bp.route('/logout')
def logout():
    """Log out the current user and redirect to the landing page.

    Safe to call even when no user is authenticated; Flask-Login's
    :func:`~flask_login.logout_user` is a no-op in that case.

    Returns:
        flask.Response: A redirect to ``main.index``.
    """
    if current_user.is_authenticated:
        current_app.logger.info(f"User {current_user.username} has logged out.")
    logout_user()
    return redirect(url_for('main.index'))


@auth_bp.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per minute", methods=['POST'])
def register():
    """Display the registration form and create a new user account.

    ``GET`` renders the form. On a valid ``POST``, the submitted email
    is normalised (lower-cased and stripped) before the new
    :class:`~app.models.User` row is inserted. The session is flushed
    before committing so that the auto-generated primary key is available
    for :meth:`~app.models.User.get_token`, allowing the user to
    interact with the API immediately after registration without a
    separate token-request step.

    An :class:`~sqlalchemy.exc.IntegrityError` is caught to handle the
    race condition where two concurrent requests submit the same username
    or email after form-level uniqueness validation has already passed.

    Rate limited to **5 POST requests per minute** per remote IP.

    Returns:
        flask.Response: A rendered ``auth/register.html`` template on
        ``GET`` or failed validation, otherwise a redirect to
        ``auth.login`` on success.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = SignupForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data.lower().strip(),
        )
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.flush()
            user.get_token()
            db.session.commit()
        except sa.exc.IntegrityError:
            db.session.rollback()
            flash('Username or email already exists.')
            return redirect(url_for('auth.register'))

        current_app.logger.info(
            f"New user registered. Username: {user.username}, "
            f"email: ({user.email})"
        )
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title='Register', form=form)


@auth_bp.route('/reset_password_request', methods=['GET', 'POST'])
@limiter.limit('5 per minute', methods=['POST'])
def reset_password_request():
    """Display the password reset request form and dispatch a reset email.

    ``GET`` renders the form. On a valid ``POST``, the submitted email
    is looked up in the database. If a matching account is found,
    :func:`~app.auth.email.send_password_reset_email` is called;
    otherwise nothing is sent. In both cases the same flash message is
    displayed, intentionally giving no indication of whether the address
    is registered (account enumeration prevention).

    Rate limited to **5 POST requests per minute** per remote IP.

    Returns:
        flask.Response: A rendered ``auth/reset_password_request.html``
        template on ``GET`` or failed validation, otherwise a redirect
        to ``auth.login``.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        user = db.session.scalar(sa.select(User).where(User.email == email))
        current_app.logger.info(
            f"Password reset requested for email: {email} "
            f"from IP: {request.remote_addr}"
        )
        if user:
            send_password_reset_email(user)
            current_app.logger.info(f"Reset email sent to user_id={user.id}")

        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login'))

    return render_template(
        'auth/reset_password_request.html',
        title='Reset Password',
        form=form,
    )


@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
@limiter.limit('3 per minute', methods=['POST'])
def reset_password(token):
    """Verify a password reset token and set a new password.

    ``GET`` validates *token* via
    :meth:`~app.models.User.verify_reset_password_token` and renders
    the reset form if the token is valid, otherwise redirects to the
    login page. On a valid ``POST``, an additional check prevents the
    user from resetting to their current password before the new hash is
    persisted.

    Rate limited to **3 POST requests per minute** per remote IP —
    stricter than other auth endpoints because a valid token is already
    a privileged credential.

    Args:
        token (str): The signed JWT embedded in the reset link, supplied
            by Flask from the ``<token>`` URL segment.

    Returns:
        flask.Response: A rendered ``auth/reset_password.html`` template
        when the token is valid and the form has not yet been submitted
        successfully, otherwise a redirect to ``auth.login``.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    user = User.verify_reset_password_token(token)
    if not user:
        current_app.logger.warning(
            f"Invalid or expired reset token used from IP: {request.remote_addr}"
        )
        flash('Invalid or expired reset link.')
        return redirect(url_for('auth.login'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        if user.check_password(form.password.data):
            current_app.logger.info(
                f"User tried reusing old password: user_id={user.id}"
            )
            flash('Please choose a different password.')
            return redirect(url_for('auth.reset_password', token=token))

        user.set_password(form.password.data)
        db.session.commit()
        current_app.logger.info(
            f"Password successfully reset for user_id={user.id}"
        )
        flash('Your password has been reset. You can now log in.')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', form=form)