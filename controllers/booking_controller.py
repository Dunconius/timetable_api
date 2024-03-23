from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload

from init import db

from models.booking import Booking, booking_schema, bookings_schema
from models.room import Room, room_schema, rooms_schema, room_booking_schema
from models.subject import Subject, subject_schema, subjects_schema, subject_booking_schema
from models.time_slot import TimeSlot, time_slot_schema, time_slots_schema, time_slot_booking_schema

bookings_bp = Blueprint('bookings', __name__, url_prefix='/bookings')

# get ALL bookings - GET (booking, subject, room, timeslot)
@bookings_bp.route('/', methods=['GET'])
def get_all_bookings():
    bookings = Booking.query.options(
        joinedload(Booking.room),  # Load data from the Room model
        joinedload(Booking.subject),  # Load data from the Subject model
        joinedload(Booking.time_slot)  # Load data from the TimeSlot model
    ).all()

    # Serialize all bookings using bookings_schema with related data included
    serialized_bookings = bookings_schema.dump(bookings)

    return jsonify({'bookings': serialized_bookings})

# get ONE booking
@bookings_bp.route('/<int:booking_id>')
def get_one_booking(booking_id):
    booking = Booking.query.options(
        joinedload(Booking.room),  # Load data from the Room model
        joinedload(Booking.subject),  # Load data from the Subject model
        joinedload(Booking.time_slot)  # Load data from the TimeSlot model
    ).get_or_404(booking_id)
    #booking = Booking.query.get_or_404(booking_id)
    #room = Room.query.get_or_404()

    return {
        "Booking ID": booking.id,
        "Room": room_schema.dump(booking.room) if booking.room else None,
        "Subject": subject_schema.dump(booking.subject) if booking.subject else None,
        "TimeSlot": time_slot_schema.dump(booking.time_slot) if booking.time_slot else None
    }


    