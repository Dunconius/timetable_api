from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload

from init import db
from models.time_slot import TimeSlot, time_slot_schema, time_slots_schema
from models.booking import Booking, booking_nested

from models.subject import Subject, subject_schema, subjects_schema
from controllers.subject_controller import subjects_bp

time_slots_bp = Blueprint('time_slots', __name__, url_prefix='/time_slots')

# Gets all time-slots and returns their day and time.
@time_slots_bp.route('/', methods=['GET'])
def get_all_times():
    time_slots = TimeSlot.query.all()
    time_slots_list = [{'id': time_slot.id, 'Day': time_slot.time_slot_day, 'Time': time_slot.time_slot_time} for time_slot in time_slots]
    return jsonify({'timeslots': time_slots_list})

# Gets one time-slot and returns it day and time, and all booking details associated with that time.
@time_slots_bp.route('/<int:time_slot_id>')
def get_one_timeslot(time_slot_id):
    time_slot = TimeSlot.query.get(time_slot_id)

    if time_slot:
        # Fetch bookings associated with the time slot and include related attributes
        bookings = Booking.query.filter_by(time_slot_id=time_slot_id).options(
            joinedload(Booking.subject),  # Load data from the Subject model
            joinedload(Booking.room)  # Load data from the Room model
        ).all()
        # Serialize bookings using the custom schema with related attributes
        serialized_bookings = [booking_nested.dump(booking) for booking in bookings]
        return {
            "time slot": time_slot_schema.dump(time_slot),
            "bookings": serialized_bookings
        }
    else:
        return {"error": f"Time ID:{time_slot_id} not found"}, 404
