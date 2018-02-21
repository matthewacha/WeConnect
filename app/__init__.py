from flask import Flask

app = Flask(__name__)

from app.users import users as users_blueprint
app.register_blueprint(users_blueprint)

from app.businesses import businesses as businesses_blueprint
app.register_blueprint(businesses_blueprint)
