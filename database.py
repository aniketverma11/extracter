from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import app
from flask_migrate import Migrate

from sqlalchemy import Column
db = SQLAlchemy()



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),nullable=False)
    mobile = db.Column(db.Integer, nullable=True)
    role = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(120), nullable=True)
    password = db.Column(db.Text(), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    doccument = db.relationship('Users', backref="user")

    def __repr__(self) -> str:
        return 'User>>> {self.username}', 'User_id>>> {self.id}'


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    img_link = db.Column(db.String(500), nullable=True)
    username = db.Column(db.String(80),nullable=False)
    mobile = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    doccument = db.relationship('Posts', backref="users")
    def __repr__(self) -> str:
        return f'User>>> {self.id}, {self.username}'


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    img_link = db.Column(db.String(500), nullable=True)
    title = db.Column(db.String(80), nullable=True)
    reading_time=db.Column(db.String(10), nullable=True)
    cateory=db.Column(db.String(80), nullable=True)
    description = db.Column(db.String(350), nullable=True)
    dr_name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    #doccument = db.relationship('Posts', backref="posts")
    def __repr__(self) -> str:
        return f'User>>> {self.id}'

class Patients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),nullable=False)
    mobile = db.Column(db.Integer, nullable=True)
    role = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(120), nullable=True)
    password = db.Column(db.Text(), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    doccument = db.relationship('Patientsusers', backref="Patients")

    def __repr__(self) -> str:
        return 'User>>> {self.username}', 'User_id>>> {self.id}'

class Patientsusers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    username = db.Column(db.String(80),nullable=False)
    mobile = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    doccument = db.relationship('Collection', backref="Patientsusers")
    def __repr__(self) -> str:
        return f'User>>> {self.id}, {self.username}'


class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('patientsusers.id'))
    coll_name = db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    doccument = db.relationship('Extracter', backref="Collection")
    def __repr__(self) -> str:
        return f'User>>> {self.id}, {self.coll_name}'


class Extracter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), db.ForeignKey('collection.coll_name'))
    col_name = db.Column(db.String(80), nullable=True)
    pdfname=db.Column(db.String(80), nullable=True)
    url = db.Column(db.String(500), nullable=True)
    path = db.Column(db.String(500), nullable=True)
    visits = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __repr__(self) -> str:
        return f'doccument>>> {self.id}, {self.url}'

