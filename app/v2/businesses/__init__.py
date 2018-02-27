from flask import Blueprint

businesses = Blueprint('businessesv2' , __name__, url_prefix='/api/v2')

from . import views
