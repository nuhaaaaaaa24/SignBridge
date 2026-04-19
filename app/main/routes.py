'''
app/main/routes.py
Created by Shivangi Sritharan
Last modified: 18/04/2026

This file contains routes for webpages in the
main blueprint.
'''

from flask import render_template, redirect, url_for, flash, current_app
from flask_login import current_user
from app.main import main_bp
from app.main.forms import ContactForm
import smtplib # handles emails
from email.message import EmailMessage

# route for landing page
@main_bp.route('/')
@main_bp.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('user.profile'))
    return render_template('main/index.html', title='Landing')

# route for about page
@main_bp.route('/about')
def about():
    return render_template('main/about.html', title='About Us')

# route for contact page
@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    # send emails through contact page
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
                    current_app.config['MAIL_PASSWORD']
                )
                smtp.send_message(msg)

            flash("Message sent successfully!")
            return redirect(url_for('main.contact'))

        except Exception as e:
            current_app.logger.error(f"Contact form error: {e}")
            flash("Something went wrong. Please try again later.")

    return render_template('main/contact.html', title='Contact Us', form=form)