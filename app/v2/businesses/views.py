import os
import random
import jwt
from flask import Flask, jsonify,request, session, make_response, abort
from werkzeug.security import generate_password_hash, check_password_hash
from app.v2 import models
from app import db
#from app.v2.users.views import token_required
from . import businessesv2

@businessesv2.route('/businesses', methods = ['POST'])
def register():
    data = request.get_json()
    business = models.Business(name=data['name'],
                               description=data['description'],
                               location=data['location'],
                               category=data['category'])
    try:
        db.session.add(business)
        db.session.commit()
        message="Successfully added business"
    except:
        return make_response(("Business already exists"), 401)
    db.session.close()
    return jsonify({"message":message})

@businessesv2.route('/businesses', methods = ['GET'])
def view_businesses():
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
def view_business(id):
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
        
