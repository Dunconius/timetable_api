from flask import Blueprint, request

from init import db
from models.subject import Subject, subject_schema, subjects_schema
from models.teacher import Teacher
from controllers.teacher_controller import teachers_bp

subjects_bp = Blueprint('subjects', __name__, url_prefix='/subjects')
subjects_bp.register_blueprint(teachers_bp)

# get ALL subjects and show the classes they're teaching - GET
@subjects_bp.route('/')
def get_all_subjects():
    stmt = db.select(Subject)
    subjects = db.session.scalars(stmt)
    return subjects_schema.dump(subjects)

# get ONE teacher (dynamic route) and show the classes they're teaching - GET

# create teacher (admin only) - POST

# delete teacher (admin only) - DELETE

# edit teacher (admin only) - PUT, PATCH