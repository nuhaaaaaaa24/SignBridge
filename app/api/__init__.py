from flask import Blueprint
from extensions import csrf

api_bp = Blueprint('api', __name__)

csrf.exempt(api_bp)

from app.api import tokens, users, rooms, errors