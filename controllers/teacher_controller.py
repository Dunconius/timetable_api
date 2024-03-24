from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from sqlalchemy import asc

from init import db
from models.teacher import Teacher, teacher_schema
from models.subject import Subject, subject_schema
from models.booking import Booking, booking_schema

#bits for admin authorization
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from controllers.auth_utils import check_admin

teachers_bp = Blueprint('teachers', __name__, url_prefix='/teachers')

# Gets all teachers and returns their id and name.
@teachers_bp.route('/', methods=['GET'])
def get_all_teachers():
    teachers = Teacher.query.all()
    teachers_list = [{"id": teacher.id, "name": teacher.teacher_name} for teacher in teachers]
    return jsonify({"teachers": teachers_list})

# Gets one teacher and returns all the subjects their assigned to and their bookings details. Requires the teacher_id in dynamic route
@teachers_bp.route('/<int:teacher_id>')
def get_one_teacher(teacher_id):
    teacher = Teacher.query.get(teacher_id)

    if teacher:
        subjects = [subject_schema.dump(subject) for subject in teacher.subjects]

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
    else:
        return {"error": f"Teacher ID:{teacher_id} not found"}, 404

    
# Adds a new teacher. Requires admin auth. Teacher details required in the body request
@teachers_bp.route('/', methods=['POST'])
@jwt_required()
@check_admin
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

# Deletes a teacher. Requires admin auth. Teacher_id required in dynamic route
@teachers_bp.route('/<int:teacher_id>', methods=['DELETE'])
@jwt_required()
@check_admin
def delete_teacher(teacher_id):
    teacher = Teacher.query.get(teacher_id)

    if teacher:
        db.session.delete(teacher)
        db.session.commit()
        return {'message': f'Teacher ID:{teacher.id} Name:{teacher.teacher_name} deleted successfully'}
    else:
        return {'error': f'Teacher ID:{teacher_id} not found'}, 404

# Updates an existing teacher. Requires admin auth. Teacher_id required in dynamic route. Teacher details required in the body request 
@teachers_bp.route('/<int:teacher_id>', methods=['PUT', 'PATCH'])
@jwt_required()
@check_admin
def update_teacher(teacher_id):
    body_data = teacher_schema.load(request.get_json(), partial=True)
    teacher = Teacher.query.get(teacher_id)

    if teacher:
        # The teacher exists, so update the attributes if they are provided in the request
        teacher.teacher_name = body_data.get('teacher_name') or teacher.teacher_name
        db.session.commit()

        # Construct the success message after the update
        success_message = f"Teacher '{teacher.teacher_name}' updated successfully!"

        return jsonify({
            "message": success_message,
            "teacher": teacher_schema.dump(teacher)
        })
    else:
        # The teacher doesn't exist, return the custom error message
        return {'error': f'Teacher ID:{teacher_id} not found'}, 404




