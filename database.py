from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random
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
    doccument = db.relationship('Patients_Users', backref="Patients")

    def __repr__(self) -> str:
        return 'User>>> {self.username}', 'User_id>>> {self.id}'

class Patients_Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    username = db.Column(db.String(80),nullable=False)
    mobile = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    #doccument = db.relationship('Patients', backref="Patients_Users")
    def __repr__(self) -> str:
        return f'User>>> {self.id}, {self.username}'

class PDF_Extracter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=True)
    url = db.Column(db.Text, nullable=False)
    short_url = db.Column(db.String(3), nullable=True)
    visits = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def generate_short_characters(self):
        characters = string.digits+string.ascii_letters
        picked_chars = ''.join(random.choices(characters, k=3))

        link = self.query.filter_by(short_url=picked_chars).first()

        if link:
            self.generate_short_characters()
        else:
            return picked_chars

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.short_url = self.generate_short_characters()

    def __repr__(self) -> str:
        return 'doccument>>> {self.url}'
