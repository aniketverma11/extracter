from constants.http_statscode import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from flask import Blueprint, request
from flask.json import jsonify
import validators
from flask_jwt_extended import get_jwt_identity, jwt_required
from database import *


dele = Blueprint("del", __name__, url_prefix="/api/v1/del")


@dele.route('/doctors',methods=['GET','DELETE'])
def doctors():
    if request.method=='GET':
        find = User.query.all()
        list = []
        for i in find:
            list.append({
                'id':i.id,
                'name':i.username,
                'mobile':i.mobile,
                'email':i.email,
                'role':i.role,
                'created':i.created_at
            })
        return jsonify({'data':list})
    id = request.args.get('id')
    found_id = User.query.filter_by(id=id).first()
    if found_id:
        db.session.delete(found_id)
        db.session.commit()
        return jsonify({
            "msg":"successfully delete"
        })
    return jsonify({
            "msg":"user does not exist"
        })

@dele.route('/doctor_user',methods=['GET','DELETE'])
def doctors_user():
    if request.method=='GET':
        find = Users.query.all()
        list = []
        for i in find:
            list.append({
                'id':i.id,
                'name':i.username,
                'mobile':i.mobile,
                'email':i.email,
                'created':i.created_at
            })
        return jsonify({'data':list})
    id = request.args.get('id')
    found_id = Users.query.filter_by(id=id).first()
    if found_id:
        db.session.delete(found_id)
        db.session.commit()
        return jsonify({
            "msg":"successfully delete"
        })
    return jsonify({
            "msg":"user does not exist"
        })

@dele.route('/patients',methods=['GET','DELETE'])
def patients():
    if request.method=='GET':
        find = Patients.query.all()
        list = []
        for i in find:
            list.append({
                'id':i.id,
                'name':i.username,
                'mobile':i.mobile,
                'email':i.email,
                'role':i.role,
                'created':i.created_at
            })
        return jsonify({'data':list})
    id = request.args.get('id')
    found_id = Patients.query.filter_by(id=id).first()
    if found_id:
        db.session.delete(found_id)
        db.session.commit()
        return jsonify({
            "msg":"successfully delete"
        })
    return jsonify({
            "msg":"user does not exist"
        })


@dele.route('/Patients_user',methods=['GET','DELETE'])
def patients_user():
    if request.method=='GET':
        find = Patientsusers.query.all()
        list = []
        for i in find:
            list.append({
                'id':i.id,
                'name':i.username,
                'mobile':i.mobile,
                'email':i.email,
                'created':i.created_at
            })
        return jsonify({'data':list})
    id = request.args.get('id')
    found_id = Patientsusers.query.filter_by(id=id).first()
    if found_id:
        db.session.delete(found_id)
        db.session.commit()
        return jsonify({
            "msg":"successfully delete"
        })
    return jsonify({
            "msg":"user does not exist"
        })

@dele.route('/blogs',methods=['GET','DELETE'])
def blogs():
    if request.method=='GET':
        find = Posts.query.all()
        list = []
        for i in find:
            list.append({
                'id':i.id,
                'user_id':i.user_id,
                'name':i.title,
                'img':i.img_link,
                'catagory':i.cateory,
                'drname':i.dr_name,
                'descriptiion':i.description,
                'created':i.created_at
            })
        return jsonify({'data':list})
    id = request.args.get('id')
    found_id = Posts.query.filter_by(id=id).first()
    if found_id:
        db.session.delete(found_id)
        db.session.commit()
        return jsonify({
            "msg":"successfully delete"
        })
    return jsonify({
            "msg":"blog does not exist"
        })

@dele.route('/pdf',methods=['GET','DELETE'])
def pdf():
    if request.method=='GET':
        find = Extracter.query.all()
        list = []
        for i in find:
            list.append({
                'id':i.id,
                "collection":i.col_name,
                'pdfname':i.pdfname,
                "url":i.url,
                "path":i.path,
                'created':i.created_at
            })
        return jsonify({'data':list})
    id = request.args.get('id')
    found_id = Extracter.query.filter_by(id=id).first()
    if found_id:
        db.session.delete(found_id)
        db.session.commit()
        return jsonify({
            "msg":"successfully delete"
        })
    return jsonify({
            "msg":"collection does not exist"
        })

@dele.route('/col',methods=['GET','DELETE'])
def col():
    if request.method=='GET':
        find = Collection.query.all()
        list = []
        for i in find:
            list.append({
                'id':i.id,
                "collection":i.coll_name,
                'created':i.created_at

            })
                
        return jsonify({'data':list})