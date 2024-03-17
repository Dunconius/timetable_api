from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError

from init import db, ma

# defining the Rooms table
class Room(db.Model):
    __tablename__ = 'rooms'

    # defining the native fields for this table
    room_id = db.Column(db.String(5), primary_key=True)
    building_number = db.Column(db.String(1))
    room_number = db.Column(db.Integer)


    # defining the interrelationships
    # classes = db.relationship('Class', back_populates='room')
    
class RoomSchema(ma.Schema):
    class Meta:
        fields = ('room_id', 'building_number', 'room_number')

room_schema = RoomSchema()
rooms_schema = RoomSchema(many=True)