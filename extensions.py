'''
extensions.py

Created by Shivangi Sritharan
Last modified: 13/04/2026

This file is used to initialize extensions to the application.
It exists to solve the problem of circular dependencies when
importing certain modules (e.g. socketio, database) directly
from the app.
'''

from flask_sqlalchemy import SQLAlchemy # for database
from flask_migrate import Migrate # for database migrations
from flask_login import LoginManager # for logins
from flask_login import current_user # to tie user id to rate limits
from flask_wtf import CSRFProtect # to protect against csrf attacks
from flask_mail import Mail # to manage email sending
from flask_moment import Moment # for time stamps
from flask_limiter import Limiter # for rate limiting
from flask_limiter.util import get_remote_address # for rate limiting
from flask_socketio import SocketIO # for websocket access
from flask_bcrypt import Bcrypt # for password hashing
from flask import request
import os
# initialize all modules
db = SQLAlchemy() # db represents the database object
migrate = Migrate() # migrate represents the migration engine
login = LoginManager()
csrf = CSRFProtect()
mail = Mail()
moment = Moment() 
socketio = SocketIO()
bcrypt = Bcrypt()

# reverse proxy forwarding bc of render
def get_ip():
    xff = request.headers.get("X-Forwarded-For", request.remote_addr)
    if xff and "," in xff:
        return xff.split(",")[0].strip()
    return xff

# tie rate limits to user id if signed in
def user_or_ip_key():
    if current_user.is_authenticated:
        return f"user:{current_user.id}"
    return f"ip:{get_ip()}"

limiter = Limiter(key_func=user_or_ip_key,
                  strategy="moving-window",)

login.login_view = 'auth.login'
login.login_message = ('Please log in to access this page.')