'''
config.py
Created by Nuha Rilwan
Last modified: 10/04/2026

This file contains configuration stuff.
'''

import os
from datetime import timedelta # for session lifetime
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env')) # set variables before class is constructed

class Config:

    # runtime errors for everything now thumbsup.jpg
    def get_env_variable(var_name):
        value = os.environ.get(var_name)
        if not value:
            raise RuntimeError(f"{var_name} is not set. Aborting launch sequence.")
        return value

    SECRET_KEY = get_env_variable('SECRET_KEY') # secret key for token generation
    PERMANENT_SESSION_LIFETIME = get_env_variable('PERMANENT_SESSION_LIFETIME') # session lifetime of 30 minutes. This means that if a user is inactive for 30 minutes, they will be logged out. This is a security measure to prevent unauthorized access to accounts.
    uri = get_env_variable('DATABASE_URL') # secret key for token generation
    
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql+psycopg2://", 1)

    SQLALCHEMY_DATABASE_URI = uri 

    # the flask-limiter extension stores data in this
    # because limiter uses the limit library this is kept separate from sqlalchemy
    RATELIMIT_STORAGE_URI = get_env_variable("RATELIMIT_STORAGE_URI")
    RATELIMIT_STRATEGY = get_env_variable("RATELIMIT_STRATEGY") # enforce default rate limit time window of 1 minute. (moving window)
    
    # admin email stuff
    MAIL_SERVER = get_env_variable('MAIL_SERVER')
    MAIL_PORT = get_env_variable('MAIL_PORT')
    MAIL_USE_TLS = get_env_variable('MAIL_USE_TLS')
    MAIL_USERNAME = get_env_variable('MAIL_USERNAME')
    MAIL_PASSWORD = get_env_variable('MAIL_PASSWORD')
    ADMINS = ['admin.signbridge+errors@gmail.com']

    # recaptcha
    RECAPTCHA_PUBLIC_KEY = get_env_variable("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = get_env_variable("RECAPTCHA_PRIVATE_KEY")
