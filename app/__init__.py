from flask import Flask

app = Flask(__name__)

from app.users import users as users_blueprint
app.register_blueprint(users_blueprint)
from app.business import business as business_blueprint
app.register_blueprint(business_blueprint)
