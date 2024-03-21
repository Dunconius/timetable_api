from flask import Blueprint, request, jsonify

from init import db
from models.time_slot import TimeSlot, time_slot_schema, time_slots_schema

from models.subject import Subject, subject_schema, subjects_schema
from controllers.subject_controller import subjects_bp

time_slots_bp = Blueprint('time_slots', __name__, url_prefix='/time_slots')

# get ALL time slots - GET
@time_slots_bp.route('/', methods=['GET'])
def get_all_times():
    time_slots = TimeSlot.query.all()
    time_slots_list = [{'id': time_slot.id, 'Day': time_slot.time_slot_day, 'Time': time_slot.time_slot_time} for time_slot in time_slots]
    return jsonify({'timeslots': time_slots_list})

# get ONE time slot and show schedules that time.
@time_slots_bp.route('/<int:time_slot_id>')
def get_one_timeslot(time_slot_id):
    time_slot = TimeSlot.query.get_or_404(time_slot_id)

    # subjects = [subject_schema.dump(subject) for subject in time_slot.subjects]

    return {
        "time slot": time_slot_schema.dump(time_slot)       
    }
