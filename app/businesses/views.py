import os
import random
from flask import Flask, jsonify, request, session, make_response, abort
from werkzeug.security import generate_password_hash, check_password_hash
from app.users.views import database, Business, generate_id, token_required
from . import businesses
from json import dumps

business_data = []

@businesses.route('/api/businesses', methods = ['POST'])
def register():
    data = request.get_json()
    business = Business(data['name'],data['description'], data['location'], data['category'])
    biz_profile = {"details":business,
                   "biz_id":generate_id,
                   "reviews":[]}
    business_data.append(biz_profile)
    message = "Successfully added business"

    return jsonify({"message":message})
