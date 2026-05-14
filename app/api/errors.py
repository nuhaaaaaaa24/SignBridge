'''
app/auth/errors.py
Created by Nuha Rilwan
Last modified 22/04/2026


'''
from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.exceptions import HTTPException
from app.api import api_bp

# Build a JSON error with the HTTP status code and an optional message.
# Uses Werkzeug's HTTP_STATUS_CODES to get the default message for the status code.
def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    return payload, status_code

# shortcut for 400 Bad Request with a custom message
def bad_request(message):
    return error_response(400, message)

# Catch all HTTP exceptions raised within the API blueprint and return JSON instead of HTML.
@api_bp.errorhandler(HTTPException)
def handle_exception(e):
    return error_response(e.code)