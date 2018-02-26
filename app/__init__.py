from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
db.init_app(app)

from app.v2 import models


from app.v1.users import usersv1 as usersv1_blueprint
app.register_blueprint(usersv1_blueprint)

from app.v1.businesses import businessesv1 as businessesv1_blueprint
app.register_blueprint(businessesv1_blueprint)

from app.v2.users import users as usersv2_blueprint
app.register_blueprint(usersv2_blueprint)

#from app.v2.businesses import businesses as businessesv2_blueprint
#app.register_blueprint(businessesv2_blueprint)
