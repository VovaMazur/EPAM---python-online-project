"""Data model definition for the application"""
from flask_serialize import FlaskSerialize
from manifestapp.db_instance import db

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
