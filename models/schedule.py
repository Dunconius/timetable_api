from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError

from init import db, ma

# defining the Schedule table
class Schedule(db.Model):
    __tablename__ = 'schedules'

    # defining the native fields for this table
    schedule_id = db.Column(db.Integer, primary_key=True)
    
    # foreign fields --------------------------- table/column they come from
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.subject_id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.room_id'), nullable=False)
    time_slot_id = db.Column(db.Integer, db.ForeignKey('time_slots.time_slot_id'), nullable=False)

    # interrelationships --- From class name --------- to this class
    subject = db.relationship('Subject', back_populates='schedules')
    room = db.relationship('Room', back_populates='schedules')
    time_slot = db.relationship('Time_slot', back_populates='schedules')
    
# defines the fields we want to be returned (deserialized) from the database
class ScheduleSchema(ma.Schema):
    
    teacher = fields.Nested('TeacherSchema', only = ['teacher_name'])
    
    class Meta:
        fields = ('schedule_id', 'subject', 'room', 'time_slot')

schedule_schema = ScheduleSchema()
schedules_schema = ScheduleSchema(many=True)