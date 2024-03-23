from flask import Blueprint, request, jsonify
from init import db
from models.subject import Subject, subject_schema, subjects_schema
from models.teacher import Teacher, teacher_schema, teachers_schema
from models.cohort import Cohort, cohort_schema, cohorts_schema

subjects_bp = Blueprint('subjects', __name__, url_prefix='/subjects')

# get ALL subjects - GET
@subjects_bp.route('/')
def get_all_subjects():
    stmt = db.select(Subject)
    subjects = db.session.scalars(stmt)
    return subjects_schema.dump(subjects)

# get ONE subject (dynamic route) and show its cohort and teacher - GET
@subjects_bp.route('/<int:subject_id>')
def get_one_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    teacher = teacher_schema.dump(subject.teacher) if subject.teacher else None
    cohort = cohort_schema.dump(subject.cohort) if subject.cohort else None

    return {
        "subject": subject_schema.dump(subject),
        "teacher": teacher,
        "cohort": cohort
    }

# create subject (admin only) - POST
@subjects_bp.route('/', methods=['POST'])
def add_subject():
    body_data = subject_schema.load(request.get_json())

    subject = Subject(
        subject_year=body_data.get('subject_year'),
        subject_name=body_data.get('subject_name'),
        teacher_id=body_data.get('teacher_id'),
        cohort_id=body_data.get('cohort_id')
    )

    db.session.add(subject)
    db.session.commit()

    return subject_schema.dump(subject), 201

# delete subject (admin only) - DELETE
@subjects_bp.route('/<int:subject_id>', methods=['DELETE'])
def delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)

    db.session.delete(subject)
    db.session.commit()

    return {'message': f'Subject ID:{subject.id} Name:{subject.subject_year} {subject.subject_name} deleted successfully'}

# edit subject (admin only) - PUT, PATCH
@subjects_bp.route('/<int:subject_id>', methods=['PUT', 'PATCH'])
def update_subject(subject_id):
    body_data = subject_schema.load(request.get_json(), partial=True)
    subject = Subject.query.get_or_404(subject_id)

    subject.subject_year = body_data.get('subject_year', subject.subject_year)
    subject.subject_name = body_data.get('subject_name', subject.subject_name)
    subject.teacher_id = body_data.get('teacher_id', subject.teacher_id)
    subject.cohort_id = body_data.get('cohort_id', subject.cohort_id)

    db.session.commit()

    return jsonify({
        "message": f"Subject '{subject.subject_year} {subject.subject_name}' updated successfully!",
        "subject": subject_schema.dump(subject)
    })

