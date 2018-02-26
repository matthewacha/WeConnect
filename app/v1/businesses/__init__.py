from flask import Blueprint

businessesv1 = Blueprint('business' , __name__)

from . import views
