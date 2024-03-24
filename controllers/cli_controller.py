from datetime import date

from flask import Blueprint

from init import db, bcrypt
from models.cohort import Cohort
from models.room import Room
from models.booking import Booking
from models.subject import Subject
from models.teacher import Teacher
from models.time_slot import TimeSlot
from models.user import User

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_tables():
    print("Creating tables...")
    db.create_all()
    print("Tables create")

@db_commands.cli.command('drop')
def drop_tables():
    print("Dropping tables...")
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command('seed')
def seed_tables():
    print("Seeding tables...")
    # seeding tables that don't require foreign keys first
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
            building_number="G",
            room_number="01"
        ),
        Room(
            building_number="G",
            room_number="02"
        ),Room(
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
            cohort_id=cohorts[0].id,
            teacher_id=teachers[0].id
        ),
        Subject(
            subject_year="second year",
            subject_name="maths",
            cohort_id=cohorts[1].id,
            teacher_id=teachers[2].id
        ),
        Subject(
            subject_year="first year",
            subject_name="science",
            cohort_id=cohorts[0].id,
            teacher_id=teachers[1].id
        )
    ]
    db.session.add_all(subjects)
    # committing first tier of foreign key tables
    db.session.commit()

    # seeding second tier of foreign key tables
    bookings = [
        Booking(
            subject_id=subjects[0].id,
            room_id=rooms[0].id,
            time_slot_id=time_slots[0].id
        ),
        Booking(
            subject_id=subjects[1].id,
            room_id=rooms[1].id,
            time_slot_id=time_slots[1].id
        ),
        Booking(
            subject_id=subjects[2].id,
            room_id=rooms[2].id,
            time_slot_id=time_slots[2].id
        )
    ]
    db.session.add_all(bookings)
    # committing second tier of foreign key tables
    db.session.commit()

    print("Tables seeded")