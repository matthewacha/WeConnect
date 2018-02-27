from flask import Blueprint

businessesv1 = Blueprint('business' , __name__, url_prefix='/api/v1')

from . import views
