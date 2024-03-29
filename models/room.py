from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError

from init import db, ma

# defining the Rooms table
class Room(db.Model):
    __tablename__ = 'rooms'

    # defining the native fields for this table
    id = db.Column(db.Integer, primary_key=True)
    building_number = db.Column(db.String(1))
    room_number = db.Column(db.Integer)

    # defining the interrelationships
    bookings = db.relationship('Booking', back_populates='room', cascade='all, delete-orphan')
    
class RoomSchema(ma.Schema):
    class Meta:
        fields = ('id', 'building_number', 'room_number')

class RoomBookingSchema(ma.Schema):
    class Meta:
        fields = ('building_number', 'room_number')

room_schema = RoomSchema()
rooms_schema = RoomSchema(many=True)
room_booking_schema = RoomBookingSchema()