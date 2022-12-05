from flask import Flask,jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException


from extension import db, migrate, jwt, ma
from routes import register,post,log

# api = Api(app)
# db = SQLAlchemy(app)
def create_app():
    try:
        app = Flask(__name__)
        
        app.config['SECRET_KEY'] = "sdfhs8dhfuijekfodjiujjj"
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@127.0.0.1/beyondirr'

        register_additional_extensions(app)
        register_blueprint(app)


        @app.errorhandler(HTTPException)
        def error_handler(err):
            response = {
                'success': False,
                'msg': str(err),
            }
            return jsonify(response), 405

        return app
    except Exception as err:
        print("Error occured:", err)

def register_additional_extensions(app):
    """Register additional Flask extensions"""
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)

def register_blueprint(app):
    """Register Flask blueprints."""
    app.register_blueprint(register.usersprint, url_prefix="/api/v1")
    app.register_blueprint(post.postsprint, url_prefix="/api/v1")
    app.register_blueprint(log.logs_blueprint, url_prefix="/api/v1")
    
    return None
