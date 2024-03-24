from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from init import db
from models.cohort import Cohort, cohort_schema, cohorts_schema
from models.subject import Subject, subject_schema, subjects_schema
from controllers.subject_controller import subjects_bp

#bits for admin authorization
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from controllers.auth_utils import check_admin

cohorts_bp = Blueprint('cohorts', __name__, url_prefix='/cohorts')

# Gets all cohorts and returns their ID and year group
@cohorts_bp.route('/', methods=['GET'])
def get_all_cohorts():
    cohorts = Cohort.query.all()
    cohorts_list = [{"id": cohort.id, "Year Group": cohort.year_group} for cohort in cohorts]
    return jsonify({"cohorts": cohorts_list})

# Gets one cohort and returns the subjects they are enrolled into
@cohorts_bp.route('/<int:cohort_id>')
def get_one_cohort(cohort_id):
    cohort = Cohort.query.get(cohort_id)

    if cohort:
        subjects = [subject_schema.dump(subject) for subject in cohort.subjects]
        return {
            "cohort": cohort_schema.dump(cohort),
            "subject": subjects       
        }
    else:
        return {"error": f"Cohort ID:{cohort_id} not found"}, 404

# Adds a new cohort entry. Requires admin auth. Cohort details required in the body request
@cohorts_bp.route('/', methods=['POST'])
@jwt_required()
@check_admin
def add_cohort():
    try:
        # Attempt to load the data from the request JSON using cohort_schema
        body_data = cohort_schema.load(request.get_json())
    except ValidationError as e:
        # Handle the validation error by returning a custom error message
        return {"error": str(e)}, 400  # Return a 400 Bad Request status code

    # If the data is valid, proceed with cohort creation
    cohort = Cohort(
        year_group=body_data.get('year_group')
    )
    db.session.add(cohort)
    db.session.commit()

    # Construct the success message after the cohort is added
    success_message = {
        'message': 'Cohort added successfully',
        'cohort': cohort_schema.dump(cohort)
    }

    return jsonify(success_message), 201  # Return a 201 Created status code

# Deletes a cohort entry. Requires admin auth. Cohort_id required in dynamic route
@cohorts_bp.route('/<int:cohort_id>', methods=['DELETE'])
@jwt_required()
@check_admin
def delete_cohort(cohort_id):
    stmt = db.select(Cohort).where(Cohort.id == cohort_id)
    cohort = db.session.scalar(stmt)

    if cohort:
        db.session.delete(cohort)
        db.session.commit()
        return {'message': f'Cohort ID:{cohort.id} year:{cohort.year_group} deleted successfully'}
    else:
        return {'error': f'Cohort ID:{cohort_id} not found'}, 404
    
# Updates an existing cohort. Requires admin auth. Cohort_id required in dynamic route. Cohort details required in the body request
@cohorts_bp.route('/<int:cohort_id>', methods=['PUT', 'PATCH'])
@jwt_required()
@check_admin
def update_cohort(cohort_id):
    body_data = cohort_schema.load(request.get_json(), partial=True)
    stmt = db.select(Cohort).filter_by(id=cohort_id)
    cohort = db.session.scalar(stmt)

    if cohort:
        cohort.year_group = body_data.get('year_group') or cohort.year_group
        db.session.commit()

        # Construct the success message
        success_message = {
            'message': 'Cohort updated successfully',
            'cohort': cohort_schema.dump(cohort)
        }

        return jsonify(success_message)
    else:
        return {'error': f'Cohort ID:{cohort_id} not found'}, 404