# from flask import abort, current_user

# def check_admin():
#     if not current_user.is_admin:
#         abort(403)  # Forbidden error if the user is not an admin

from datetime import date
import functools

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.user import User

def check_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        # if user is admin
        if user.is_admin:
            # continue and run decorated function
            return fn(*args, **kwargs)
        # else
        else:
            # return an error
            return {"error": "Not authorized user"}, 403
    return wrapper