from manifestapp import db

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    passengerID = db.Column(db.Integer, db.ForeignKey('passenger.id'), nullable=False)
    geo_location = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(90), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    other_pass = db.Column(db.String(100))
    comments = db.Column(db.String(140))


class Passenger(db.Model):
    __tablename__ = 'passengers'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(45), nullable=False)
    lname = db.Column(db.String(45), nullable=False)
    seatno = db.Column(db.String(3), nullable=False)
    address = db.Column(db.String(100))
    dob = db.Column(db.Date)
    status = db.Column(db.String(10), nullable=False)
    comments = db.Column(db.String(140))