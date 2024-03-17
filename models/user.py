from init import db, ma
from marshmallow import fields

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

# here we're making the User SCHEMA. Schemas define how data should be represented when it's transmitted over the network, usually in formats like JSON or XML.
class UserSchema(ma.Schema):

    class Meta:
        fields = ('user_id', 'name', 'is_admin')


user_schema = UserSchema() 
users_schema = UserSchema(many=True) 
