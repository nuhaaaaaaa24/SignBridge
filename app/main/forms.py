'''
app/main/forms.py

Created by
Last modified 19/04/2026

This file contains the form to send emails 
through the Contact Us link.
'''

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

# Contact form for the main contact page.
# Allows any visitor (authenticated or not) to send a message to the site admins.
class ContactForm(FlaskForm):
    name = StringField(
        'Your Name', 
        validators=[DataRequired(), Length(max=100)],
        render_kw={"class": "input", "placeholder": "Your Name"}
    )

    # senders email address must be a valid email format.
    email = StringField(
        'Your Email', 
        validators=[DataRequired(), Email()],
        render_kw={"class": "input", "placeholder": "Your E-mail"}
    )
    
    # message subject is required and has a max length of 150 characters.
    subject = StringField(
        'Subject', 
        validators=[DataRequired(), Length(max=150)],
        render_kw={"class": "input", "placeholder": "Subject"}
    )

    # Message body is required and must be at least 10 characters long to ensure meaningful content.
    message = TextAreaField(
        'Message', 
        validators=[DataRequired(), Length(min=10)],
        render_kw={"class": "input", "placeholder": "Your Message"}
    )

    submit = SubmitField(
        'Send Message',
        render_kw={"class": "btn btn-primary btn-block"}
    )