from flask import Blueprint, request

from init import db

from models.schedule import Schedule, schedule_schema, schedules_schema

schedules_bp = Blueprint('schedules', __name__, url_prefix='/schedules')

# get ALL schedules - GET (schedule, subject, room, timeslot)
@schedules_bp.route('/', methods=['GET'])
def get_all_schedules():
    schedules = Schedule.query.all()
    schedules_list = [{'id': schedule.id} for schedule in schedules]
    return jsonify('schedules': schedules_list)