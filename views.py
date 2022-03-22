from constants.http_statscode import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from flask import Blueprint, request
from flask.json import jsonify
import validators
from flask_jwt_extended import get_jwt_identity, jwt_required
from database import *

views = Blueprint("views", __name__, url_prefix="/api/v1/views")

@views.post('/user_create')
def user_create():
    if request.method == 'POST':
        name = request.json['username']
        mobile = request.json['mobile']
        email = request.json['email']
        id=request.json['id']
        user = Users(username=name, mobile=mobile, email=email, user_id=id)
        db.session.add(user)
        db.session.commit()
        user = Users.query.filter_by(email=email).first()
        return jsonify({
            'message': "User created",
            'user': {
                'username': user.username, "email":user.email, "id":user.id
            }

        }), HTTP_201_CREATED


@views.get('/users') 
def users():  
    id=request.args.get('id')
    user1= User.query.filter_by(id=id).first()
    if user1:
        list = [{"name":user1.username, "email":user1.email, "mobile":user1.mobile, "id":user1.id, 'created_at':user1.created_at, 'upated_at': user1.updated_at}]
        users = Users.query.filter_by(user_id=id)
        for i in users:
            list.append({
                    'id': i.id,
                    "foreign_key":i.user_id,
                    'name': i.username,
                    'mobile': i.mobile,
                    'email': i.email,
                    'created_at': i.created_at,
                    'upated_at': i.updated_at
                })
        return jsonify({"data":list}),HTTP_200_OK
    return jsonify({'msg':'user does not exist'})

@views.route("/user_blog_create", methods=['POST', 'GET'])
def blogs():
    if request.method == 'POST':
        time = request.json["reading_time"]
        title=request.json["title"]
        img_link=request.json["im_link"]
        category = request.json["category"]
        description = request.json["description"]
        drname = request.json["dr_name"]
        mobile = request.json["id"]
        blog = Posts(user_id = mobile, reading_time=time,title=title, cateory=category, description=description, dr_name=drname, img_link=img_link)
        db.session.add(blog)
        db.session.commit()
        user = Posts.query.filter_by(description=description).first()
        return jsonify({
                'message': "blog created",
                'user': {
                    'id':user.id,
                    "title":user.title,
                    'dr_name': user.dr_name, 
                    "catagory":user.cateory,
                    "time":user.reading_time,
                    "description":user.description,
                    "creater_at":user.created_at

                }
            }), HTTP_201_CREATED

    choice = ["cardiology","Neeurology", "Gynaecology", "Endocrinology", "General", "Medicine", "Ayurveda"]
    return jsonify({"catagories":choice})




@views.get("/all_posts")
def all_post():
    id = request.args.get("id")
    list = []
    posts = Posts.query.filter_by(user_id=id)
    for i in posts:
        list.append({
            "id":i.id,
            "drname":i.dr_name,
            "title":i.title,
            "description":i.description,
            "img":i.img_link,
            'created_at': i.created_at,
            'upated_at': i.updated_at
        })
    return jsonify({'data':list}),HTTP_200_OK


@views.delete("delete_posts")
def delete():
    id = request.args.get("id")
    found_id = Posts.query.filter_by(id=id).first()
    db.session.delete(found_id)
    db.session.commit()
    return jsonify({
        "msg":"successfully delete"
    })

#@views.delete("delete_user")
#def delete():
 #   id = request.args.get("id")
 #   found_id = Users.query.filter_by(id=id).first()
 #   db.session.delete(found_id)
 #   db.session.commit()
 #   return jsonify({
  #      "msg":"successfully delete"
  #  })

# create user from patient side

@views.post('/patient_create')
def patient_create():
    if request.method == 'POST':
        name = request.json['username']
        mobile = request.json['mobile']
        email = request.json['email']
        id=request.json['id']
        user = Patientsusers(username=name, mobile=mobile, email=email, user_id=id)
        db.session.add(user)
        db.session.commit()
        user = Patientsusers.query.filter_by(email=email).first()
        return jsonify({
            'message': "User created",
            'user': {
                'username': user.username, "email":user.email, "id":user.id
            }

        }), HTTP_201_CREATED


# show all users from patients side

@views.get('/patients') 
def patients():  
    id=request.args.get('id')
    user1= Patients.query.filter_by(id=id).first()
    if user1:
        list = [{"name":user1.username, "email":user1.email, "mobile":user1.mobile, "id":user1.id, 'created_at':user1.created_at, 'upated_at': user1.updated_at}]
        users = Patientsusers.query.filter_by(user_id=id)
        for i in users:
            list.append({
                    'id': i.id,
                    "foreign_key":i.user_id,
                    'name': i.username,
                    'mobile': i.mobile,
                    'email': i.email,
                    'created_at': i.created_at,
                    'upated_at': i.updated_at
                })
        return jsonify({"data":list}),HTTP_200_OK

    return jsonify({'msg':'user does not exist'})
# show all blog to patients

@views.get('/blogs')
def all_blogs():
    blogs = Posts.query.all()
    list = []
    for i in blogs:
        list.append({
            "id":i.id,
            "drname":i.dr_name,
            "title":i.title,
            "description":i.description,
            "img":i.img_link,
            'created_at': i.created_at,
            'upated_at': i.updated_at
        })
    return jsonify({'data':list}),HTTP_200_OK


# get all doctor contact details for consultant

@views.get('/contact')
def doctoer():
    doctors = User.query.all()
    list =[]
    for doctor in doctors:
        list.append({
            "name":doctor.username,
            "mobile":doctor.mobile,
            "email":doctor.email
        })
    return jsonify({"contacts":list})


# for the collection of pdf files 

@views.route('/collection', methods=['POST', 'GET'])
def collection():
    if request.method=='POST':
        title = request.json['title']
        link_list = request.json['l_list']
        id = request.json['id'] #take id from Patient_user table so that we can create multiple collection for patients
        for i in link_list:
            path= i['path']
            pdf_name= i['name']
            link = i['link']
            user = Extracter(user_id=id, col_name=title, url=link, pdfname=pdf_name, path= path)
            db.session.add(user)
            db.session.commit()
        user = Extracter.query.filter_by(user_id=id,col_name=title)
        list = []
        for i in user:
            list.append({
                "title":i.col_name,
                "id":i.id,
                "link":i.url,
                "created_at":i.created_at,
                "collection_id":i.id
                    
            })
        return jsonify({"data":list})
    id = request.args.get('id', type = int) #user id who make collection
    title = request.args.get('title', type = str) # collection name
    data = Extracter.query.filter_by(user_id=id, col_name=title)
    l = []
    for i in data:
        l.append({
            "date":i.created_at,
            "name": i.pdfname,
            "url":i.url,
            "collection_name":i.col_name,
            "collection_id":i.id
        })
    return jsonify({"data":l})






# see all content inside users table
@views.get('/tableusers')
def table():
    users = Users.query.all()
    list = []
    for i in users:
        list.append({
            'id': i.id,
            "foreign_key":i.user_id,
            'name': i.username,
            'mobile': i.mobile,
            'email': i.email,
            'created_at': i.created_at,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
            'upated_at': i.updated_at
        })
    return jsonify({"data":list}),HTTP_200_OK