import os
import random
import jwt
import datetime
from flask import Flask, jsonify, request, session, make_response, abort
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

class User(object):
        def __init__(self, email, password):
                self.email = email
                self.password = password

        def change_password(self, new_password):
                password = self.new_password
                return password
        def email(self):
                return self.email
        def password(self):
                return self.password

class Business(object):
        def __init__(self, name, location, category):
                self.name = name
                self.location = location
                self.category = category

        def change_name(self,new_name):
                name = self.new_name
                return name
        def change_location(self,new_location):
                location = self.location
                return location
        def change_category(self,new_category):
                category = self.new_category

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
                user_profiles = []
                for user in database:
                        user_profiles.append({'email':user['details'].email,
                                  'password':user['details'].password,
                                  'user_id':user['id'],
                                  'businesses':user['businesses']})
                for user in user_profiles:
                        if user['user_id'] == data['sub']:
                                current_user = user
            except:
                return jsonify({"message":"Token is invalid"}), 401
            return funct(current_user, *args, **kwargs)
    return decorated_funct
    
@users.route('/api/auth/register', methods = ['POST'])
def add_user():
    json_data = request.get_json()

    user = User(json_data['email'], generate_password_hash(json_data['password']))
    user_profile = {'details':user,
                    'user_id':generate_id(),
                    'businesses':[]}
    database.append(user_profile)
    message = 'Successfully signed up'

    return jsonify({"message":message})
    

@users.route('/api/auth/login', methods = ['POST'])
def login():
        auth = request.get_json()
        if not auth or not auth['email'] or not auth['password']:
                return make_response(("Authorize with email and password"), 401)

        user_profiles = []
        for user in database:
                user_profiles.append({'email':user['details'].email,
                                  'password':user['details'].password,
                                  'user_id':user['user_id'],
                                  'businesses':user['businesses']})

        user = [user for user in user_profiles if user['email'] == auth['email']]
        if len(user) == 0 :
                return make_response(("Authorize with correct credentials"), 401)
        info = user[0]
        if check_password_hash(info['password'], auth['password']):
                token = jwt.encode({
                        "exp": datetime.datetime.utcnow() + datetime.timedelta(days = 0, minutes = 45),
                        "iat": datetime.datetime.utcnow(),
                        "sub": info['user_id']}, secret_key, algorithm = 'HS256')
                return jsonify({'token':token})
        return make_response(("Authorize with correct password"), 401)

@users.route('/api/auth/logout', methods = ['POST'])
def logout():
        if 'access_token' in request.headers:
            token = request.headers['access_token']
            token = None
        
        return make_response(("Successfully logged out"), 200)
