'''
app/admin/forms.py
Created by 
Last modified: 19/04/2026

This file contains the server-side code for 
admin-related forms. The forms are 
implemented with Flask-WTForms.
'''

from flask_wtf import FlaskForm
from wtforms import SubmitField

class ToggleAdminForm(FlaskForm):
    submit = SubmitField('Toggle Admin')

class DeleteUserForm(FlaskForm):
    submit = SubmitField('Delete')

class UnblockUserForm(FlaskForm):
    submit = SubmitField('Unblock User')