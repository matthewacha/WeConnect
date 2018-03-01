import os
import random
import jwt
from flask import Flask, jsonify, request, session, make_response, abort
from flasgger.utils import swag_from
from werkzeug.security import generate_password_hash, check_password_hash
from app.v1.models import database, Business, generate_bizId, generate_id
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
    for business in businesses_db:
        if data['name']==business['details'].name:
            return make_response(('Business already exists, try another'),401)
    business = Business(data['name'],data['description'], data['location'], data['category'],current_user['user_id'])
    biz_profile = {"details":business,
                   "biz_id":generate_bizId(businesses_db),
                   "reviews":[]}
    businesses_db.append(biz_profile)
    
    return jsonify({'message':"Successfully added business"})


@businessesv1.route('/businesses/<businessId>', methods = ['GET'])
@swag_from('../api-docs/v1/view_business.yml')
@token_required
def retrieve_business(current_user, businessId):
    Idlist = map(int, businessId.split())
    businessId = Idlist[0]
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
        if business["businessId"] == businessId:
            business_out.append(business)

    if len(business_out) == 0:
        message = ["Business does not exist"]
    else:
        message = business_out
    return jsonify({"business":message})

@businessesv1.route('/businesses', methods = ['GET'])
@swag_from('../api-docs/v1/view_businesses.yml')
@token_required
def retrieve_businesses(current_user):
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

@businessesv1.route('/businesses/<businessId>', methods = ['PUT'])
@swag_from('../api-docs/v1/update_business.yml')
@token_required
def edit_business(current_user, businessId):
    Idlist = map(int, businessId.split())
    businessId = Idlist[0]
    data = request.get_json()
    for business in businesses_db:
        if business['details'].user_id == current_user['user_id']:
            if business['biz_id'] == businessId:
                if data['new_name']:
                    business['details'].name = data['new_name']
                if data['new_description']:
                    business['details'].description = data['new_description']
                if data['new_location']:
                    business['details'].category = data['new_category']
                    message = "Successfully edited"
            else:
                return make_response(("Business does not exists"), 401)
        else:
            return make_response(("Authoriation required"),401)
                
    return jsonify({"message":message })

@businessesv1.route('/businesses/<businessId>', methods = ['DELETE'])
@swag_from('../api-docs/v1/delete_business.yml')
@token_required
def delete_business(current_user, businessId):
    Idlist = map(int, businessId.split())
    businessId = Idlist[0]
    for business in businesses_db:
        if business['details'].user_id == current_user['user_id']:
            if business["biz_id"] == businessId:
                businesses_db.remove(business)
                message = "Successfully deleted"
            else:
                return jsonify({"message":[businessId,business["biz_id"]]})
                #message = "Business does not exist"
        else:
            return make_response(("You are not authorized"), 401)
    return jsonify({"message":message})

@businessesv1.route('/businesses/<businessId>/reviews', methods = ['POST'])
@swag_from('../api-docs/v1/post_review.yml')
@token_required
def post_review(current_user, businessId):
    Idlist = map(int, businessId.split())
    businessId = Idlist[0]
    data = request.get_json()
    review = data['review']
    for business in businesses_db:
        if business["biz_id"] == businessId:
            business['reviews'].append(review)
            message = "Successfully added review"
    return jsonify({"message":message})


@businessesv1.route('/businesses/<businessId>/reviews', methods = ['GET'])
@swag_from('../api-docs/v1/view_reviews.yml')
@token_required
def view_reviews(current_user, businessId):
    Idlist = map(int, businessId.split())
    businessId = Idlist[0]
    all_reviews = []
    for business in businesses_db:
        if business["biz_id"] == businessId:
            all_reviews = business['reviews']
    if len(all_reviews)==0:
        message="No reviews"
    else:
        message= all_reviews

    return jsonify({'reviews':message})
