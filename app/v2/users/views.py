import os#pragma:no cover
import jwt#pragma:no cover
import datetime#pragma:no cover
from flask import Flask, jsonify, request, session, make_response#pragma:no cover
from werkzeug.security import generate_password_hash, check_password_hash#pragma:no cover
from functools import wraps#pragma:no cover
from . import users#pragma:no cover
from app import app, db, models#pragma:no cover
from json import dumps#pragma:no cover

@users.route('/api/v2/auth/register', methods = ['POST'])
def add_new_user():
    json_data = request.get_json()
    user = models.User(email = json_data['email'],
                       password = generate_password_hash(json_data['password']))
    
    try:
        db.session.add(user)
        db.session.commit()
        message = 'Successfully signed up'
    except:
        message = 'User already taken'
    db.session.close()
    return jsonify({'message':message})

