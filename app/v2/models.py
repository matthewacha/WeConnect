from sqlalchemy import Column, ForeignKey, Integer, String#pragma:no cover
from sqlalchemy import create_engine#pragma:no cover
from sqlalchemy.orm import relationship#pragma:no cover
from app import db#pragma:no cover


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True)
    password = db.Column(db.String(300))
    businesses = db.relationship('Business', backref='user',
                                 lazy='dynamic')
    def __init__(self, email, password):
        self.email = email#pragma:no cover
        self.password = password#pragma:no cover
        db.create_all()   #pragma:no cover
    
class Business(db.Model):
    __tablename__ = 'businesses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    description = db.Column(db.String(1000), nullable=False)
    location = db.Column(db.String(200))
    category = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    reviews = db.relationship('Review', backref='business',
                                 lazy='dynamic')
    def __init__(self, name, description, location, category, user_id):
        self.name = name#pragma:no cover
        self.description = description#pragma:no cover
        self.location = location
        self.category = category
        self.user_id = user_id
        db.create_all()#pragma:no cover

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1000), nullable=False)
    businessId = db.Column(db.Integer, db.ForeignKey('businesses.id'))
    def __init__(self, description, businessId):
        self.description = description#pragma:no cover
        self.businessId = businessId
        db.create_all()#pragma:no cover
