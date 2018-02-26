from flask import Blueprint

usersv1 = Blueprint('users' , __name__)

from . import views
