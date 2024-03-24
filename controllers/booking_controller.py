from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from sqlalchemy import asc
from sqlalchemy.exc import IntegrityError

from init import db

from models.booking import Booking, booking_schema, bookings_schema
from models.room import Room, room_schema, rooms_schema, room_booking_schema
from models.subject import Subject, subject_schema, subjects_schema, subject_booking_schema
from models.time_slot import TimeSlot, time_slot_schema, time_slots_schema, time_slot_booking_schema

bookings_bp = Blueprint('bookings', __name__, url_prefix='/bookings')

# get ALL bookings - GET (booking, subject, room, timeslot)
@bookings_bp.route('/', methods=['GET'])
def get_all_bookings():
    # Query all bookings and order them by booking_id
    bookings = Booking.query.order_by(asc(Booking.id)).options(
        joinedload(Booking.room),  # Load data from the Room model
        joinedload(Booking.subject),  # Load data from the Subject model
        joinedload(Booking.time_slot)  # Load data from the TimeSlot model
    ).all()

    # Serialize all bookings using bookings_schema with related data included
    serialized_bookings = bookings_schema.dump(bookings)

    return jsonify({'bookings': serialized_bookings})

# get ONE booking MAKE THIS RETURN THE SUBJECT NAME, ROOM NUMBER, AND TIME INSTEAD OF IDs
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

# ADD a booking
@bookings_bp.route('/', methods=['POST'])
def add_booking():
    body_data = booking_schema.load(request.get_json())

    room_id = body_data.get('room_id')
    time_slot_id = body_data.get('time_slot_id')

    # Check if a booking with the same room_id and time_slot_id already exists
    existing_booking = Booking.query.filter_by(room_id=room_id, time_slot_id=time_slot_id).first()
    if existing_booking:
        return jsonify({'error': 'Booking already exists for this room and time slot.'}), 400

    booking = Booking(
        subject_id=body_data.get('subject_id'),
        room_id=room_id,
        time_slot_id=time_slot_id
    )

    db.session.add(booking)
    db.session.commit()

    # Fetch the related objects from the database
    room = Room.query.get(booking.room_id)
    subject = Subject.query.get(booking.subject_id)
    time_slot = TimeSlot.query.get(booking.time_slot_id)

    # Construct the response JSON including related model information
    response_data = {
        "booking": booking_schema.dump(booking),
        "room": room_schema.dump(room),
        "subject": subject_schema.dump(subject),
        "time_slot": time_slot_schema.dump(time_slot)
    }

    return jsonify(response_data), 201

# DELETE a booking
@bookings_bp.route('/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    stmt = db.select(Booking).where(Booking.id == booking_id)
    booking = db.session.scalar(stmt)

    if booking:
        db.session.delete(booking)
        db.session.commit()
        return {'message': f'Booking ID:{booking.id} deleted successfully'}
    else:
        return {'error': f'Booking ID:{booking_id} not found'}, 404

# UPDATE a booking
# @bookings_bp.route('/<int:booking_id>', methods=['PUT', 'PATCH'])
# def update_booking(booking_id):
#     body_data = booking_schema.load(request.get_json(), partial=True)
#     stmt = db.select(Booking).filter_by(id=booking_id)
#     booking = db.session.scalar(stmt)

#     if booking:
#         booking.subject_id = body_data.get('subject_id') or booking.subject_id
#         booking.room_id = body_data.get('room_id') or booking.room_id
#         booking.time_slot_id = body_data.get('time_slot_id') or booking.time_slot_id
#         db.session.commit()
#         return booking_schema.dump(booking)
#     else:
#         return {'error': f'Booking ID:{booking_id} not found'}, 404
    
@bookings_bp.route('/<int:booking_id>', methods=['PUT', 'PATCH'])
def update_booking(booking_id):
    body_data = booking_schema.load(request.get_json(), partial=True)
    stmt = db.select(Booking).filter_by(id=booking_id)
    booking = db.session.scalar(stmt)

    if booking:
        # Check if subject_id, room_id, and time_slot_id exist before updating
        subject_id = body_data.get('subject_id')
        room_id = body_data.get('room_id')
        time_slot_id = body_data.get('time_slot_id')

        if subject_id and not db.session.query(Subject.id).filter_by(id=subject_id).scalar():
            return {'error': f'Subject ID:{subject_id} not found'}, 404

        if room_id and not db.session.query(Room.id).filter_by(id=room_id).scalar():
            return {'error': f'Room ID:{room_id} not found'}, 404

        if time_slot_id and not db.session.query(TimeSlot.id).filter_by(id=time_slot_id).scalar():
            return {'error': f'Time Slot ID:{time_slot_id} not found'}, 404

        # Update the booking
        booking.subject_id = subject_id or booking.subject_id
        booking.room_id = room_id or booking.room_id
        booking.time_slot_id = time_slot_id or booking.time_slot_id

        try:
            db.session.commit()
            return booking_schema.dump(booking)
        except IntegrityError as e:
            db.session.rollback()
            return {'error': str(e)}, 400  # Handle integrity constraint violation
    else:
        return {'error': f'Booking ID:{booking_id} not found'}, 404
    