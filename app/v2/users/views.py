import os#pragma:no cover
import jwt#pragma:no cover
import datetime#pragma:no cover
from flask import Flask, jsonify, request, session, make_response#pragma:no cover
from flasgger.utils import swag_from
from werkzeug.security import generate_password_hash, check_password_hash#pragma:no cover
from functools import wraps#pragma:no cover
from . import users#pragma:no cover
from app import app, db, models#pragma:no cover
from app.v2.models import User
from json import dumps#pragma:no cover

def token_required(funct):
    @wraps(funct)
    def decorated_funct(*args, **kwargs):
        token = None
        if 'access_token' in request.headers:
            token = request.headers['access_token']
            if not token:
                return jsonify({"message":"Token is missing"}), 401#pragma:no cover
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
                user = models.User.query.filter_by(id=data['sub']).first()
                current_user = user
            except:
                return jsonify({"message":"Token is invalid"}), 401
            return funct(current_user, *args, **kwargs)
        else:
            return jsonify({"error": "Token required"}), 401
    return decorated_funct

@users.route('/auth/register', methods = ['POST'])
#@swag_from('../api-docs/v2/register_user.yml')
def add_new_user():
    json_data = request.get_json()
    user = models.User(email = json_data['email'],
                       password = generate_password_hash(json_data['password']))
    
    try:
        db.session.add(user)
        db.session.commit()
        message = 'Successfully signed up'
    except:
        return make_response(("User already exists"), 401)
    db.session.close()
    return jsonify({'message':message})

@users.route('/auth/login', methods = ['POST'])
def login():
    data=request.get_json()
    if not data['email'] or not data['password']:
        return make_response(('Authorize with all credentials'), 401)
    
    user = models.User.query.filter_by( email = data['email']).first()
    if not user:
        return make_response(('User does not exist'), 401)
    if check_password_hash(user.password, data['password']):
        token = jwt.encode({
                        "exp": datetime.datetime.utcnow() + datetime.timedelta(days = 0, minutes = 45),
                        "iat": datetime.datetime.utcnow(),
                        "sub": user.id}, app.config['SECRET_KEY'], algorithm = 'HS256')
        return jsonify({'token':token})
    return make_response(("Login with correct password"), 401)

@users.route('/auth/reset_password', methods = ['POST'])
@token_required
def reset_password(current_user):
    data = request.get_json()
    if not data['email'] or not data['old_password'] or not data['new_password']:
        return make_response(("Fill all credentials"),401)
    user = models.User.query.filter_by( email = data['email']).first()
    if not user:
        return make_response(("Wrong email"), 401)
    if check_password_hash(user.password, data['old_password']):
        user.password = data['new_password']
        return make_response(("Successfully changed password"), 200)
    return make_response(("Input correct old password"), 401)

@users.route('/auth/logout', methods = ['POST'])
#@swag_from('../api-docs/v2/logout_user.yml')
def logout():
    return make_response(("Successfully logged out"), 200)
