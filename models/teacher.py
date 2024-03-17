from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError

from init import db, ma

# defining the Teachers table
class Teacher(db.Model):
    __tablename__ = 'teachers'

    # defining the native fields for this table
    teacher_id = db.Column(db.Integer, primary_key=True)
    teacher_name = db.Column(db.String(100))
    
    # defining the interrelationships
    # subjects = db.relationship('Subject', back_populates='teacher', cascade='all, delete-orphan')
    
# defines the fields we want to be returned (deserialized) from the database
class TeacherSchema(ma.Schema):
    class Meta:
        fields = ('teacher_id', 'teacher_name')

teacher_schema = TeacherSchema()
teachers_schema = TeacherSchema(many=True)