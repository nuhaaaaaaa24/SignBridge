'''
models.py
Created by Shivangi Sritharan
Last modified: 18/04/2026

This file contains the code used to generate 
the application database. The code is implemented
with SQLAlchemy to maintain a DBMS-agnostic 
database script. We use Flask-Migrate elsewhere to
generate a migration script for the database.
'''

from datetime import datetime, timezone
from typing import Optional # to let values be a specific type or None (for nullable fields)
import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import timedelta
from flask import current_app, url_for
from extensions import db, login, bcrypt
from flask_login import UserMixin # this helper implements methods required by flask-login's session mgmt system
from hashlib import md5
from time import time
import jwt
import secrets
from datetime import datetime, timedelta, timezone

# flask-login expects that the application will configure a user loader function that can be called to load a user given the ID
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class User(UserMixin, db.Model):
    __tablename__ = "user" # explicitly set table name

    # enforce block logic
    __table_args__ = (
        sa.CheckConstraint(
            "(is_blocked = TRUE AND blocked_until IS NOT NULL) OR (is_blocked = FALSE AND blocked_until IS NULL)",
            name="block_timer_check"
        ),
    )

    # id is unique and also the primary key
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    # UNIQUE=TRUE (since users login with username)
    username: so.Mapped[str] = so.mapped_column(sa.String(50), index=True, unique=True, nullable=False)

    # email is email 
    email: so.Mapped[str] = so.mapped_column(sa.String(100), index=True, unique=True, nullable=False)

    # we store password hashes instead of raw passwords for security reasons
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(128), nullable=False)

    # last seen isnt necessary but is nice
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(default=lambda: datetime.now(timezone.utc))

    # is_admin checks if a user is admin or not
    is_admin: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False, nullable=False)

    # is_blocked is used when rate limiting to block users
    is_blocked: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False, nullable=False)

    # add timer to automatically unblock users
    blocked_until: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime, nullable=True)

    # failed_login_attempts is used to track the attempts a user makes before they
    # are automatically blocked
    # this should refresh when a user is unblocked.
    failed_login_attempts: so.Mapped[int] = so.mapped_column(default=0, nullable=False)

    # deletion flag
    is_deleted: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False, nullable=False)

    # add timer for account deletion
    scheduled_deletion: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime(timezone=True), nullable=True)

    # created_at tracks when a user was created
    created_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))

    # orm relationships for better querying
    rooms = db.relationship(
        "Room",
        back_populates="owner", # rooms.owner shows the owner of a room
        cascade="all, delete-orphan",
        passive_deletes=True # let db handle deletes instead of orm
    )
    rooms_joined = db.relationship(
        "Room",
        secondary="room_participant",
        back_populates="participants" # user.rooms_joined shows the rooms a user is in
    )
    messages = db.relationship(
        "Message", 
        back_populates="user", # user.messages shows a user's messages
        cascade="all, delete-orphan",
        passive_deletes=True # let db handle deletes instead of orm
    )

    # repr tells python how to print the table.
    # this is used for debugging
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    # we use bcrypt for password hashing and checking
    def set_password(self, password: str): # set the password hash for a user based on the raw password input
        # hashes the plaintext pw using bcrypt and stores the resulting has as a utf-8 string becuase bcrypt retruns bytes and we want to store it as a string in the db
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    # takes the plaintext password input and checks it against the stored hash, returning True if they match and False not
    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)
    
    # add profile pictures with Gravatar
    def avatar(self, size):
        # convert email to lowercase (required by gravatar) and encode 
        # the string as bytes so python can work with it (see https://docs.gravatar.com/avatars/python/)
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
    # reset password token
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in, 'ph': self.password_hash[-8:]},
            current_app.config['SECRET_KEY'], algorithm='HS256')
    
    def is_admin_user(self) -> bool:
        return self.is_admin
    
    # helper methods for user cleanup after deletion
    @property
    def pending_deletion(self) -> bool:
        return (
            self.days_until_deletion is not None
            and not self.is_deleted
        )

    @property
    def deletion_due(self) -> bool:
        return (
            self.days_until_deletion is not None
            and datetime.now(timezone.utc) >= self.days_until_deletion
        )
    
    def cleanup_deleted_users():
        users = db.session.scalars(
            sa.select(User).where(
                User.is_deleted.is_(True)
            )
        ).all()

        for user in users:
            db.session.delete(user)

        db.session.commit()

    # invokable from the class itself
    @staticmethod
    def verify_reset_password_token(token):
        try:
            data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            return db.session.get(User, data['reset_password'])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        
    # API
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
            'created_at': self.created_at.isoformat(),
            'is_admin': self.is_admin,
            '_links': {
                'self': url_for('api.get_user', id=self.id)
            }
        }
    
    token: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32), index=True, unique=True, nullable=True)
    token_expiration: so.Mapped[Optional[datetime]] = so.mapped_column(nullable=True)

    def get_token(self, expires_in=3600): # generate or return a valid API token for the current user
        now = datetime.now(timezone.utc) # get the current UTC time
        # check whether the user already has a token AND expiration time exists
        if self.token and self.token_expiration and \
            self.token_expiration.replace(tzinfo=timezone.utc) > now + timedelta(seconds=60): # ensure token is still valid for more than 60 seconds remaining
            return self.token # return existing token if it's still valid without with sufficient time to expire

        self.token = secrets.token_hex(16) # generate a new random token (32 hex characters)
        self.token_expiration = now + timedelta(seconds=expires_in) # set token expiration time from now (1 hour)

        db.session.add(self) # adds the current user object to the db session to track changes
        db.session.flush()   # forces SQLAlchemy to register changes

        return self.token # returns the generated token for the user to be used

    def revoke_token(self): 
        self.token_expiration = datetime.now(timezone.utc) - timedelta(seconds=1) # set expiration to past time (1 sec ago) to invalidate token

    @staticmethod # method belongs to the class, not a specific instance, because we want to check the token without needing a user instance
    def check_token(token): # check whether a given token is valid and return the associated user if it is
        user = db.session.scalar(sa.select(User).where(User.token == token)) # determine user linked to this token in db
        if user is None or user.token_expiration.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc): # check if token does not exist or expired
            return None
        # auto-renew if less than 60 seconds remaining
        if user.token_expiration.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc) + timedelta(seconds=60): # check if token is close to expiry (less than 60 sec left)
            user.get_token() # if it is close to expire, generate a new token instead of waiting current one to expire
            db.session.commit() # save renewed token to db
        return user # return authenticated user object

