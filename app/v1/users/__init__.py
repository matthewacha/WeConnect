from flask import Blueprint

usersv1 = Blueprint('users' , __name__, url_prefix='/api/v1')

from . import views
