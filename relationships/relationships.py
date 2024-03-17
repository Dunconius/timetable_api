from init import db
from models.teacher import Teacher
from models.subject import Subject

# Define relationships after all models are defined
Teacher.subjects = db.relationship('Subject', back_populates='teacher')