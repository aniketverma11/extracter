import json
from unicodedata import category
from constants.http_statscode import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from flask import Blueprint, request
from flask.json import jsonify
import validators
from flask_jwt_extended import get_jwt_identity, jwt_required
from database import *

views = Blueprint("views", __name__, url_prefix="/api/v1/views")

@views.route('/user_create')
def user_create():
    if request.method == 'POST':
        name = request.json['username']
        mobile = request.json['mobile']
        email = request.json['email']
        id=request.json['id']
        user = Users(username=name, mobile=mobile, email=email, user_id=id)
        db.session.add(user)
        db.session.commit()
        return jsonify({
            'message': "User created",
            'user': {
                'username': name, "email":email
            }

        }), HTTP_201_CREATED


@views.get('/users') 
def users():  
    id=request.args.get('id')
    list = []
    users = Users.query.filter_by(user_id=id)
    for i in users:
        list.append({
                'id': i.id,
                "foreign_key":i.user_id,
                'name': i.username,
                'mobile': i.mobile,
                'email': i.email,
                'created_at': i.created_at,
                'upated_at': i.updated_at,
            })
    return jsonify({"data":list}),HTTP_200_OK


@views.post("/user_blog_create")
def blogs():
    if request.method == 'POST':
        time = request.json["reading_time"]
        category = request.json["category"]
        description = request.json["description"]
        drname = request.json["dr_name"]
        mobile = request.json["id"]
        blog = Posts(user_id = mobile, reading_time=time, cateory=category, description=description, dr_name=drname)
        db.session.add(blog)
        db.session.commit()
        return jsonify({
                'message': "User created",
                'user': {
                    'dr_name': drname, "catagory":category
                }
            }), HTTP_201_CREATED

@views.get("/all_posts")
def all_post():
    id = request.args.get("id")
    posts = Posts.query.filter_by(user_id=id)
    list = []
    for i in posts:
        list.append({
            "id":i.id,
            "drname":i.dr_name,
            "description":i.description,
            'created_at': i.created_at,
            'upated_at': i.updated_at
        })
    return jsonify({'data':list}),HTTP_200_OK



@views.route('/', methods=['POST', 'GET'])
@jwt_required()
def handle_pdf():
    current_user = get_jwt_identity() 
    if request.method == 'POST':

        body = request.get_json().get('body', '')
        url = request.get_json().get('url', '')

        if not validators.url(url):
            return jsonify({
                'error': 'Enter a valid url'
            }), HTTP_400_BAD_REQUEST

        if PDF_Extracter.query.filter_by(url=url).first():
            return jsonify({
                'error': 'URL already exists'
            }), HTTP_409_CONFLICT

        pdf = PDF_Extracter(url=url, body=body, user_id=current_user)
        db.session.add(pdf)
        db.session.commit()

        return jsonify({
            'id': pdf.id,
            'url': pdf.url,
            'short_url': pdf.short_url,
            'visit': pdf.visits,
            'body': pdf.body,
            'created_at': pdf.created_at,
            'updated_at': pdf.updated_at,
        }), HTTP_201_CREATED

    else:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        pdf = PDF_Extracter.query.filter_by(
            user_id=current_user).paginate(page=page, per_page=per_page)

        data = []

        for pd in pdf.items:
            data.append({
                'id': pd.id,
                'url': pd.url,
                'short_url': pd.short_url,
                'visit': pd.visits,
                'body': pd.body,
                'created_at': pd.created_at,
                'updated_at': pd.updated_at,
            })

        meta = {
            "page": pdf.page,
            'pages': pdf.pages,
            'total_count': pdf.total,
            'prev_page': pdf.prev_num,
            'next_page': pdf.next_num,
            'has_next': pdf.has_next,
            'has_prev': pdf.has_prev,

        }

        return jsonify({'data': data, "meta": meta}), HTTP_200_OK
