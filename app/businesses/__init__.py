from flask import Blueprint

businesses = Blueprint('business' , __name__)

from . import views
