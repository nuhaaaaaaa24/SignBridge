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

    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30) # session lifetime of 30 minutes. This means that if a user is inactive for 30 minutes, they will be logged out. This is a security measure to prevent unauthorized access to accounts.
    SECRET_KEY = os.environ.get('SECRET_KEY') # secret key for token generation

    uri = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql+psycopg2://", 1)

    SQLALCHEMY_DATABASE_URI = uri 

    # the flask-limiter extension stores data in this
    # because limiter uses the limit library this is kept separate from sqlalchemy
    RATELIMIT_STORAGE_URI = os.environ.get("RATELIMIT_STORAGE_URI", "memory://")
    RATELIMIT_STRATEGY = 'moving-window' # enforce default rate limit time window of 1 minute.
    
    # admin email stuff
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['admin.signbridge+errors@gmail.com']