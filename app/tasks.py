from datetime import datetime, timezone
import sqlalchemy as sa
from extensions import db
from app.models import User

def process_pending_deletions(app):

    with app.app_context():
        app.logger.info('Running process_pending_deletions task')
        now = datetime.now(timezone.utc)

        users = db.session.scalars(
            sa.select(User).where(
                User.scheduled_deletion.is_not(None),
                User.is_deleted.is_(False),
                User.scheduled_deletion <= now
            )
        ).all()
        app.logger.info(f'Found {len(users)} users pending deletion...')
        for user in users:
            user.is_deleted = True

        db.session.commit()
        app.logger.info('process_pending_deletions completed')


def cleanup_deleted_users(app):

    with app.app_context():
        app.logger.info('Running cleanup_deleted_users task')
        users = db.session.scalars(
            sa.select(User).where(
                User.is_deleted.is_(True)
            )
        ).all()
        app.logger.info(f'Found {len(users)} deleted users to remove')
        for user in users:
            db.session.delete(user)

        db.session.commit()
        app.logger.info('cleanup_deleted_users completed')