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
    # seeding tables that don't require foreign keys
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
            year_group="2022"
        ),
        Cohort(
            year_group="2023"
        ),
        Cohort(
            year_group="2024"
        ),
    ]
    db.session.add_all(cohorts)

    rooms = [
        Room(
            room_id="G01",
            building_number="G",
            room_number="01"
        ),
        Room(
            room_id="G02",
            building_number="G",
            room_number="02"
        ),Room(
            room_id="G03",
            building_number="G",
            room_number="03"
        ),
    ]
    db.session.add_all(rooms)

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
            time_slot_id=1,
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
    # committing all seeds that don't require foreign keys
    db.session.commit()

    # seeding first tier of foreign key tables
    subjects = [
        Subject(
            subject_year="first year",
            subject_name="maths",
            cohort_id=cohorts[0].cohort_id,
            teacher_id=teachers[0].teacher_id
        )
    ]
    db.session.add_all(subjects)
    # committing first tier of foreign key tables
    db.session.commit()

    # seeding second tier of foreign key tables
    schedules = [
        Schedule(
            subject_id=subjects[0].subject_id,
            room_id='G01',
            time_slot_id=[0].time_slot_id
        )
    ]
    db.session.add_all(schedules)
    # committing second tier of foreign key tables
    db.session.commit()

    print("Tables seeded")