import os
import random
import jwt
from flask import Flask, jsonify,request, session, make_response, abort
from flasgger.utils import swag_from
from werkzeug.security import generate_password_hash, check_password_hash
from app.v2 import models
from app import db
from app.v2.users.views import token_required
from . import businessesv2

@businessesv2.route('/businesses', methods = ['POST'])
#@swag_from('../api-docs/v2/register_business.yml')
@token_required
def register_business(current_user):
    data = request.get_json()
    business = models.Business(name=data['name'],
                               description=data['description'],
                               location=data['location'],
                               category=data['category'],
                               user_id=current_user.id
                               )
    try:
        db.session.add(business)
        db.session.commit()
        message="Successfully added business"
    except:
        return make_response(("Business already exists"), 401)
    db.session.close()
    return jsonify({"message":message})

@businessesv2.route('/businesses', methods = ['GET'])
#@swag_from('../api-docs/v1/view_businesses.yml')
@token_required
def view_businesses(current_user):
    businesses = models.Business.query.all()
    all_businesses=[]
    for business in businesses:
        output={}
        output['name'] = business.name
        output['description'] = business.description
        output['location'] = business.location
        output['category'] = business.category
        all_businesses.append(output)
    return jsonify({"businesses":all_businesses})

@businessesv2.route('/businesses/<id>', methods = ['GET'])
#@swag_from('../api-docs/v1/view_business.yml')
@token_required
def view_business(current_user, id):
    business = models.Business.query.filter_by(id=id).first()
    business_ = []
    if business:
        output = {}
        output['name'] = business.name
        output['description'] = business.description
        output['location'] = business.location
        output['category'] = business.category
        return jsonify({"business":output})
    return make_response(("Business does not exist"), 401)


@businessesv2.route('/businesses/<id>', methods=['PUT'])
@token_required
def update_business(current_user, id):
    data = request.get_json()
    business = models.Business.query.filter_by(id=id).first()
    if business:
        business.name = data['new_name']
        business.description=data['new_description']
        business.location = data['new_location']
        business.category = data['new_category']
        return jsonify({"mesage":"Successfully updated"})
    return make_response(("Business does not exist"), 401)

@businessesv2.route('/businesses/<id>', methods = ['DELETE'])
@token_required
def delete_business(current_user, id):
    business = models.Business.query.filter_by(id=id).first()
    if business:
        db.session.delete(business)
        db.session.commit()
        return jsonify({"message":"Successfully deleted"})
    return make_response(("Business does not exist"),401)

@businessesv2.route('/businesses/<id>/reviews', methods=['POST'])
@token_required
def add_review(current_user, id):
    data=request.get_json()
    business = models.Business.query.filter_by(id=id).first()
    if business:
        try:
            review = models.Review(description=data['description'],businessId=id)
            db.session.add(review)
            db.session.commit()
            message = "Successfully added"
        except:
            return make_response(("Exited with error"), 401)
    else:
        return make_response(("Business does not exist"), 401)
    return jsonify({"messgae":message})

@businessesv2.route('/businesses/<id>/reviews', methods=['GET'])
#@token_required
def view_reviews(id):
    data=request.get_json()
    business = models.Business.query.filter_by(id=id).first()
    if business:
        try:
            #message = "yeahh"
            all_reviews= models.Review.query.filter_by(businessId=id)
            reviews =[]
            for review in all_reviews:
                output = {}
                output['review']=review['description']
                reviews.append(output)
            return jsonify({"Reviews":reviews})
        except:
            return jsonify({"error": " required"}), 401
    return make_response(("Business does not exist"),401)

