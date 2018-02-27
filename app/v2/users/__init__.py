from flask import Blueprint

users = Blueprint('usersv2' , __name__, url_prefix='/api/v2')

from . import views
