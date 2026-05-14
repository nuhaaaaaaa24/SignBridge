from flask import Blueprint # import Blueprint from the flask library to create a seperate module for admin routes

admin_bp = Blueprint('admin', __name__) # create the admin blueprint named 'admin' and the current module's name

from app.admin import routes # import the admin routes so they are registered with this bp