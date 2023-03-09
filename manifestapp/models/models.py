"""Data model definition for the application"""
from flask_serialize import FlaskSerialize
from flask_login import UserMixin
from password_strength import PasswordPolicy
from manifestapp.extensions import db, login_manager, app_bcrypt


FsMixin = FlaskSerialize(db)

class Event(db.Model, FsMixin):
    """Class model to store event data"""

    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    passengerID = db.Column(db.Integer, db.ForeignKey('passengers.id'), nullable=False)
    geo_location = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(90), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    other_pass = db.Column(db.String(100))
    comments = db.Column(db.String(140))

    # serializer fields
    __fs_create_fields__ = __fs_update_fields__ = ['date', 'passengerID', 'geo_location',
                                                   'description', 'status', 'other_pass',
                                                   'comments']

class Passenger(db.Model, FsMixin):
    """Class model to store passenger data"""

    __tablename__ = 'passengers'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(45), nullable=False)
    lname = db.Column(db.String(45), nullable=False)
    seatno = db.Column(db.String(3), nullable=False)
    address = db.Column(db.String(100))
    dob = db.Column(db.Date)
    status = db.Column(db.String(10), nullable=False)
    comments = db.Column(db.String(140))

    # serializer fields
    __fs_create_fields__ = __fs_update_fields__ = ['fname', 'lname',
                                                   'seatno', 'address', 'dob', 'status', 'comments']


policy = PasswordPolicy.from_names(
    length=8,  # min length: 8
    uppercase=1,  # need min. 1 uppercase letters
    numbers=1,  # need min. 1 digits
)

@login_manager.user_loader
def load_user(user_id):
    """User callback utility function"""
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    """Class model to store users data"""

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), nullable=False, unique=True)
    pwd_hash = db.Column(db.String(60), nullable=False)
    is_active = db.Column(db.Integer, nullable=False, default=1)  #1 is active, 0 is inactive

    @property
    def password(self):
        """User attribute to set hashed password"""
        return self.pwd_hash

    @password.setter
    def password(self, plain_text_pwd):
        """User attribute setter for hashed password"""
        self.pwd_hash = app_bcrypt.generate_password_hash(plain_text_pwd).decode('utf-8')

    def check_pwd(self, attempted_pwd):
        """User password method check. Checking of string vs hashed password stored in the DB"""
        return app_bcrypt.check_password_hash(self.pwd_hash, attempted_pwd)
