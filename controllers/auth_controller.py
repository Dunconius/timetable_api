from datetime import timedelta

from flask import Blueprint, request, jsonify, abort
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from psycopg2 import errorcodes

from init import db, bcrypt
from models.user import User, user_schema
from controllers.auth_utils import check_admin

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# login for a user. Returns their email, admin status, and auth token
@auth_bp.route('/login', methods=['POST'])
def auth_login():
    body_data = request.get_json()
    stmt = db.select(User).filter_by(email=body_data.get('email'))
    user = db.session.scalar(stmt)
    if user and bcrypt.check_password_hash(user.password, body_data.get('password')):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return {'email': user.email, 'token': token, 'is_admin': user.is_admin}
    else:
        return {'error': 'Invalid email or password'}, 401
    
# test route to confirm check_admin function works as intended
@auth_bp.route('/test', methods=['GET'])
@jwt_required()
@check_admin
def test_admin():
    return jsonify({'message': 'You are an admin!'})