"""Background tasks for deferred user account deletion.

This module implements the two-phase account removal pipeline that runs
on an hourly schedule via :class:`~apscheduler.schedulers.background.BackgroundScheduler`
(registered in :func:`app.create_app`).

**Phase 1 — :func:`process_pending_deletions`**
    Marks accounts as logically deleted once their scheduled deletion
    timestamp has elapsed. The account still exists in the database at
    this point, giving the pipeline a recoverable intermediate state.

**Phase 2 — :func:`cleanup_deleted_users`**
    Permanently removes all rows that were marked ``is_deleted = True``
    in Phase 1, along with any cascade-deleted related records.

Separating the two phases means that a crash or restart between them
leaves accounts in a soft-deleted state rather than partially removed,
which is far easier to reason about and recover from.

Note:
    Both functions accept an explicit *app* argument and open their own
    :func:`~flask.Flask.app_context`. This is required because APScheduler
    runs jobs on background threads that have no Flask context of their own.
"""

from datetime import datetime, timezone

import sqlalchemy as sa

from app.models import User
from extensions import db


def process_pending_deletions(app):
    """Mark accounts as logically deleted once their deletion date has passed.

    Queries for :class:`~app.models.User` rows where
    :attr:`~app.models.User.scheduled_deletion` is in the past and
    :attr:`~app.models.User.is_deleted` is still ``False``, then flips
    ``is_deleted`` to ``True`` in a single committed transaction.

    This is Phase 1 of the two-phase deletion pipeline. Rows are *not*
    removed here; that is deferred to :func:`cleanup_deleted_users` so
    that the two operations can fail independently without leaving the
    database in an inconsistent state.

    Args:
        app (flask.Flask): The application instance used to push an
            application context onto the background thread. Passed in
            explicitly by APScheduler; see :func:`app.create_app` for
            the scheduler registration.

    Example:
        Manually triggering the task outside of APScheduler::

            from app import create_app
            from app.tasks import process_pending_deletions

            process_pending_deletions(create_app())
    """
    with app.app_context():
        app.logger.info('Running process_pending_deletions task')

        now = datetime.now(timezone.utc)

        users = db.session.scalars(
            sa.select(User).where(
                User.scheduled_deletion.is_not(None),
                User.is_deleted.is_(False),
                User.scheduled_deletion <= now,
            )
        ).all()

        app.logger.info(f'Found {len(users)} users pending deletion...')

        for user in users:
            user.is_deleted = True

        db.session.commit()
        app.logger.info('process_pending_deletions completed')


def cleanup_deleted_users(app):
    """Permanently remove all rows previously marked as logically deleted.

    Queries for :class:`~app.models.User` rows where
    :attr:`~app.models.User.is_deleted` is ``True`` and calls
    :meth:`~sqlalchemy.orm.Session.delete` on each, relying on
    SQLAlchemy's cascade rules to remove related records (sessions,
    messages, etc.) in the same transaction.

    This is Phase 2 of the two-phase deletion pipeline and should only
    run *after* :func:`process_pending_deletions` has had the opportunity
    to promote eligible accounts to the soft-deleted state.

    .. warning::
        Deletion is **irreversible**. Once this task commits, affected
        rows and all their cascaded dependents are permanently gone.

    Args:
        app (flask.Flask): The application instance used to push an
            application context onto the background thread. Passed in
            explicitly by APScheduler; see :func:`app.create_app` for
            the scheduler registration.

    Example:
        Manually triggering the task outside of APScheduler::

            from app import create_app
            from app.tasks import cleanup_deleted_users

            cleanup_deleted_users(create_app())
    """
    with app.app_context():
        app.logger.info('Running cleanup_deleted_users task')

        users = db.session.scalars(
            sa.select(User).where(
                User.is_deleted.is_(True),
            )
        ).all()

        app.logger.info(f'Found {len(users)} deleted users to remove')

        for user in users:
            db.session.delete(user)

        db.session.commit()
        app.logger.info('cleanup_deleted_users completed')