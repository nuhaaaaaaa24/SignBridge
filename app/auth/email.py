"""Password reset email dispatch for the auth blueprint.

Kept separate from other email helpers in :mod:`app.core.email` because
it is the only mailer that requires generating a signed token — coupling
token creation and email dispatch into one call keeps the auth views
clean and ensures the two steps are never accidentally separated.

Note:
    This module must be called within an active Flask application context.
    :func:`~flask.current_app` is used to read ``ADMINS`` from the config,
    and :func:`~flask.render_template` requires the application context to
    locate the template folder. Both are satisfied automatically when the
    function is called from within a request or an explicit
    ``with app.app_context()`` block.
"""

from flask import current_app, render_template

from app.core.email import send_email


def send_password_reset_email(user):
    """Generate a password reset token and dispatch the reset email.

    Calls :meth:`~app.models.User.get_reset_password_token` to produce a
    short-lived signed JWT, then delegates to :func:`~app.core.email.send_email`
    with both a plain-text and an HTML body so that mail clients without
    HTML rendering can still present a usable link.

    The sender address is taken from the first entry of the ``ADMINS``
    config key so that replies and bounce notifications are routed to the
    admin inbox rather than a no-reply black hole.

    Args:
        user (app.models.User): The account requesting the password reset.
            Must expose a :meth:`~app.models.User.get_reset_password_token`
            method and an :attr:`~app.models.User.email` attribute.

    Example:
        Sending a reset email from an auth view::

            from app.auth.email import send_password_reset_email

            user = User.query.filter_by(email=form.email.data).first()
            if user:
                send_password_reset_email(user)
    """
    token = user.get_reset_password_token()
    send_email(
        '[SignBridge] Reset Your Password',
        sender=current_app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template('email/reset_password.txt', user=user, token=token),
        html_body=render_template('email/reset_password.html', user=user, token=token),
    )