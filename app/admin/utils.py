'''
app/admin/utils.py

Created by
Last modified 19/04/2026

This file contains helpers for the admin blueprint.
'''

from functools import wraps
from flask import abort
from flask_login import current_user

# we use a custom decorator based on flask-login's login-required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function