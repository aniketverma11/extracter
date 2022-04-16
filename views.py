from constants.http_statscode import HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR
from flask import Blueprint, request
from flask.json import jsonify
import validators
from flask_jwt_extended import get_jwt_identity, jwt_required
from database import *

views = Blueprint("views", __name__, url_prefix="/api/v1/views")


#create doctors manuall
@views.post('/doc')
def doc():
    name=request.json['name']
    speciality =request.json['speciality']
    mobile = request.json['mobile']
    email = request.json['email']
    doc = User(username=name, mobile=mobile, speciality=speciality, email=email, role="doctor")
    db.session.add(doc)
    db.session.commit()
    doc2 = User.query.filter_by(mobile=mobile).first()
    return jsonify({
        'id':doc2.id,
        'name':doc2.username,
        'mobile':doc2.mobile,
        'email':doc2.email,
        'speciality':doc2.speciality
    })
  

#create doctor user
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

@views.route("/user_blog_create", methods=['POST','GET','PUT'])
def blogs():
    if request.method == 'POST':
        time = request.json["reading_time"]
        title=request.json["title"]
        img_link=request.json["im_link"]
        category = request.json["category"]
        description = request.json["description"]
        drname = request.json["dr_name"]
        id = request.json["id"]
        type = request.json["type"] # type would be post or draft
        blog = Posts(user_id = id, reading_time=time,title=title, cateory=category, description=description, dr_name=drname, img_link=img_link,type=type)
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
                    "type":user.type,
                    "description":user.description,
                    "creater_at":user.created_at

                }
            }), HTTP_201_CREATED
    #for update the type from draft to post or viceversa   
    elif request.method=='PUT':
        try:
            id = request.args.get('id')
            post = Posts.query.filter_by(id=id).first()
            if post:
                time = request.json["reading_time"]
                title=request.json["title"]
                img_link=request.json["im_link"]
                category = request.json["category"]
                description = request.json["description"]
                drname = request.json["dr_name"]
                type = request.json['type']
                post.title=title
                post.reading_time=time
                post.img_link=img_link
                post.cateory=category
                post.description=description
                post.dr_name=drname
                post.type=type
                db.session.commit()
                return jsonify({
                    "title":post.title,
                    "img_link":post.img_link,
                    "category":post.cateory,
                    "description":post.description,
                    "update_at":post.updated_at,
                    "id":post.id,
                    "type":post.type
                })
        
        except Exception as e:
            return jsonify({"msg":"id not found"})



    choice = ["Cardiology","Neurology", "Gynaecology", "Endocrinology", "General", "Medicine", "Ayurveda"]
    return jsonify({"catagories":choice})

@views.get("/drafts")
def drafts():
    id = request.args.get("id")
    list = []
    posts = Posts.query.filter_by(user_id=id,type='draft')
    for i in posts:
        list.append({
            "catagory":i.cateory,
            "id":i.id,
            "drname":i.dr_name,
            "title":i.title,
            "description":i.description,
            "img":i.img_link,
            'created_at': i.created_at,
            'upated_at': i.updated_at,
            "type":i.type
        })
    return jsonify({'data':list}),HTTP_200_OK



