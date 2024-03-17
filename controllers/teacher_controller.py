from flask import Blueprint, request

from init import db

from models.teacher import Teacher, teacher_schema, teachers_schema

teachers_bp = Blueprint('teachers', __name__, url_prefix='/teachers')

# get ALL teachers and show the classes they're teaching - GET
@teachers_bp.route('/')
def get_all_teachers():
    stmt = db.select(Teacher)
    teachers = db.session.scalars(stmt)
    return teachers_schema.dump(teachers)

# get ONE teacher (dynamic route) and show the classes they're teaching - GET

# create teacher (admin only) - POST

# delete teacher (admin only) - DELETE

# edit teacher (admin only) - PUT, PATCH



