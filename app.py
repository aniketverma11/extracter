from flask.json import jsonify
from constants.http_statscode import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from flask import Flask, config, redirect
import os
from api import auth
from database import db
from flask_jwt_extended import JWTManager
from flasgger import Swagger, swag_from
from config.swagger import template, swagger_config
from views import views
from flask_migrate import Migrate


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    migrate = Migrate(app, db)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY="SECRET_key",
            SQLALCHEMY_DATABASE_URI= "sqlite:///blog.db",
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

    #Swagger(app, config=swagger_config, template=template)

    """@app.get('/<short_url>')
    @swag_from('./docs/short_url.yaml')
    def redirect_to_url(short_url):
        bookmark = Bookmark.query.filter_by(short_url=short_url).first_or_404()

        if bookmark:
            bookmark.visits = bookmark.visits+1
            db.session.commit()
            return redirect(bookmark.url)"""

    """@app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({'error': 'Not found'}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({'error': 'Something went wrong, we are working on it'}), HTTP_500_INTERNAL_SERVER_ERROR"""

    return app


application = create_app()