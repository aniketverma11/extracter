from flask import Blueprint, app, request, jsonify, Flask, json
#from flask_restful import Resource, Api, request
from werkzeug.security import check_password_hash, generate_password_hash
#import validators
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
#from flasgger import swag_from
from constants.http_statscode import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT
from database import *

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

@auth.post('/register')
def register():
    username = request.json['username']
    mobile = request.json['mobile']
    email = request.json["email"]
    password = request.json['password']
    role = request.json['role']


    if role=="doctor":
        if len(password) <= 6:
            return jsonify({'error': "Password is too short"}), HTTP_400_BAD_REQUEST

        if len(username) < 3:
            return jsonify({'error': "User is too short"}), HTTP_400_BAD_REQUEST

        if User.query.filter_by(mobile=mobile).first() is not None:
            return jsonify({'error': "Mobile Number is taken"}), HTTP_409_CONFLICT
        
        if User.query.filter_by(email=email).first() is not None:
            return jsonify({'error': "Mobile Number is taken"}), HTTP_409_CONFLICT
        

        pwd_hash = generate_password_hash(password)

        user = User(username=username, mobile=mobile, role=role, password=pwd_hash, email=email)
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(mobile=mobile).first()
        return jsonify({
            'message': "Patient created",
            'user': {
                'username': user.username, "mobile": user.mobile, "id":user.id, "role":user.role
            }

        }), HTTP_201_CREATED
    
    elif role=="patient":
        if len(password) <= 6:
            return jsonify({'error': "Password is too short"}), HTTP_400_BAD_REQUEST

        if len(username) < 3:
            return jsonify({'error': "User is too short"}), HTTP_400_BAD_REQUEST

        if Patients.query.filter_by(mobile=mobile).first() is not None:
            return jsonify({'error': "Mobile Number is taken"}), HTTP_409_CONFLICT
        
        if Patients.query.filter_by(email=email).first() is not None:
            return jsonify({'error': "Mobile Number is taken"}), HTTP_409_CONFLICT

        pwd_hash = generate_password_hash(password)

        user = Patients(username=username, mobile=mobile, email=email, role=role, password=pwd_hash)
        db.session.add(user)
        db.session.commit()
        user = Patients.query.filter_by(mobile=mobile).first()
        return jsonify({
            'message': "Patient created",
            'user': {
                'username': user.username, "mobile": user.mobile, "id":user.id, "role":user.role
            }

        }), HTTP_201_CREATED
    
    return jsonify({'error': 'Wrong credentials'}), HTTP_401_UNAUTHORIZED

@auth.post('/register_google')
def register_goole():
    email = request.json["email"]
    user = User.query.filter_by(email=email).first()
    user2 = Patients.query.filter_by(email=email).first()
    if user:
        
        refresh = create_refresh_token(identity=user.id)
        access = create_access_token(identity=user.id)

        return jsonify({
            'user': {
                'refresh': refresh,
                'access': access,
                'username': user.username,
                'mobile': user.email,
                'id':user.id
            }
        }), HTTP_200_OK
    
    elif user2:
        
        refresh = create_refresh_token(identity=user2.id)
        access = create_access_token(identity=user2.id)

        return jsonify({
            'user': {
                'refresh': refresh,
                'access': access,
                'username': user2.username,
                'mobile': user2.mobile,
                'id':user2.id,
                'role':user2.role
            }
        }), HTTP_200_OK
    return jsonify({'error': 'Wrong credentials'}), HTTP_401_UNAUTHORIZED

@auth.post('/login')
def login():
    mobile = request.json.get('mobile', '')

    user = User.query.filter_by(mobile=mobile).first()
    user2 = Patients.query.filter_by(mobile=mobile).first()
    if user:
        
        refresh = create_refresh_token(identity=user.id)
        access = create_access_token(identity=user.id)

        return jsonify({
            'user': {
                'refresh': refresh,
                'access': access,
                'username': user.username,
                'mobile': user.mobile,
                'id':user.id,
                'role':user.role
            }
        }), HTTP_200_OK
    
    elif user2:
        
        refresh = create_refresh_token(identity=user2.id)
        access = create_access_token(identity=user2.id)

        return jsonify({
            'user': {
                'refresh': refresh,
                'access': access,
                'username': user2.username,
                'mobile': user2.mobile,
                'id':user2.id,
                'role':user2.role
            }
        }), HTTP_200_OK

    return jsonify({'error': 'Wrong credentials'}), HTTP_401_UNAUTHORIZED


@auth.post('/login_email')
def login_email():
    email = request.json.get('email', '')
    user = User.query.filter_by(email=email).first()

    if user:
        
        refresh = create_refresh_token(identity=user.id)
        access = create_access_token(identity=user.id)

        return jsonify({
            'user': {
                'refresh': refresh,
                'access': access,
                'username': user.username,
                'email': user.email,
                'id':user.id
            }
        }), HTTP_200_OK

    return jsonify({'error': 'Wrong credentials'}), HTTP_401_UNAUTHORIZED
