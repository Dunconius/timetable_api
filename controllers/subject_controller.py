from flask import Blueprint, request, jsonify
from init import db
from models.subject import Subject, subject_schema, subjects_schema
from models.teacher import Teacher, teacher_schema, teachers_schema
from models.cohort import Cohort, cohort_schema, cohorts_schema

#bits for admin authorization
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from controllers.auth_utils import check_admin

subjects_bp = Blueprint('subjects', __name__, url_prefix='/subjects')

# Gets all subjects and returns their id, year group, and name
@subjects_bp.route('/')
def get_all_subjects():
    stmt = db.select(Subject)
    subjects = db.session.scalars(stmt)
    return subjects_schema.dump(subjects)

# Gets one subject and returns its corresponding cohort and teacher
@subjects_bp.route('/<int:subject_id>')
def get_one_subject(subject_id):
    subject = Subject.query.get(subject_id)

    if subject:
        teacher = teacher_schema.dump(subject.teacher) if subject.teacher else None
        cohort = cohort_schema.dump(subject.cohort) if subject.cohort else None

        return {
            "subject": subject_schema.dump(subject),
            "teacher": teacher,
            "cohort": cohort
        }
    else:
        return {"error": f"Subject {subject_id} not found"}, 404

# Adds a new subject. Requires admin auth. Subject details required in the body request
@subjects_bp.route('/', methods=['POST'])
@jwt_required()
@check_admin
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

# Deletes a subject. Requires admin auth. Subject_id required in dynamic route
@subjects_bp.route('/<int:subject_id>', methods=['DELETE'])
@jwt_required()
@check_admin
def delete_subject(subject_id):
    subject = Subject.query.get(subject_id)

    if subject:
        db.session.delete(subject)
        db.session.commit()
        return {'message': f'Subject ID:{subject.id} Name:{subject.subject_year} {subject.subject_name} deleted successfully'}
    else:
        return {"error": f"Subject {subject_id} not found"}, 404

# Updates an existing subject. Requires admin auth. Subject_id required in dynamic route. Subject details required in the body request
@subjects_bp.route('/<int:subject_id>', methods=['PUT', 'PATCH'])
@jwt_required()
@check_admin
def update_subject(subject_id):
    body_data = subject_schema.load(request.get_json(), partial=True)
    subject = Subject.query.get(subject_id)

    if subject:
        subject.subject_year = body_data.get('subject_year', subject.subject_year)
        subject.subject_name = body_data.get('subject_name', subject.subject_name)
        subject.teacher_id = body_data.get('teacher_id', subject.teacher_id)
        subject.cohort_id = body_data.get('cohort_id', subject.cohort_id)
        db.session.commit()
        return jsonify({
            "message": f"Subject '{subject.subject_year} {subject.subject_name}' updated successfully!",
            "subject": subject_schema.dump(subject)
        })
    else:
        return {"error": f"Subject {subject_id} not found"}, 404

