from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError

from init import db, ma

# defining the Subject table
class Subject(db.Model):
    __tablename__ = 'subjects'

    # defining the native fields for this table
    id = db.Column(db.Integer, primary_key=True)
    subject_year = db.Column(db.String)
    subject_name = db.Column(db.String)

    # foreign fields --------------------------- table/column they come from
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    cohort_id = db.Column(db.Integer, db.ForeignKey('cohorts.id'))

    # Add the back-reference to booking
    bookings = db.relationship('Booking', back_populates='subject')
    
    # Define the relationship with Teacher
    teacher = db.relationship('Teacher', back_populates='subjects')
    cohort = db.relationship('Cohort', back_populates='subjects')
    
    
# defines the fields we want to be returned (deserialized) from the database
class SubjectSchema(ma.Schema):
    class Meta:
        fields = ('id', 'subject_year', 'subject_name')

class SubjectBookingSchema(ma.Schema):
    class Meta:
        fields = ('subject_year', 'subject_name')

subject_schema = SubjectSchema()
subjects_schema = SubjectSchema(many=True)
subject_booking_schema = SubjectBookingSchema()