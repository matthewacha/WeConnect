import os
import random
import jwt
import datetime
from flask import Flask, jsonify, request, session, make_response, abort
from flasgger import swag_from
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from . import usersv1
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
                self.password = new_password
               
        def email(self):
                return self.email
        
        def password(self):
                return self.password

class Business(object):
        def __init__(self, name,description, location, category, user_id):
                self.name = name
                self.description = description
                self.location = location
                self.category = category
                self.user_id = user_id

        def change_name(self,new_name):
                self.name = new_name
                
        def change_location(self,new_location):
                self.location = location
                
        def change_category(self,new_category):
                self.category = new_category

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
                user =[user for user in database if user['user_id'] == data["sub"]]
                current_user = user[0]
            except:
                return jsonify({"message":"Token is invalid"}), 401
            return funct(current_user, *args, **kwargs)
    return decorated_funct
    
@usersv1.route('/auth/register', methods = ['POST'])
@swag_from('v1/api-docs/register_user.yml')
def add_user():
    json_data = request.get_json()

    user = User(json_data['email'], generate_password_hash(json_data['password']))
    user_profile = {'details':user,
                    'user_id':generate_id(),
                    'businesses':[]}
    user = [user for user in database if user['details'].email == json_data['email']]
    if len(user) > 0:
        database.append(user_profile)
        message = 'Successfully signed up'
    else:
        message = 'User already exists'
    return jsonify({"message":message})
    

@usersv1.route('/auth/login', methods = ['POST'])
@swag_from('v1/api-docs/login_user.yml')
def login():
        auth = request.get_json()
        if not auth or not auth['email'] or not auth['password']:
                return make_response(("Authorize with email and password"), 401)

        user = [user for user in database if user['details'].email == auth['email']]
        if len(user) == 0 :
                return make_response(("Authorize with correct credentials"), 401)
        info = user[0]
        if check_password_hash(info['details'].password, auth['password']):
                token = jwt.encode({
                        "exp": datetime.datetime.utcnow() + datetime.timedelta(days = 0, minutes = 45),
                        "iat": datetime.datetime.utcnow(),
                        "sub": info['user_id']}, secret_key, algorithm = 'HS256')
                return jsonify({'token':token})
        return make_response(("Authorize with correct password"), 401)

@usersv1.route('/auth/reset-password', methods = ['POST'])
@swag_from('v1/api-docs/reset_password.yml')
@token_required
def reset_password(current_user):
        cred = request.get_json()
        if not cred or not cred['email'] or not cred['old_password'] or not cred['new_password']:
                return make_response(("Please input passwords"), 401)
        if cred['email'] == current_user['details'].email:
                current_user['details'].change_password(generate_password_hash(cred['new_password']))
                return make_response(("Successfully changed password"), 200)


@usersv1.route('/auth/logout', methods = ['POST'])
@swag_from('v1/api-docs/logout_user.yml')
@token_required
def logout(current_user):
        if 'access_token' in request.headers:
            token = request.headers['access_token']
            token = None
            return jsonify({'message':"Successfully logged out"})
        return make_response(("Token required"), 499)
