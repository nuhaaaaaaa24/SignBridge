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

class ContactForm(FlaskForm):
    name = StringField(
        'Your Name', 
        validators=[DataRequired(), Length(max=100)],
        render_kw={"class": "input", "placeholder": "Your Name"}
    )

    email = StringField(
        'Your Email', 
        validators=[DataRequired(), Email()],
        render_kw={"class": "input", "placeholder": "Your E-mail"}
    )

    subject = StringField(
        'Subject', 
        validators=[DataRequired(), Length(max=150)],
        render_kw={"class": "input", "placeholder": "Subject"}
    )

    message = TextAreaField(
        'Message', 
        validators=[DataRequired(), Length(min=10)],
        render_kw={"class": "input", "placeholder": "Your Message"}
    )

    submit = SubmitField(
        'Send Message',
        render_kw={"class": "btn btn-primary btn-block"}
    )