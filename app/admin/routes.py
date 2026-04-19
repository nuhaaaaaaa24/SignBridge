from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User
from app.admin import admin_bp
from app.admin.utils import admin_required
from app.admin.forms import ToggleAdminForm, UnblockUserForm, DeleteUserForm

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    users = User.query.order_by(User.username).all()
    toggle_form = ToggleAdminForm()
    unblock_form = UnblockUserForm()
    delete_form = DeleteUserForm()
    return render_template('admin/admin-dashboard.html', title='Admin Dashboard', users=users, toggle_form=toggle_form, unblock_form=unblock_form, delete_form=delete_form)

@admin_bp.route('/user/<int:id>/toggle-admin', methods=['POST'])
@login_required
@admin_required
def toggle_admin(id):
    user = User.query.get_or_404(id)
    if user == current_user:
        flash('You cannot change your own admin status.')
        return redirect(url_for('admin.dashboard'))
    user.is_admin = not user.is_admin
    db.session.commit()
    flash(f'Admin status updated for {user.username}.')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/user/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if user == current_user:
        flash('You cannot delete yourself.')
        return redirect(url_for('admin.dashboard'))
    try:
        # delete all rooms owned by this user
        for room in user.rooms:
            db.session.delete(room)

        # now delete the user
        db.session.delete(user)

        db.session.commit()
        flash(f'User {user.username} deleted.')

    except Exception as e:
        db.session.rollback()
        flash('Error deleting user.')
        
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/user/<int:id>/unblock', methods=['POST'])
@login_required
@admin_required
def unblock_user(id):
    user = User.query.get_or_404(id)

    if not user.is_blocked:
        flash(f'{user.username} is not blocked.')
        return redirect(url_for('admin.dashboard'))

    user.is_blocked = False
    user.failed_login_attempts = 0  # reset attempts

    db.session.commit()

    flash(f'User {user.username} has been unblocked.')
    return redirect(url_for('admin.dashboard'))
