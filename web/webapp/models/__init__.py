import datetime
from flask_security import UserMixin, RoleMixin
from ..database import db

roles_users = db.Table('roles_users',
    db.Column('user_id',db.Integer(),db.ForeignKey('user.id')),
    db.Column('role_id',db.Integer(),db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    confirmed_at = db.Column(db.DateTime())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role',secondary='roles_users',backref=db.backref('users',lazy="dynamic"))
    

    def get(self, attribute_name):
        """
        A generic getter function to retrieve the value of a user attribute.

        :param attribute_name: The name of the attribute to retrieve.
        :return: The value of the specified attribute, or None if the attribute doesn't exist.
        """
        return getattr(self, attribute_name, None)

