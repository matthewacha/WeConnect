import os
import random
import jwt
from flask import Flask, jsonify, request, session, make_response, abort
from flasgger.utils import swag_from
from werkzeug.security import generate_password_hash, check_password_hash
from app.v1.models import database, Business, generate_id
from app.v1.users.views import token_required
from functools import wraps
from . import businessesv1
from json import dumps

secret_key = "its_so_secret_1945"
businesses_db = []

@businessesv1.route('/businesses', methods = ['POST'])
@swag_from('../api-docs/v1/register_business.yml')
@token_required
def register(current_user):
    data = request.get_json()
    business = Business(data['name'],data['description'], data['location'], data['category'],user_id=current_user['user_id'])
    biz_profile = {"details":business,
                   "biz_id":generate_id(),
                   "reviews":[]}
    businesses_db.append(biz_profile)
    
    return jsonify({'message':"Successfully added business"})



@businessesv1.route('/businesses/<name>', methods = ['GET'])
@swag_from('../api-docs/v1/view_business.yml')
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

@businessesv1.route('/businesses', methods = ['GET'])
@swag_from('../api-docs/v1/view_businesses.yml')
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
    if len(output) == 0:
        message = "No businesses exist"
    else:
        message = output
        

    return jsonify({"businesses":message})

@businessesv1.route('/businesses/<name>', methods = ['PUT'])
@swag_from('../api-docs/v1/update_business.yml')
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

@businessesv1.route('/businesses/<name>', methods = ['DELETE'])
@swag_from('../api-docs/v1/delete_business.yml')
@token_required
def delete_business(current_user, name):
    for business in businesses_db:
        if business['details'].user_id == current_user['user_id']:
            if business["details"].name == name:
                businesses_db.remove(business)
                message = "Successfully deleted"
            else:
                message = "Business does not exist"
        else:
            message = "You are not authorized"
    return jsonify({"message":message})

@businessesv1.route('/businesses/<name>/reviews', methods = ['POST'])
@swag_from('../api-docs/v1/post_review.yml')
@token_required
def post_review(current_user, name):
    data = request.get_json()
    review = data['review']
    for business in businesses_db:
        if business["details"].name == name:
            business['reviews'].append(review)
            message = "Successfully added review"
    return jsonify({"message":message})


@businessesv1.route('/businesses/<name>/reviews', methods = ['GET'])
@swag_from('../api-docs/v1/view_reviews.yml')
@token_required
def view_reviews(current_user, name):
    all_reviews = []
    for business in businesses_db:
        if business['details'].name == name:
            all_reviews = business['reviews']
    if len(all_reviews)==0:
        message="No reviews"
    else:
        message= all_reviews

    return jsonify({'reviews':message})
