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



@businesses.route('/api/businesses/<name>', methods = ['GET'])
def retrieve_business(name):
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

    business_out = []

    for business in output:
        if business["name"] == name:
            business_out.append(business)

    if len(business_out) == 0:
        message = ["Business does not exist"]
    else:
        message = business_out
    return jsonify({"business":message[0]})

@businesses.route('/api/businesses', methods = ['GET'])
def retrieve_businesses():
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

@businesses.route('/api/businesses/<name>', methods = ['PUT'])
@token_required
def edit_business(current_user, name):
    data = request.get_json()
    
    for business in businesses_db:
        if business['details'].user_id == current_user['user_id']:
            if business['details'].name == name:
                if data['new_name']:
                    business['details'].name = data['new_name']
                if data['new_description']:
                    business['details'].description = data['new_description']
                if data['new_location']:
                    business['details'].category = data['new_category']
                    message = "Successfully edited"
            else:
                message = "Business does not exist"
        else:
            message = "You do not have authorization"
                
    return jsonify({"message":message })

@businesses.route('/api/businesses/<name>', methods = ['DELETE'])
@token_required
def delete_business(current_user, name):
    for business in businesses_db:
        if business['details'].user_id == current_user['user_id'] and business["details"].name == name:
            businesses_db.remove(business)
            message = "Successfully deleted"
        else:
            message = "You are not authorized"
    return jsonify({"message":message})

@businesses.route('/api/businesses/<name>/reviews', methods = ['POST'])
@token_required
def post_review(current_user, name):
    data = request.get_json()
    review = data['review']
    for business in businesses_db:
        if business["details"].name == name:
            business['reviews'].append(review)
            message = "Successfully added review"
    return jsonify({"message":message})


@businesses.route('/api/businesses/<name>/reviews', methods = ['GET'])
@token_required
def view_reviews(current_user, name):
    all_reviews = []
    for business in businesses_db:
        if business['details'].name == name:
            all_reviews = business['reviews']

    return jsonify({'reviews':all_reviews})
