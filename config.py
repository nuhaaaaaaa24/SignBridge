import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env')) # set variables before class is constructed

class Config:
    # secret key for token generation
    # todo: add a real secret key lol
    SECRET_KEY = os.environ.get('SECRET_KEY') or "you-will-never-guess"

    # the flask-SQLAlchemy extension takes the location of the application's 
    # database from the SQLALCHEMY_DATABASE_URI configuration variable
    # if the url isn't defined in DATABASE_URL it will fall back to
    # app.db found locally.
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    #SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://signbridge:thesbdatabase123@localhost:5432/signbridgedb'

    uri = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')

    if not uri:
        raise RuntimeError("DATABASE_URL is not set. Application will not start.")

    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql+psycopg2://", 1)

    SQLALCHEMY_DATABASE_URI = uri

    # the flask-limiter extension stores data in this
    # because limiter uses the limit library this is kept separate from sqlalchemy
    RATELIMIT_STORAGE_URI = os.environ.get("RATELIMIT_STORAGE_URI", "memory://")
    
    # admin email mailing list lol
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = "587"
    MAIL_USE_TLS = "1"
    MAIL_USERNAME = "admin.signbridge@gmail.com"
    MAIL_PASSWORD = "gtoa yyxu nigi ptai"
    ADMINS = ['admin.signbridge+errors@gmail.com']
