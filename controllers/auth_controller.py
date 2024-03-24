from datetime import timedelta

from flask import Blueprint, request, jsonify, abort # current_user
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from psycopg2 import errorcodes

from init import db, bcrypt
from models.user import User, user_schema
from controllers.auth_utils import check_admin

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST']) #auth/login
def auth_login():
    # get the request body
    body_data = request.get_json()
    # from the User database, find the user with that email
    stmt = db.select(User).filter_by(email=body_data.get("email"))
    user = db.session.scalar(stmt)
    # if user exists and password is correct
    if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
        # create jwt (JSON Web Token)
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        # return the token along with the user information
        return {"email": user.email, "token": token, "is_admin": user.is_admin}
    # else
    else:
        # return error
        return {"error": "Invalid email or password"}, 401 # The 401 Unauthorized.
    
@auth_bp.route('/test', methods=['GET'])
@jwt_required()
@check_admin
def test_admin():
    return jsonify({'message': 'You are an admin!'})