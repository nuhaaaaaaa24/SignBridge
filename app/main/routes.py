"""Route handlers for the main blueprint.

Serves the public-facing pages of the application: the landing page,
the about page, and the contact form. All views are unauthenticated
and ``GET``-only except for :func:`contact`, which also accepts
``POST`` submissions.

Note:
    :func:`contact` sends email directly via :mod:`smtplib` rather
    than through :func:`~app.core.email.send_email`. This is intentional
    — the contact form is outbound to the admin inbox and does not
    require the async dispatch or Flask-Mail configuration used for
    transactional emails sent *to* users.
"""

import smtplib
from email.message import EmailMessage

from flask import current_app, flash, redirect, render_template, url_for
from flask_login import current_user

from app.main import main_bp
from app.main.forms import ContactForm


@main_bp.route('/')
@main_bp.route('/index')
def index():
    """Render the application landing page.

    Accessible at both ``/`` and ``/index`` so that bare-domain
    requests are handled without a redirect.

    Returns:
        flask.Response: The rendered ``main/index.html`` template.
    """
    return render_template('main/index.html', title='Landing')


@main_bp.route('/about')
def about():
    """Render the about page.

    Returns:
        flask.Response: The rendered ``main/about.html`` template.
    """
    return render_template('main/about.html', title='About Us')


@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Display the contact form and dispatch submitted messages to the admin inbox.

    ``GET`` renders the empty form. On a valid ``POST``, constructs a
    plain-text :class:`~email.message.EmailMessage` from the submitted
    fields and sends it synchronously via :mod:`smtplib` over SMTP-SSL
    (port 465). The ``From`` address is the application's configured
    ``MAIL_USERNAME`` so that the message passes Gmail's authentication
    checks; the sender's actual address is included in the message body.

    On success the user is redirected back to ``main.contact`` with a
    confirmation flash. On any SMTP or runtime error the exception is
    logged at ``ERROR`` level and a generic failure message is flashed
    so that internal configuration details are not exposed to the
    visitor.

    Returns:
        flask.Response: The rendered ``main/contact.html`` template on
        ``GET`` or failed validation, otherwise a redirect to
        ``main.contact`` on success.
    """
    form = ContactForm()
    if form.validate_on_submit():
        try:
            msg = EmailMessage()
            msg['Subject'] = form.subject.data
            msg['From'] = current_app.config['MAIL_USERNAME']
            msg['To'] = "admin.signbridge+inquiries@gmail.com"
            msg.set_content(
                f"Name: {form.name.data}\n"
                f"Email: {form.email.data}\n\n"
                f"{form.message.data}"
            )
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(
                    current_app.config['MAIL_USERNAME'],
                    current_app.config['MAIL_PASSWORD'],
                )
                smtp.send_message(msg)

            flash("Message sent successfully!")
            return redirect(url_for('main.contact'))

        except Exception as e:
            current_app.logger.error(f"Contact form error: {e}")
            flash("Something went wrong. Please try again later.")

    return render_template('main/contact.html', title='Contact Us', form=form)