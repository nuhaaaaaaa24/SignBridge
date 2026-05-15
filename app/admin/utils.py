"""Helper utilities for the admin blueprint.

Provides route decorators that enforce admin-only access on top of
Flask-Login's standard authentication checks.
"""

from functools import wraps

from flask import abort
from flask_login import current_user


def admin_required(f):
    """Decorator that restricts a route to authenticated admin users.

    Extends Flask-Login's ``@login_required`` pattern by adding a second
    check for :attr:`~app.models.User.is_admin`. Unauthenticated users
    and authenticated non-admins both receive a ``403 Forbidden``
    response, intentionally giving no hint about the existence of the
    admin interface.

    Args:
        f (Callable): The view function to protect.

    Returns:
        Callable: The wrapped view function with admin enforcement applied.

    Raises:
        werkzeug.exceptions.Forbidden: (HTTP 403) If the current user is
            not authenticated or does not have ``is_admin = True``.

    Example:
        Protecting an admin-only route::

            from app.admin.helpers import admin_required

            @admin_bp.route('/dashboard')
            @login_required
            @admin_required
            def dashboard():
                return render_template('admin/dashboard.html')
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function