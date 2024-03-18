from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError

from init import db, ma

# defining the Schedule table
class Schedule(db.Model):
    __tablename__ = 'schedules'

    # defining the native fields for this table
    id = db.Column(db.Integer, primary_key=True)
    
    # foreign fields --------------------------- table/column they come from
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    time_slot_id = db.Column(db.Integer, db.ForeignKey('time_slots.id'))

    # interrelationships --- From class name --------- to this class
    subject = db.relationship('Subject', back_populates='schedules')
    room = db.relationship('Room', back_populates='schedules')
    time_slot = db.relationship('TimeSlot', back_populates='schedules')
    
class ScheduleSchema(ma.Schema):
    class Meta:
        model = Schedule
        include_fk = True  # Include foreign keys in the schema

schedule_schema = ScheduleSchema()
schedules_schema = ScheduleSchema(many=True)