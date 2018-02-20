import os
import random
import jwt
import datetime
from flask import Flask, jsonify, request, session, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from . import users
from app import app
from json import dumps

secret_key = "its_so_secret_1945"
database = []

###helper methods###
def generate_id():
        id = random.uniform(5,500000)
        id *= 100000
        id = int(id)
        return id

def token_required(funct):
    @wraps(funct)
    def decorated_funct(*args, **kwargs):
        token = None
        if 'access_token' in request.headers:
            token = request.headers['access_token']
            if not token:
                return jsonify({"message":"Token is missing"}), 401#pragma:no cover
            try:
                data = jwt.decode(token, secret_key)
            except:
                return jsonify({"message":"Token is invalid"}), 401
            return funct(current_user, *args, **kwargs)
    return decorated_funct
    
@users.route('/api/auth/register', methods = ['POST'])
def add_user():
    json_data = request.get_json()
    user_profile = {'email': json_data['email'],
                    'password':generate_password_hash(json_data['password']),
                    'id':generate_id(),                
                    'businesses':[]}
    database.append(user_profile)
    message = 'Successfully signed up'

    return jsonify({"message":message})
    

@users.route('/api/auth/login', methods = ['POST'])
def login():
    auth = request.get_json()

    if not auth or not auth['email'] or not auth['password']:
        return make_response(("Authorize with email and password"), 401)
    
    for user in database:
        if user['email'] == auth['email']:
            user = user

        #user = user
        
    if check_password_hash(user['password'], auth['password']):
        token = jwt.encode({
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days = 0, minutes = 45),
            "iat": datetime.datetime.utcnow(),
            "sub": user['id']}, secret_key, algorithm = 'HS256')
        return jsonify({'token':token})
    return make_response(("Authorize with correct password"), 401)
