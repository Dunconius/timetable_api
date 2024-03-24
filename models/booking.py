from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError
from sqlalchemy.orm import joinedload

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

    class Meta:
        model = Booking
        include_fk = True  # Include foreign keys in the schema

# Defines a booking schema with more user friendly data for use in nested objects
class BookingNestedSchema(ma.Schema):
    id = fields.Int()
    building_number = fields.Str(attribute="room.building_number") 
    room_number = fields.Str(attribute="room.room_number") 
    subject_name = fields.Str(attribute="subject.subject_name")  
    time_slot_day = fields.Str(attribute="time_slot.time_slot_day")  
    time_slot_time = fields.Str(attribute="time_slot.time_slot_time")  

booking_schema = BookingSchema()        

# Create an instance of BookingSchema for single objects and multiple objects
booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)
booking_nested = BookingNestedSchema()