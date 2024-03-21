from flask import Blueprint, request

from init import db
from models.subject import Subject, subject_schema, subjects_schema
from models.teacher import Teacher, teacher_schema, teachers_schema
from models.cohort import Cohort, cohort_schema, cohorts_schema
from controllers.teacher_controller import teachers_bp

cohorts_bp = Blueprint('cohorts', __name__, url_prefix='/cohorts')
cohorts_bp.register_blueprint(cohorts_bp)

# get ALL cohorts - GET
@cohorts_bp.route('/')
def get_all_cohorts():
    cohorts = Cohort.query.all()
    return cohorts_schema.dump(cohorts)
    
    # stmt = db.select(Cohort)
    # cohorts = db.session.scalars(stmt)
    # return cohorts_schema.dump(cohorts)
    
    
    
    # cohorts = Cohort.query.all()
    # cohorts_list = [{"id": cohort.id, "name": cohort.year_group} for cohort in cohorts]
    # return jsonify({"cohorts": cohorts_list})