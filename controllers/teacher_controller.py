from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from sqlalchemy import asc

from init import db
from models.teacher import Teacher, teacher_schema
from models.subject import Subject, subject_schema
from models.booking import Booking, booking_schema

teachers_bp = Blueprint('teachers', __name__, url_prefix='/teachers')

# get ALL teachers - GET
@teachers_bp.route('/', methods=['GET'])
def get_all_teachers():
    teachers = Teacher.query.all()
    teachers_list = [{"id": teacher.id, "name": teacher.teacher_name} for teacher in teachers]
    return jsonify({"teachers": teachers_list})

# get ONE teacher (dynamic route), show the classes they're teaching, and the times/rooms for those classes - GET
@teachers_bp.route('/<int:teacher_id>')
def get_one_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)

    # Access the related subjects through the teacher's subjects relationship
    subjects = [subject_schema.dump(subject) for subject in teacher.subjects]

    # Create a list to store subject details including rooms and times
    subjects_with_details = []

    for subject in subjects:
        subject_id = subject['id']
        bookings = Booking.query.filter_by(subject_id=subject_id).options(
            joinedload(Booking.room),
            joinedload(Booking.time_slot)
        ).order_by(
            asc(Booking.time_slot_id) # sort bookings by time
        ).all()

        # Create a list to store booking details
        bookings_details = []
        for booking in bookings:
            booking_details = {
                "id": booking.id,
                "room": {
                    "building_number": booking.room.building_number,
                    "room_number": booking.room.room_number
                },
                "time_slot": {
                    "time_slot_day": booking.time_slot.time_slot_day,
                    "time_slot_time": booking.time_slot.time_slot_time
                }
            }
            bookings_details.append(booking_details)

        # Append subject details along with bookings details
        subject_with_details = {
            "id": subject['id'],
            "subject_year": subject['subject_year'],
            "subject_name": subject['subject_name'],
            "bookings": bookings_details
        }
        subjects_with_details.append(subject_with_details)

    return jsonify({
        "teacher": teacher_schema.dump(teacher),
        "Assigned to subjects": subjects_with_details
    })

    
# create teacher (admin only) - POST # ADD IN ADMIN ACCESS ONLY!!!!!!!!!!!!
@teachers_bp.route('/', methods=['POST'])
def add_teacher():
    body_data = teacher_schema.load(request.get_json())

    teacher = Teacher(
        teacher_name = body_data.get('teacher_name')
    )
    db.session.add(teacher)
    db.session.commit()

    success_message = f"Teacher '{teacher.teacher_name}' added successfully!"
    
    return jsonify({
        "message": success_message,
        "teacher": teacher_schema.dump(teacher)
     }), 201

# delete teacher (admin only) - DELETE # ADD IN ADMIN ACCESS ONLY!!!!!!!!!!!!
@teachers_bp.route('/<int:teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    stmt = db.select(Teacher).where(Teacher.id == teacher_id)
    teacher = db.session.scalar(stmt)

    if teacher:
        db.session.delete(teacher)
        db.session.commit()
        return {'message': f'Teacher ID:{teacher.id} Name:{teacher.teacher_name} deleted successfully'}
    else:
        return {'error': f'Teacher ID:{teacher_id} not found'}, 404

# edit teacher (admin only) - PUT, PATCH # ADD IN ADMIN ACCESS ONLY!!!!!!!!!!!!
@teachers_bp.route('/<int:teacher_id>', methods=['PUT', 'PATCH'])
def update_teacher(teacher_id):
    body_data = teacher_schema.load(request.get_json(), partial=True)
    stmt = db.select(Teacher).filter_by(id=teacher_id)
    teacher = db.session.scalar(stmt)

    success_message = f"Teacher '{teacher.teacher_name}' updated successfully!"

    if teacher:
        teacher.teacher_name = body_data.get('teacher_name') or teacher.teacher_name
        db.session.commit()
        return jsonify({
            "message": success_message,
            "teacher": teacher_schema.dump(teacher)
        })
    else:
        return {'error': f'Teacher ID:{teacher_id} not found'}, 404




