from datetime import datetime, timezone
import sqlalchemy as sa
from extensions import db
from app.models import User

def process_pending_deletions(app):

    with app.app_context():

        now = datetime.now(timezone.utc)

        users = db.session.scalars(
            sa.select(User).where(
                User.scheduled_deletion.is_not(None),
                User.is_deleted.is_(False),
                User.scheduled_deletion <= now
            )
        ).all()

        for user in users:
            user.is_deleted = True

        db.session.commit()


def cleanup_deleted_users(app):

    with app.app_context():

        users = db.session.scalars(
            sa.select(User).where(
                User.is_deleted.is_(True)
            )
        ).all()

        for user in users:
            db.session.delete(user)

        db.session.commit()