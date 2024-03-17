from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError

from init import db, ma

# defining the Subject table
class Subject(db.Model):
    __tablename__ = 'subjects'

    # defining the native fields for this table
    subject_id = db.Column(db.Integer, primary_key=True)
    subject_year = db.Column(db.String)
    subject_name = db.Column(db.String)
    
    # foreign fields --------------------------- table/column they come from
    cohort_id = db.Column(db.Integer, db.ForeignKey("cohorts.cohort_id"))
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.teacher_id"))

    # interrelationships --- From table name --------- to this table
    cohort = db.relationship('Cohort', back_populates='subjects')
    teacher = db.relationship('Teacher', back_populates='subjects')
    
    schedules = db.relationship('Schedule', back_populates='subject', cascade='all, delete-orphan')  # Assuming a Subject can have multiple Schedules
    
# defines the fields we want to be returned (deserialized) from the database
class SubjectSchema(ma.Schema):
    class Meta:
        fields = ('subject_id', 'subject_year', 'subject_name')

subject_schema = SubjectSchema()
subjects_schema = SubjectSchema(many=True)