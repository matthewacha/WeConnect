import os
from app import app

#define directory for application
BASEDIR = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = 'we_do_business_everyday'

class Development():
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/weconnect'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'we_do_business_everyday'
    SWAGGER = {
            'swagger': '2.0',
            'title': 'we-connect-api',
            'description': "The we-connect-you app allows you to register a business and\
            make reviews of other businesses",
            'basePath': '/',
            'version': '0.0.1',
            'contact': {
                'Developer': 'Matthew Wacha',
                'email': 'matthewacha@gmail.com'
            },
            'license': {
            },
            'tags': [
                {
                    'name': 'User',
                    'description': 'The user of the api'
                },
                {
                    'name': 'Business',
                    'description': 'Business a user adds,updates, deletes'
                },
                {
                    'name': 'Review',
                    'description': 'A users analytical rating of a business'
                },
            ]
        }
class Deployment():
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'we_do_business_everyday'
    SWAGGER = {
            'swagger': '2.0',
            'title': 'we-connect-api',
            'description': "The we-connect-you app allows you to register a business and\
            make reviews of other businesses",
            'basePath': '/',
            'version': '0.0.1',
            'contact': {
                'Developer': 'Matthew Wacha',
                'email': 'matthewacha@gmail.com'
            },
            'license': {
            },
            'tags': [
                {
                    'name': 'User',
                    'description': 'The user of the api'
                },
                {
                    'name': 'Business',
                    'description': 'Business a user adds,updates, deletes'
                },
                {
                    'name': 'Review',
                    'description': 'A users analytical rating of a business'
                },
            ]
        }
configure = {'dev':Development, 'dep':Deployment}
