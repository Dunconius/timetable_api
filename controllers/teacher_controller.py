from flask import Blueprint, request, jsonify

from init import db

from models.teacher import Teacher, teacher_schema, teachers_schema
from models.subject import Subject, subject_schema, subjects_schema

teachers_bp = Blueprint('teachers', __name__, url_prefix='/teachers')

# get ALL teachers - GET
@teachers_bp.route('/', methods=['GET'])
def get_all_teachers():
    teachers = Teacher.query.all()
    teachers_list = [{"id": teacher.id, "name": teacher.teacher_name} for teacher in teachers]
    return jsonify({"teachers": teachers_list})

# get ONE teacher (dynamic route) and show the classes they're teaching - GET
@teachers_bp.route('/<int:teacher_id>')
def get_one_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)

    # Access the related subjects through the teacher's subjects relationship
    subjects = [subject_schema.dump(subject) for subject in teacher.subjects]

    return {
        "teacher": teacher_schema.dump(teacher),
        "subjects": subjects
    }

# create teacher (admin only) - POST

# delete teacher (admin only) - DELETE

# edit teacher (admin only) - PUT, PATCH



