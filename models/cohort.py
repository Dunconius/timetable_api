from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError

from init import db, ma

# defining the Cohort table
class Cohort(db.Model):
    __tablename__ = 'cohorts'

    # defining the native fields for this table
    cohort_id = db.Column(db.Integer, primary_key=True)
    year_group = db.Column(db.String)
    
    # defining the interrelationships
    # classes = db.relationship('Class', back_populates='room')
    
# defines the fields we want to be returned (deserialized) from the database
class CohortSchema(ma.Schema):
    class Meta:
        fields = ('cohort_id', 'year_group')

cohort_schema = CohortSchema()
cohorts_schema = CohortSchema(many=True)