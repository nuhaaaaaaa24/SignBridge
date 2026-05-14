'''
app/auth/auth.py
Created by Nuha Rilwan
Last modified 22/04/2026


'''
import sqlalchemy as sa
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from extensions import db
from app.models import User
from app.api.errors import error_response

# HTTP Basic and Token auth instances for the API blueprint.
# Basic auth is used only to obtain a token (POST /api/tokens).
# Token auth is used for all other protected API endpoints.
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

# Verify username and password for basic auth.
# Returns the User object if credentials are valid, None otherwise.
@basic_auth.verify_password
def verify_password(username, password):
    user = db.session.scalar(sa.select(User).where(User.username == username))
    if user and user.check_password(password):
        return user

# Return a JSON error response instead of the default HTML for basic auth failures.
@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status)

# Verify bearer token for token auth.
# Returns the User object if the token is valid and not expired, None otherwise.
@token_auth.verify_token
def verify_token(token):
    return User.check_token(token) if token else None

# Return a JSON error response instead of the default HTML for token auth failures.
@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)