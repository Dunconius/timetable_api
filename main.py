import os
from flask import Flask
from marshmallow.exceptions import ValidationError
from init import db, ma, bcrypt, jwt

# Import SQLAlchemy models and relationships
from models.teacher import Teacher
from models.cohort import Cohort
from models.time_slot import TimeSlot
from models.room import Room
from models.subject import Subject
from models.booking import booking
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
    from controllers.cli_controller import db_commands
    app.register_blueprint(db_commands)
    
    from controllers.teacher_controller import teachers_bp
    app.register_blueprint(teachers_bp)

    from controllers.subject_controller import subjects_bp
    app.register_blueprint(subjects_bp)

    from controllers.cohort_controller import cohorts_bp
    app.register_blueprint(cohorts_bp)

    from controllers.times_controller import time_slots_bp
    app.register_blueprint(time_slots_bp)

    from controllers.rooms_controller import rooms_bp
    app.register_blueprint(rooms_bp)

    from controllers.booking_controller import bookings_bp
    app.register_blueprint(bookings_bp)
    
    return app