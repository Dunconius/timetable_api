from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError

from init import db, ma

# defining the Time_slot table
class TimeSlot(db.Model):
    __tablename__ = 'time_slots'

    # defining the native fields for this table
    time_slot_id = db.Column(db.String(5), primary_key=True)
    time_slot_day = db.Column(db.String)
    time_slot_time = db.Column(db.String)

    # back_populates for defining the interrelationships
    # classes = db.relationship('Class', back_populates='room')
    
class TimeSlotSchema(ma.Schema):
    class Meta:
        fields = ('time_slot_id', 'time_slot_day', 'time_slot_time')

time_slot_schema = TimeSlotSchema()
time_slots_schema = TimeSlotSchema(many=True)