class Room(db.Model):
    __tablename__ = "room"

    # room_id
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    # room code (different!)
    room_code: so.Mapped[str] = so.mapped_column(sa.String(9), index=True, unique=True, nullable=False)
    # room created at (timezone currently UTC but may need to be changed)
    created_at: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc), nullable=False)
    # owner id - foreign key from the user table
    owner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id, ondelete="CASCADE"), index=True, nullable=False)

    # orm relationships
    owner = db.relationship(
        "User",
        back_populates="rooms", # user.rooms shows all rooms owned by a user
        passive_deletes=True
    )
    participants = db.relationship(
        "User",
        secondary="room_participant",
        viewonly=True  # read-only; managed directly via RoomParticipant
    )
    messages = db.relationship(
        "Message", 
        back_populates="room",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    transcripts = db.relationship(
        "Transcript",
        back_populates="room",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def __repr__(self):
        return '<Room {}>'.format(self.id)
    
    def to_dict(self):
        return {
            'id': self.id,
            'room_code': self.room_code,
            'created_at': self.created_at.isoformat(),
            'owner_id': self.owner_id,
            '_links': {
                'self': url_for('api.get_room', id=self.id),
                'messages': url_for('api.get_room_messages', id=self.id)
            }
        }

# users to rooms is a many to many relationship so this table exists to break it up
class RoomParticipant(db.Model):
    __tablename__ = "room_participant"
    # id
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    # user id 
    rp_user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id, ondelete="CASCADE"), index=True, nullable=False)
    # room id
    rp_room_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Room.id, ondelete="CASCADE"), index=True, nullable=False)

    def __repr__(self):
        return '<RoomParticipant {}>'.format(self.id)

# transcript generated by model
# can be started, stopped (ie a session can have multiple), can be downloaded
class Transcript(db.Model):
    __tablename__ = "transcript"
    # id
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    # content of transcript. this does not need to be unique and the table doesn't need to be indexed on it (storage issues)
    ts_content: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)
    # creation
    created_at: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc), nullable=False)
    # foreign key room id
    room_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Room.id, ondelete="CASCADE"), index=True, nullable=False)

    # orm relationships
    room = db.relationship("Room")

    def __repr__(self):
        return '<Transcript {}>'.format(self.ts_content)

# messages in the chat
class Message(db.Model):
    __tablename__ = "message"
    # id
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    # content
    msg_content: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)
    # creation
    created_at: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc), nullable=False)
    # user id 
    user_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey(User.id, ondelete="CASCADE"), index=True, nullable=True)
    # room id
    room_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Room.id, ondelete="CASCADE"), index=True, nullable=False)

    # orm relationships
    room = db.relationship(
        "Room", back_populates="messages" # message.room shows the room a message was sent in
    )
    
    user = db.relationship(
        "User", back_populates="messages" # message.user shows the owner of a message
    )

    def __repr__(self):
        return '<Message {}>'.format(self.msg_content)
    
    def to_dict(self):
        return {
            'id': self.id,
            'msg_content': self.msg_content,
            'created_at': self.created_at.isoformat(),
            'user_id': self.user_id,
            'room_id': self.room_id,
            'sender': self.user.username if self.user else 'Guest'
        }