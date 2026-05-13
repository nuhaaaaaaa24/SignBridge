'''
app/user/routes.py
Created by Shivangi Sritharan
Last modified: 18/04/2026

This file contains user-related page
routes.
'''

from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import current_user, login_required
from email.message import EmailMessage
import sqlalchemy as sa
import smtplib
from extensions import db, limiter
from app.user.forms import EditProfileForm, EmptyForm, DeleteAccountRequestForm
from app.models import User
from app.user import user_bp

#route for user dashboard page
@user_bp.route('/dashboard')
@login_required
def dashboard():
    form = EmptyForm()
    return render_template('user/dashboard.html', title='Dashboard', form=form)

# route for user profile page
@user_bp.route('/profile')
@login_required # for obvious reasons
def profile():
    form = EmptyForm()
    return render_template('user/user.html', title='Your Account', user=current_user, form=form)

# route for edit user page
@user_bp.route('/edit_profile', methods=['GET', 'POST'])
@limiter.limit('5 per minute', methods=['POST'])
@login_required # for obvious reasons
def edit_profile():
    form = EditProfileForm(current_user.username, current_user.email, obj=current_user)

    if form.validate_on_submit():
        changes = [] # used to log changes without exposing the values to the viewer
        # update username/email
        if form.username.data:
            changes.append(f"username {current_user.username} has changed to new username: {form.username.data}")
            current_user.username = form.username.data

        if form.email.data:
            changes.append(f"email {current_user.email} has changed to new email: {form.email.data}")
            current_user.email = form.email.data

        # update password if provided
        if form.new_password.data:
            changes.append("password has been updated")
            current_user.set_password(form.new_password.data)

        db.session.commit()
        current_app.logger.info(f"Profile updated: user_id={current_user.id} changes={changes} ip={request.remote_addr}")
        flash("Profile updated successfully")

        return redirect(url_for('user.profile'))

    return render_template('user/edit-profile.html', title='Edit Profile', form=form, user=current_user)

# requesting account deletion
@user_bp.route('/delete_account_request', methods=['GET', 'POST'])
@login_required
def delete_account_request():
    form = DeleteAccountRequestForm()

    if form.validate_on_submit():
        try:
            msg = EmailMessage()
            msg['Subject'] = "SignBridge Account Deletion Request"
            msg['From'] = current_app.config['MAIL_USERNAME']
            msg['To'] = "admin.signbridge+support@gmail.com"

            msg.set_content(
                f"Account deletion request received.\n\n"
                f"User ID: {current_user.id}\n"
                f"Username: {current_user.username}\n"
                f"Email: {current_user.email}\n\n"
                f"Reason:\n{form.reason.data}\n\n"
                f"Action required: Please review this request before deleting the account."
            )

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(
                    current_app.config['MAIL_USERNAME'],
                    current_app.config['MAIL_PASSWORD']
                )
                smtp.send_message(msg)

            current_app.logger.info(
                f"Account deletion requested: user_id={current_user.id} ip={request.remote_addr}"
            )

            flash("Your account deletion request has been submitted for admin review.")
            return redirect(url_for('user.profile'))

        except Exception as e:
            current_app.logger.error(f"Account deletion request error: {e}")
            flash("Something went wrong. Please try again later.")

    return render_template('user/delete-account.html',title='Request Account Deletion',form=form)
