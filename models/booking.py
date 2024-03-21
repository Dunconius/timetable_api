from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError

from init import db, ma

# defining the booking table
class Booking(db.Model):
    __tablename__ = 'bookings'

    # defining the native fields for this table
    id = db.Column(db.Integer, primary_key=True)
    
    # foreign fields --------------------------- table/column they come from
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    time_slot_id = db.Column(db.Integer, db.ForeignKey('time_slots.id'))

    # interrelationships --- From class name --------- to this class
    subject = db.relationship('Subject', back_populates='bookings')
    room = db.relationship('Room', back_populates='bookings')
    time_slot = db.relationship('TimeSlot', back_populates='bookings')
    
class BookingSchema(ma.Schema):
    class Meta:
        model = Booking
        include_fk = True  # Include foreign keys in the schema

booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)