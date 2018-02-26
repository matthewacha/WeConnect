from flask import Blueprint

businesses = Blueprint('businessesv2' , __name__)

from . import views
