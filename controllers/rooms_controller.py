from flask import Blueprint, request, jsonify

from init import db
from models.room import Room, room_schema, rooms_schema
from models.booking import Booking, booking_schema, bookings_schema, booking_nested
from sqlalchemy.orm import joinedload

rooms_bp = Blueprint('rooms', __name__, url_prefix='/rooms')

# gets ALL rooms and returns their id, building, and room number
@rooms_bp.route('/', methods=['GET'])
def get_all_rooms():
    rooms = Room.query.all()
    rooms_list = [{'id': room.id, 'Building': room.building_number, 'Room Number': room.room_number} for room in rooms]
    return jsonify({'rooms': rooms_list})

# gets ONE room and shows all bookings in that room.
@rooms_bp.route('/<int:room_id>')
def get_one_room(room_id):
    room = Room.query.get(room_id)

    if room:
        # Fetch bookings associated with the room and include related attributes
        bookings = Booking.query.filter_by(room_id=room_id).options(
            joinedload(Booking.subject),  # Load data from the Subject model
            joinedload(Booking.time_slot)  # Load data from the TimeSlot model
        ).all()

        # Serialize bookings using the custom schema with related attributes
        serialized_bookings = [booking_nested.dump(booking) for booking in bookings]

        return {
            "Room": room_schema.dump(room),
            "Bookings": serialized_bookings
        }
    else:
        return {"error": f"Room ID:{room_id} not found"}, 404
    
