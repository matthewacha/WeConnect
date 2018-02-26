import os
from app import app

#define directory for application
BASEDIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/weconnect'
WTF_CSRF_ENABLED = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = 'we_do_business_everyday'

SWAGGER = {}
