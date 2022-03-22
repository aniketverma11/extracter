from flask.json import jsonify
from constants.http_statscode import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from flask import Flask, config, redirect
import os
from api import auth
from database import db
from flask_jwt_extended import JWTManager
from views import views
from flask_migrate import Migrate


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    migrate = Migrate(app, db, render_as_batch=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY="SECRET_key",
            SQLALCHEMY_DATABASE_URI= "sqlite:///simpli.db",
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY="This_is_a_key"


        )
    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)

    JWTManager(app)
    app.register_blueprint(auth)
    app.register_blueprint(views)
    return app


application = create_app()