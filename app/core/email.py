"""Shared email dispatch utilities.

Provides a thin asynchronous wrapper around Flask-Mail that is reused
by any blueprint that needs to send email (e.g. password reset in
:mod:`app.auth.email`). Sending is offloaded to a daemon thread so
that the HTTP response is never delayed by SMTP negotiation.

Note:
    :func:`send_email` must be called within an active Flask request or
    application context. The current application object is captured via
    :meth:`~flask.Flask._get_current_object` before the thread starts
    so that the daemon thread receives a concrete reference rather than
    the request-local proxy, which would be invalid once the originating
    context is torn down.
"""

from threading import Thread
from flask import current_app
from flask_mail import Message
from extensions import mail

def send_async_email(app, msg: Message) -> None:
    """Send a :class:`~flask_mail.Message` inside a background thread.

    Pushes a new application context onto the background thread before
    calling :meth:`~flask_mail.Mail.send`, because Flask-Mail reads
    SMTP configuration from the app config and requires an active
    context to do so.

    Args:
        app (flask.Flask): The concrete application instance (not the
            proxy). Must be obtained via
            :meth:`~flask.Flask._get_current_object` in the calling
            thread before the :class:`~threading.Thread` is started.
        msg (flask_mail.Message): The fully constructed message to send,
            including subject, sender, recipients, and body.
    """
    with app.app_context():
        mail.send(msg)


def send_email(
    subject: str,
    sender: str,
    recipients: list[str],
    text_body: str,
    html_body: str,
) -> None:
    """Construct and dispatch an email asynchronously.

    Builds a :class:`~flask_mail.Message` from the supplied arguments
    and hands it off to :func:`send_async_email` running on a
    :class:`~threading.Thread`, returning immediately so the caller's
    response time is not affected by SMTP latency.

    Args:
        subject (str): The email subject line.
        sender (str): The ``From`` address. Typically the first entry of
            the ``ADMINS`` config key (e.g.
            ``current_app.config['ADMINS'][0]``).
        recipients (list[str]): One or more ``To`` addresses.
        text_body (str): Plain-text fallback body for mail clients that
            do not render HTML.
        html_body (str): HTML body for clients that support rich
            rendering.

    Example:
        Sending a notification email from any blueprint::

            from app.core.email import send_email

            send_email(
                subject='[SignBridge] Welcome',
                sender=current_app.config['ADMINS'][0],
                recipients=[user.email],
                text_body=render_template('email/welcome.txt', user=user),
                html_body=render_template('email/welcome.html', user=user),
            )
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(
        target=send_async_email,
        args=(current_app._get_current_object(), msg),
    ).start()