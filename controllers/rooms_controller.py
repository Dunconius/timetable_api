from flask import Blueprint, request, jsonify

from init import db
from models.room import Room, room_schema, rooms_schema



rooms_bp = Blueprint('rooms', __name__, url_prefix='/rooms')

# get ALL time slots - GET
@rooms_bp.route('/', methods=['GET'])
def get_all_times():
    rooms = TimeSlot.query.all()
    rooms_list = [{'id': time_slot.id, 'Day': time_slot.time_slot_day, 'Time': time_slot.time_slot_time} for time_slot in rooms]
    return jsonify({'timeslots': rooms_list})

# get ONE time slot and show schedules that time.
@rooms_bp.route('/<int:time_slot_id>')
def get_one_timeslot(time_slot_id):
    time_slot = TimeSlot.query.get_or_404(time_slot_id)

    # subjects = [subject_schema.dump(subject) for subject in time_slot.subjects]

    return {
        "time slot": time_slot_schema.dump(time_slot)       
    }
