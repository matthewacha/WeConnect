import os
import random
import jwt
from flask import Flask, jsonify, request, session, make_response, abort
from werkzeug.security import generate_password_hash, check_password_hash
from app.users.views import database, Business, generate_id, token_required
from functools import wraps
from . import businesses
from json import dumps

secret_key = "its_so_secret_1945"
businesses_db = []
@businesses.route('/api/businesses', methods = ['POST'])
@token_required
def register(current_user):
    data = request.get_json()
    business = Business(data['name'],data['description'], data['location'], data['category'],user_id=current_user['user_id'])
    biz_profile = {"details":business,
                   "biz_id":generate_id(),
                   "reviews":[]}
    businesses_db.append(biz_profile)
    
    return jsonify({'message':"Successfully added business"})


@businesses.route('/api/businesses', methods = ['GET'])
@token_required
def retrieve(current_user):
    output = []
    for business in businesses_db:
        business_={
        "name":business['details'].name,
        "description":business['details'].description,
        "location":business['details'].location,
        "category":business['details'].category,
        "user_id":business['details'].user_id,
        "businessId":business['biz_id'],
        "reviews":business['reviews']}
        output.append(business_)
        

    return jsonify({"businesses":output})

"""
@businesses.route('/api/businesses/<businessId>', methods = ['GET'])
@token_required
def retrieve_business(current_user,businessId):
    business = 'business'
    return jsonify({"business":business})
businesses = [user['businesses'] for business in businesses if user['details'].email == current_user['details'].email]
@businesses.route('/api/businesses/<businessId>/reviews', methods = ['POST'])
@token_required
def post_review(current_user, businessId):
    message = "message"
    return jsonify({"message":message})

@businesses.route('/api/businesses/<businessId>', methods = ['GET'])
@token_required
def get_reviews(current_user, businessId):
    reviews = ""
    return jsonify({"reviews":reviews})
"""
