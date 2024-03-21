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