'''
app/user/routes.py
Created by Shivangi Sritharan
Last modified: 18/04/2026

This file contains user-related page
routes.
'''

from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import current_user, login_required, logout_user
from email.message import EmailMessage
import sqlalchemy as sa
import smtplib
from extensions import db, limiter
from app.user.forms import EditProfileForm, EmptyForm, DeleteAccountRequestForm, DeleteUserForm
from app.models import User
from app.user import user_bp
from datetime import timedelta, timezone, datetime

#route for user dashboard page
@user_bp.route('/dashboard')
@login_required
def dashboard():
    form = EmptyForm()
    delete_form = DeleteUserForm()

    return render_template('user/dashboard.html', title='Dashboard', form=form, delete_form=delete_form)

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
# keeping this for now
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

# route to let users delete their accounts
@user_bp.route('/user/<int:id>/delete', methods=['POST'])
@limiter.limit('5 per minute', methods=['POST'])
@login_required
def delete_user(id):
    form = DeleteUserForm()

    if not form.validate_on_submit():
        flash('Invalid request.')
        return redirect(url_for('user.profile'))
    
    user = User.query.get_or_404(id)

    if user != current_user:
        flash('You cannot delete other users\' accounts.')
        return redirect(url_for('user.profile'))
    
    try:

        # stop users from trying again if they already clicked delete
        if user.scheduled_deletion is not None:
            remaining = (user.scheduled_deletion - datetime.now(timezone.utc)).days
            flash(f"Your account is already scheduled for deletion. You have {remaining} days remaining.")
            return redirect(url_for('user.profile'))
        
        # verify password
        if not user.check_password(form.password.data):
            flash('Incorrect password.')
            return redirect(url_for('user.profile'))
        
        # schedule deletion
        user.is_deleted = False
        user.scheduled_deletion = (datetime.now(timezone.utc) + timedelta(minutes=5))

        # revoke api token
        user.revoke_token()

        db.session.commit()
        current_app.logger.info(f"User {user.username} has scheduled deletion of their account.")

        flash('Your account has been scheduled for deletion in 30 days. Log in to cancel at any time before that.')

        # log user out
        logout_user()
        return redirect(url_for("main.index"))

    except Exception as e:
        db.session.rollback()
        current_app.logger.exception(f"Account deletion failed for user_id={current_user.id}, username={current_user.username}")
        flash('An error has occurred. Please try again later.')
        return redirect(url_for('user.profile'))