@views.get("/all_posts")
def all_post():
    id = request.args.get("id")
    list = []
    posts = Posts.query.filter_by(user_id=id,type='post')
    for i in posts:
        list.append({
            "catagory":i.cateory,
            "id":i.id,
            "drname":i.dr_name,
            "title":i.title,
            "description":i.description,
            "img":i.img_link,
            'created_at': i.created_at,
            'upated_at': i.updated_at,
            "type":i.type
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
    choice = request.args.get('category', type=str)
    list = []
    if choice:
        doctors = User.query.filter_by(speciality=choice)
        for i in doctors:
                list.append({
                    "id":i.id,
                    "name":i.user,
                    "mobile":i.mobile,
                    "email":i.email,
                    "speciality":i.speciality
                                      
                })
        return jsonify({'contact':list}),HTTP_200_OK
    doctors = User.query.all()
    list =[]
    for doctor in doctors:
        list.append({
            "id":doctor.id,
            "name":doctor.username,
            "mobile":doctor.mobile,
            "email":doctor.email
        })
    return jsonify({"contacts":list})


# for the collection of pdf files 

@views.route('/collection', methods=['POST', 'GET','PUT','DELETE'])
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
    
    #collection delete
    elif request.method=="DELETE":
        id = request.args.get("id")
        found_id = Collection.query.filter_by(id=id).first()
        found_pdf = Extracter.query.filter_by(col_name=found_id.coll_name)
        for pdf in found_pdf:
            db.session.delete(pdf)
            db.session.commit()
        if found_id:
            db.session.delete(found_id)
            db.session.commit()
            return jsonify({
                "msg":"successfully delete"
            })
        return jsonify({
                "msg":"user does not exist"
            })
    #collection rename
    elif request.method=="PUT":
        try:
            id = request.args.get("id")
            newcollectionname= request.json['name']
            collection = Collection.query.filter_by(id = id).first()
            col = collection.coll_name
            colnamepdf = Extracter.query.filter_by(col_name=col)
            for coll in colnamepdf:
                coll.col_name=newcollectionname
                db.session.commit()
            collection.coll_name = newcollectionname
            db.session.commit()
            return jsonify({"msg":"Update Succesfully"})
        except Exception as e:
            return jsonify({"msg":"internal server error"},e)

    #collection get on particular id
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


# get a particular collection
@views.get('/coll')
def coll():
    try:
        id = request.args.get('id', type=int)
        user_id = request.args.get('userid', type=int)
        collection = Collection.query.filter_by(id=id).first()
        coll = collection.coll_name
        pdf = Extracter.query.filter_by(col_name=coll, user_id=user_id)
        list = []
        for j in pdf:
            list.append({
                "url":j.url,
                "name":j.pdfname,
                "path":j.path,
                "pdf_id":j.id,
                "created":j.created_at
            })    
            
       
        return jsonify({"collection":collection.coll_name, "id":collection.id,"list":list})
    except Exception as e:
        return jsonify({"msg":"collection not found"},e), HTTP_400_BAD_REQUEST


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

        return jsonify({"list":list}),HTTP_202_ACCEPTED

    elif request.method=='PUT':
        id = request.args.get('id')
        newname = request.json['name']
        findpdf = Extracter.query.filter_by(id=id).first()
        findpdf.pdfname = newname
        db.session.commit()
        return jsonify({"msg":"Renamed succesfully"})

    elif request.method=='DELETE':
        id = request.args.get('id')
        pdf = Extracter.query.filter_by(id=id).first()
        db.session.delete(pdf)
        db.session.commit()
        return jsonify({"msg":"Delete succesfully"}),HTTP_200_OK



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

#create quesnairy for patient
@views.route('/questions', methods=['GET','POST','PUT', 'DELETE'])
def questions():
    if request.method=='POST':
        userid = request.json['id']
        age = request.json['age']
        gender = request.json['gender']
        diet = request.json['diet']
        smoking = request.json['smoking']
        alcohol = request.json['alcohol']
        medication = request.json['regular_medication']
        dieases = request.json['dieases']
        complaints = request.json['complaints']

        questions = Questions(
            user_id=userid,
            age=age,
            gender=gender,
            diet=diet,
            smoking=smoking,
            alcohol=alcohol,
            medication=medication,
            dieases=str(dieases),
            complaints=str(complaints)
        )
        db.session.add(questions)
        db.session.commit()
        
        questions = Questions.query.filter_by(user_id=userid).first()
        return jsonify({"msg":"saved successfully"}),HTTP_201_CREATED

    elif request.method=='GET':
        id = request.args.get("id")
        questions = Questions.query.filter_by(id=id).first()
        return jsonify({
            "id":questions.id,
            "age":questions.age,
            "gender":questions.gender,
            "diet":questions.diet,
            "smoking":questions.smoking,
            "alcohol":questions.alcohol,
            "regular_medication":questions.medication,
            "dieases":questions.dieases,
            "complaints":questions.complaints
        }),HTTP_202_ACCEPTED

    elif request.method =='PUT':
        userid = request.args.get("id")
        questions = Questions.query.filter_by(id=userid).first()
        if questions:
            questions.age = request.json['age']
            questions.gender = request.json['gender']
            questions.diet = request.json['diet']
            questions.smoking = request.json['smoking']
            questions.alcohol = request.json['alcohol']
            questions.medication = request.json['regular_medication']
            questions.dieases = request.json['dieases']
            questions.complaints = request.json['complaints']
            db.session.commit()
            return jsonify({
                "msg":"updated succesfully"
            })
        else:
            return jsonify({
                "msg":"error"
            })

#Portal sharing
@views.route('/portal', methods=['PUT', 'GET', 'POST', 'DELETE'])
def portal():
    if request.method=='POST':
        #patient_id=request.json['patient_id']
        doctor_id=request.json['doctor_id']
        patient_name=request.json['patient_name']
        pdfname=request.json['pdfname']
        url=request.json['url']
        portal = Portal(doc_id=doctor_id,patientname=patient_name,pdfname=pdfname,url=url)
        db.session.add(portal)
        db.session.commit()
        return jsonify({
            "msg":"share succesfully"
        })

    elif request.method=='GET':
        doc_id= request.args.get("id")
        portal = Portal.query.filter_by(doc_id=doc_id)
        list = []
        for pdf in portal:
            list.append({
                "patient_id":pdf.pat_id,
                "patientname":pdf.patientname,
                "pdfname":pdf.pdfname,
                "url":pdf.url
            })

        return jsonify({
            "list":list
        })