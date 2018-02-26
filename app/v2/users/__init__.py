from flask import Blueprint

users = Blueprint('usersv2' , __name__)

from . import views
