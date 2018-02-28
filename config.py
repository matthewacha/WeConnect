import os
from app import app

#define directory for application
BASEDIR = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = 'we_do_business_everyday'

class Development():
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/weconnect'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'we_do_business_everyday'
class Deployment():
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'we_do_business_everyday'
    
configure = {'dev':Development, 'dep':Deployment}
