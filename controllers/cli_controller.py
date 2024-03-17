# CLI stands for command line interface (postgres commands)
# commands for dropping tables and seeding the database
from datetime import date

from flask import Blueprint

from init import db, bcrypt
from models.cohort import Cohort
from models.room import Room
from models.schedule import Schedule
from models.subject import Subject
from models.teacher import Teacher
from models.time_slot import TimeSlot
from models.user import User
# from models.comment import Comment

# now we create the blueprint
db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_tables():
    db.create_all()
    print("Tables create")

@db_commands.cli.command('drop')
def drop_tables():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command('seed')
def seed_tables():
    users = [
        User(
            email="admin@email.com",
            password=bcrypt.generate_password_hash('123456').decode('utf-8'),
            is_admin=True
        ),
        User(
            name="User",
            email="user@email.com",
            password=bcrypt.generate_password_hash('123456').decode('utf-8')
        )
    ]
    db.session.add_all(users)

    cohorts = [
        Cohort(
            cohort_id="01",
            year_group="2022"
        ),
        Cohort(
            cohort_id="02",
            year_group="2023"
        ),
        Cohort(
            cohort_id="03",
            year_group="2024"
        ),
    ]
    db.session.add_all(cohorts)

    rooms = [
        Room(
            room_id="G01"
        ),
        Room(
            room_id="G02"
        ),
        Room(
            room_id="G03"
        ),
    ]
    db.session.add_all(rooms)

    subjects = [
        Subject(
            subject_year="first year",
            subject_name="maths"
        ),
        Subject(
            subject_year="second year",
            subject_name="maths"
        ),
        Subject(
            subject_year="third year",
            subject_name="maths"
        ),
        Subject(
            subject_year="first year",
            subject_name="science"
        ),
        Subject(
            subject_year="second year",
            subject_name="science"
        ),
        Subject(
            subject_year="third year",
            subject_name="english"
        ),
    ]
    db.session.add_all(subjects)

    teachers = [
        Teacher(
            teacher_name="Dean"
        ),
        Teacher(
            teacher_name="Taylor"
        ),
        Teacher(
            teacher_name="Belinda"
        ),
        Teacher(
            teacher_name="Alice"
        ),
    ]
    db.session.add_all(teachers)

    time_slots = [
        TimeSlot(
            time_slot_day="Monday",
            time_slot_time="Morning"
        ),
        TimeSlot(
            time_slot_day="Monday",
            time_slot_time="Afternoon"
        ),
        TimeSlot(
            time_slot_day="Tuesday",
            time_slot_time="Morning"
        ),
        TimeSlot(
            time_slot_day="Tuesday",
            time_slot_time="Afternoon"
        ),
        TimeSlot(
            time_slot_day="Wednesday",
            time_slot_time="Morning"
        ),
        TimeSlot(
            time_slot_day="Wednesday",
            time_slot_time="Afternoon"
        ),
        TimeSlot(
            time_slot_day="Thursday",
            time_slot_time="Morning"
        ),
        TimeSlot(
            time_slot_day="Thursday",
            time_slot_time="Afternoon"
        ),
        TimeSlot(
            time_slot_day="Friday",
            time_slot_time="Morning"
        ),
        TimeSlot(
            time_slot_day="Friday",
            time_slot_time="Afternoon"
        ),
    ]
    db.session.add_all(time_slots)

    
    # seed schedules LAST as it has a lot of foreign keys that must be seeded first
    schedules = [
        Schedule(
            
        ),
    ]
    db.session.add_all(schedules)

    db.session.commit()

    print("Tables seeded")