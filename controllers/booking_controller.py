from flask import Blueprint, request, jsonify

from init import db

from models.booking import Booking, booking_schema, bookings_schema

bookings_bp = Blueprint('bookings', __name__, url_prefix='/bookings')

# get ALL bookings - GET (booking, subject, room, timeslot)
@bookings_bp.route('/', methods=['GET'])
def get_all_bookings():
    bookings = Booking.query.all()
    bookings_list = [{'id': booking.id} for booking in bookings]
    return jsonify({'bookings': bookings_list})

# get ONE booking
@bookings_bp.route('/<int:booking_id>')
def get_one_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    return {
        "Booking": booking_schema.dump(booking)
    }