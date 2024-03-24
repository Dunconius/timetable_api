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
    
    __table_args__ = (
        db.UniqueConstraint(room_id, time_slot_id),
    )

# Define the Booking schema with nested fields for related models
class BookingSchema(ma.Schema):
    id = fields.Int(dump_only=True)  # Example: Include 'id' field

    subject_id = fields.Int(required=True)
    room_id = fields.Int(required=True)
    time_slot_id = fields.Int(required=True)

    # # Define nested fields for related models
    # room = fields.Nested('RoomSchema', only=('building_number', 'room_number'))
    # subject = fields.Nested('SubjectSchema', only=('subject_year', 'subject_name'))
    # time_slot = fields.Nested('TimeSlotSchema', only=('time_slot_day', 'time_slot_time'))

    class Meta:
        model = Booking
        include_fk = True  # Include foreign keys in the schema

# Create an instance of BookingSchema for single objects and multiple objects
booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)