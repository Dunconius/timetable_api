from flask import Blueprint, request, jsonify

from init import db
from models.subject import Subject, subject_schema, subjects_schema
from models.teacher import Teacher, teacher_schema, teachers_schema
from models.cohort import Cohort, cohort_schema, cohorts_schema
# from controllers.teacher_controller import teachers_bp

subjects_bp = Blueprint('subjects', __name__, url_prefix='/subjects')
# subjects_bp.register_blueprint(teachers_bp)

# get ALL subjects - GET
@subjects_bp.route('/')
def get_all_subjects():
    stmt = db.select(Subject)
    subjects = db.session.scalars(stmt)
    return subjects_schema.dump(subjects)

# get ONE subject (dynamic route) and show it's cohort and teacher - GET
@subjects_bp.route('/<int:subject_id>')
def get_one_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)

    # Access the related teachers through the subjects's teacher relationship
    teacher = teacher_schema.dump(subject.teacher) if subject.teacher else None
    
    # Access the related cohorts through the subjects's cohort relationship
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
        subject_year = body_data.get('subject_year'),
        subject_name = body_data.get('subject_name'),
        teacher_id = body_data.get('teacher_id'),
        cohort_id = body_data.get('cohort_id')
    )

    # Add the subject to the database session and commit the transaction
    db.session.add(subject)
    db.session.commit()

    return subject_schema.dump(subject), 201

    # success_message = f"Subject '{subject.subject_year} {subject.subject_name}' added successfully!"

    # Return a JSON response with the serialized subject data
    # return jsonify({
    #     "Message": success_message,
    #     "Subject": subject_schema.dump(subject)
    #     }), 201

# delete subject (admin only) - DELETE
@subjects_bp.route('/<int:subject_id>', methods=['DELETE'])
def delete_subject(subject_id):
    stmt = db.select(Subject).where(Subject.id == subject_id)
    subject = db.session.scalar(stmt)

    if subject:
        db.session.delete(subject)
        db.session.commit()
        return {'message': f'Subject ID:{subject.id} Name:{subject.subject_year} {subject.subject_name} deleted successfully'}
    else:
        return {'error': f'Subject ID:{subject_id} not found'}, 404

# edit subject (admin only) - PUT, PATCH
@teachers_bp.route('/<int:subject_id>', methods=['PUT', 'PATCH'])
def update_subject(subject_id):
    body_data = subject_schema.load(request.get_json(), partial=True)
    stmt = db.select(Subject).filter_by(id=subject_id)
    subject = db.session.scalar(stmt)

    success_message = f"Subject '{subject.subject_year} {subject.subject_name}' updated successfully!"

    if subject:
        subject.subject_year = body_data.get('subject_year') or subject.subject_year
        subject.subject_name = body_data.get('subject_name') or subject.subject_name
        #subject.teacher_id = body_data.get('teacher_id') or subject.teacher_id
        #subject.cohort_id = body_data.get('subject_id') or subject.cohort_id
        db.session.commit()

        return jsonify({
            "message": success_message,
            "subject": subject_schema.dump(subject)
        })
    else:
        return {'error': f'Subject ID:{subject_id} not found'}, 404
