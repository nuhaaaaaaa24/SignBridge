'''
app/admin/forms.py
Created by 
Last modified: 19/04/2026

This file contains the server-side code for 
admin-related forms. The forms are 
implemented with Flask-WTForms.
'''

from flask_wtf import FlaskForm # to get automatic CSRF protection for our forms
from wtforms import SubmitField # import submit button field to generate the clickable buttons

class ToggleAdminForm(FlaskForm): # form used by admins to toggle the admin status or remove admin privileges
    submit = SubmitField('Toggle Admin') #

class DeleteUserForm(FlaskForm): # form used by admins to delete a user from the system
    submit = SubmitField('Delete')

class UnblockUserForm(FlaskForm): # form used by admins to unblock a user that was previously blocked
    submit = SubmitField('Unblock User')