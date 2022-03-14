import email
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
#@swag_from('./docs/auth/register.yaml')
def register():
    username = request.json['username']
    mobile = request.json['mobile']
    password = request.json['password']
    role = request.json['role']

    if len(password) <= 6:
        return jsonify({'error': "Password is too short"}), HTTP_400_BAD_REQUEST

    if len(username) < 3:
        return jsonify({'error': "User is too short"}), HTTP_400_BAD_REQUEST

    if User.query.filter_by(mobile=mobile).first() is not None:
        return jsonify({'error': "Mobile Number is taken"}), HTTP_409_CONFLICT
    

    pwd_hash = generate_password_hash(password)

    user = User(username=username, mobile=mobile, role=role, password=pwd_hash)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': "User created",
        'user': {
            'username': username, "mobile": mobile
        }

    }), HTTP_201_CREATED

@auth.post('/register_google')
def register_goole():
    email = request.json['email']
    name = request.json['username']
    role = request.json['role']
    user = User.query.filter_by(email=email).first()

    if user:
        
        refresh = create_refresh_token(identity=user.id)
        access = create_access_token(identity=user.id)

        return jsonify({
            'user': {
                'refresh': refresh,
                'access': access,
                'username': user.username,
                'mobile': user.email
            }
        }), HTTP_200_OK
        
    user = User(username=name, role=role, email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': "User created",
        'user': {
            'username': name, "email":email
        }

    }), HTTP_201_CREATED


@auth.post('/login')
#swag_from('./docs/auth/login.yaml')
def login():
    mobile = request.json.get('mobile', '')
    #password = request.json.get('password', '')

    user = User.query.filter_by(mobile=mobile).first()

    if user:
        
        refresh = create_refresh_token(identity=user.id)
        access = create_access_token(identity=user.id)

        return jsonify({
            'user': {
                'refresh': refresh,
                'access': access,
                'username': user.username,
                'mobile': user.mobile
            }
        }), HTTP_200_OK

    return jsonify({'error': 'Wrong credentials'}), HTTP_401_UNAUTHORIZED


@auth.post('/login_email')
#swag_from('./docs/auth/login.yaml')
def login_email():
    email = request.json.get('email', '')
    #password = request.json.get('password', '')

    user = User.query.filter_by(email=email).first()

    if user:
        
        refresh = create_refresh_token(identity=user.id)
        access = create_access_token(identity=user.id)

        return jsonify({
            'user': {
                'refresh': refresh,
                'access': access,
                'username': user.username,
                'email': user.email
            }
        }), HTTP_200_OK

    return jsonify({'error': 'Wrong credentials'}), HTTP_401_UNAUTHORIZED

@auth.get("/users")
@jwt_required()
def users():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        'username': user.username,
        'email': user.email
    }), HTTP_200_OK


@auth.get('/token/refresh')
@jwt_required(refresh=True)
def refresh_users_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({
        'access': access
    }), HTTP_200_OK