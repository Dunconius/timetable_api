from flask import Blueprint, request, jsonify

from init import db
from models.room import Room, room_schema, rooms_schema

rooms_bp = Blueprint('rooms', __name__, url_prefix='/rooms')

# get ALL time slots - GET
@rooms_bp.route('/', methods=['GET'])
def get_all_rooms():
    rooms = Room.query.all()
    rooms_list = [{'id': room.id, 'Building': room.building_number, 'Room Number': room.room_number} for room in rooms]
    return jsonify({'rooms': rooms_list})

# get ONE time slot and show bookings that time.
@rooms_bp.route('/<int:room_id>')
def get_one_room(room_id):
    room = Room.query.get_or_404(room_id)

    # subjects = [subject_schema.dump(subject) for subject in room.subjects]

    return {
        "Room": room_schema.dump(room)       
    }
