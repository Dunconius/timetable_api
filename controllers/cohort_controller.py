from flask import Blueprint, request, jsonify

from init import db
from models.cohort import Cohort, cohort_schema, cohorts_schema
from models.subject import Subject, subject_schema, subjects_schema
from controllers.subject_controller import subjects_bp


cohorts_bp = Blueprint('cohorts', __name__, url_prefix='/cohorts')

# get ALL cohorts - GET
@cohorts_bp.route('/', methods=['GET'])
def get_all_cohorts():
    cohorts = Cohort.query.all()
    cohorts_list = [{"id": cohort.id, "Year Group": cohort.year_group} for cohort in cohorts]
    return jsonify({"cohorts": cohorts_list})

# get ONE cohort (dynamic route) and show all it's subjects - GET
@cohorts_bp.route('/<int:cohort_id>')
def get_one_cohort(cohort_id):
    cohort = Cohort.query.get_or_404(cohort_id)
    
    subjects = [subject_schema.dump(subject) for subject in cohort.subjects]

    return {
        "cohort": cohort_schema.dump(cohort),
        "subject": subjects       
    }

# CREATE new cohort
@cohorts_bp.route('/', methods=['POST'])
def add_cohort():
    body_data = cohort_schema.load(request.get_json())

    cohort = Cohort(
        year_group = body_data.get('year_group')
    )
    db.session.add(cohort)
    db.session.commit()

    return cohort_schema.dump(cohort), 201

# DELETE cohort
@cohorts_bp.route('/<int:cohort_id>', methods=['DELETE'])
def delete_cohort(cohort_id):
    stmt = db.select(Cohort).where(Cohort.id == cohort_id)
    cohort = db.session.scalar(stmt)

    if cohort:
        db.session.delete(cohort)
        db.session.commit()
        return {'message': f'Cohort ID:{cohort.id} year:{cohort.year_group} deleted successfully'}
    else:
        return {'error': f'Cohort ID:{cohort_id} not found'}, 404
    
# UPDATE cohort
@cohorts_bp.route('/<int:cohort_id>', methods=['PUT', 'PATCH'])
def update_cohort(cohort_id):
    body_data = cohort_schema.load(request.get_json(), partial=True)
    stmt = db.select(Cohort).filter_by(id=cohort_id)
    cohort = db.session.scalar(stmt)

    if cohort:
        cohort.year_group = body_data.get('year_group') or cohort.year_group
        db.session.commit()
        return cohort_schema.dump(cohort)
    else:
        return {'error': f'Cohort ID:{cohort_id} not found'}, 404