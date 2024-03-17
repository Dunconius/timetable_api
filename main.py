import os
from flask import Flask
from marshmallow.exceptions import ValidationError
from init import db, ma, bcrypt, jwt

# Import SQLAlchemy models and relationships
#from models.teacher import Teacher
#from models.subject import Subject
# Import the file that defines relationships
#from relationships.relationships import *

def create_app():
    app = Flask(__name__)

    # this is telling flask not to sort the keys, as it's sorting was overwriting what we told marshmallow to sort.
    app.json.sort_keys = False

    # configs
    app.config["SQLALCHEMY_DATABASE_URI"]=os.environ.get("DATABASE_URI")
    app.config["JWT_SECRET_KEY"]=os.environ.get("JWT_SECRET_KEY")

    # connect libraries with flask app
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # global error handlers
    @app.errorhandler(400)
    def bad_request(err):
        return {"error": str(err)}, 400
    
    @app.errorhandler(404)
    def not_found(err):
        return {"error": str(err)}, 404

    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {"error": err.messages}, 400
    
    # importing from the controllers file. Registered the blueprint with the flask app instance
    from controllers.teacher_controller import teachers_bp
    app.register_blueprint(teachers_bp)

    from controllers.
    
    return app