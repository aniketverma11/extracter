from constants.http_statscode import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR
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
        link = request.json['img_link']
        mobile = request.json['mobile']
        email = request.json['email']
        id=request.json['id']
        user = Users(username=name,img_link=link,mobile=mobile, email=email, user_id=id)
        db.session.add(user)
        db.session.commit()
        user = Users.query.filter_by(email=email).first()
        return jsonify({
            'message': "User created",
            'user': {
                'username': user.username, "email":user.email, "id":user.id, "img":user.img_link
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
                    'img':i.img_link,
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
        user = Posts.query.filter_by(description=description,title=title).first()
        return jsonify({
                'message': "blog created",
                'user': {
                    'id':user.id,
                    "title":user.title,
                    'dr_name': user.dr_name,
                    "time":user.reading_time,
                    "description":user.description,
                    "creater_at":user.created_at

                }
            }), HTTP_201_CREATED

    choice = ["Cardiology","Neurology", "Gynaecology", "Endocrinology", "General", "Medicine", "Ayurveda"]
    return jsonify({"catagories":choice})




@views.get("/all_posts")
def all_post():
    id = request.args.get("id")
    list = []
    posts = Posts.query.filter_by(user_id=id)
    for i in posts:
        list.append({
            "catagory":i.cateory,
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
    if found_id:
        db.session.delete(found_id)
        db.session.commit()
        return jsonify({
            "msg":"successfully delete"
        })
    return jsonify({
            "msg":"user does not exist"
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
        link = request.json['img_link']
        mobile = request.json['mobile']
        email = request.json['email']
        id=request.json['id']
        user = Patientsusers(username=name, img_link=link, mobile=mobile, email=email, user_id=id)
        db.session.add(user)
        db.session.commit()
        user = Patientsusers.query.filter_by(email=email).first()
        return jsonify({
            'message': "User created",
            'user': {
                'username': user.username, "email":user.email, "id":user.id, 'img':user.img_link
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
                    "img":i.img_link,
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
    choice = request.args.get('category', type=str)
    list = []
    if choice:
        blogs = Posts.query.filter_by(cateory=choice)
        for i in blogs:
                list.append({
                    "catagory":i.cateory,
                    "id":i.id,
                    "drname":i.dr_name,
                    "title":i.title,
                    "description":i.description,
                    "img":i.img_link,
                    'created_at': i.created_at,
                    'upated_at': i.updated_at
                })
        return jsonify({'data':list}),HTTP_200_OK
    
    blogs = Posts.query.all()
    for i in blogs:
            list.append({
                "catagory":i.cateory,
                "id":i.id,
                "drname":i.dr_name,
                "title":i.title,
                "description":i.description,
                "img":i.img_link,
                'created_at': i.created_at,
                'upated_at': i.updated_at
            })
    return jsonify({'data':list}),HTTP_200_OK
# "cardiology","Neeurology", "Gynaecology", "Endocrinology", "General", "Medicine", "Ayurveda"
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
        try:
            title = request.json['title']
            link_list = request.json['l_list']
            id = request.json['id'] #take id from Patient_user table so that we can create multiple collection for patients
            collect = Collection(user_id=id, coll_name=title)
            db.session.add(collect)
            db.session.commit()
            for i in link_list:
                colname = title
                url = i["link"]
                name = i["name"]
                path = i["path"]
                extract = Extracter(user_id=id, col_name=colname, pdfname=name, url=url, path=path)
                db.session.add(extract)
                db.session.commit()
            user = Collection.query.filter_by(user_id = id, coll_name=title).first()
            user2 = Extracter.query.filter_by(user_id=id, col_name=user.coll_name)
            list = []
            for i in user2:
                list.append({
                    "url":i.url,
                    "name":i.pdfname,
                    "path":i.path,
                    "pdf_id":i.id
                })
            
            return jsonify({"collection":user.coll_name,"id":user.id,"created":user.created_at,"list":list}), HTTP_200_OK

            

        except Exception as e:
            return jsonify({"msg":"something went wrong","error":e}), HTTP_500_INTERNAL_SERVER_ERROR
    try:
        id = request.args.get('id', type=int)
        list = []
        user = Collection.query.filter_by(user_id=id)
        for i in user:
            col = i.coll_name
            l = []
            user2 = Extracter.query.filter_by(col_name=col,user_id=id)
            for j in user2:
                l.append({
                    "url":j.url,
                    "name":j.pdfname,
                    "path":j.path,
                    "pdf_id":j.id,
                    "created":j.created_at
                })
            list.append({"collection":i.coll_name,"id":i.id,"created":i.created_at,"list":l})    
            
       
        return jsonify({"list":list})
    except Exception:
        return jsonify({"msg":"ID does not exist"}), HTTP_400_BAD_REQUEST



# edit user detail from patient side 

@views.put('/update_patient')
def edituser():
    try:
        id = request.args.get('id')
        user = Patientsusers.query.filter_by(id=id).first()
        if user:
            name = request.json['name']
            img = request.json['img']
            mobile = request.json['mobile']
            email = request.json['email']
            user.username=name
            user.mobile=mobile
            user.email=email
            user.img_link=img
            db.session.commit()
        return jsonify({
            "name":user.username,
            "img":user.img_link,
            "mobile":user.mobile,
            "email":user.email
        }), HTTP_201_CREATED
        
    except Exception as e:
        return jsonify({"msg":"you can't change parent"}), HTTP_404_NOT_FOUND


# edit user detail from patient side 

@views.put('/update_docuser')
def edit_user():
    try:
        id = request.args.get('id')
        user = Users.query.filter_by(id=id).first()
        if user:
            name = request.json['name']
            img = request.json['img']
            mobile = request.json['mobile']
            email = request.json['email']
            user.username=name
            user.mobile=mobile
            user.email=email
            user.img_link=img
            db.session.commit()
        return jsonify({
            "name":user.username,
            "img":user.img_link,
            "mobile":user.mobile,
            "email":user.email
        }), HTTP_201_CREATED
        
    except Exception as e:
        return jsonify({"msg":"id not found"}), HTTP_404_NOT_FOUND


@views.route('/pdf', methods=['GET','POST','PUT','DELETE'])
def pdf():
    if request.method == 'POST':
        try:
            id = request.json['id']
            pdfname = request.json['pdfname']
            type = request.json['type']
            pdfurl = request.json['url']
            path = request.json['path']
            user = Extracter(user_id=id, col_name=type, pdfname=pdfname,url=pdfurl, path=path )
            db.session.add(user)
            db.session.commit()
            find = Extracter.query.filter_by(pdfname=pdfname,col_name=type).first()
            return jsonify({
                "id":find.id,
                "user_id": find.user_id,
                "padfname":find.pdfname,
                "type":find.col_name,
                "pdfurl":find.url,
                "path":find.path
            })
            
        except Exception as e:
            return jsonify({"msg":"error"})

    elif request.method == 'GET':
        id = request.args.get('id')
        type = 'pdf'
        pdfs = Extracter.query.filter_by(user_id=id, col_name=type)
        list = []
        for pdf in pdfs:
            list.append({
                "id":pdf.id,
                "user_id":pdf.user_id,
                "type":pdf.col_name,
                "pdfname":pdf.pdfname,
                "url":pdf.url,
                "path":pdf.path
            })

        return jsonify({"list":list})

@views.put('/update_blog')
def editblog():
    try:
        id = request.args.get('id')
        user = Posts.query.filter_by(id=id).first()
        if user:
            title = request.json['title']
            imglink = request.json['img_link']
            category = request.json['category']
            description = request.json['description']
            user.title=title
            user.img_link=imglink
            user.cateory=category
            user.description=description
            db.session.commit()
        return jsonify({
            "title":user.title,
            "img_link":user.img_link,
            "category":user.cateory,
            "description":user.description,
            "update_at":user.updated_at,
            "id":user.id
        }), HTTP_201_CREATED
        
    except Exception as e:
        return jsonify({"msg":"id not found"}), HTTP_404_NOT_FOUND