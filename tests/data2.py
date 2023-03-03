"""Data for testing"""
from manifestapp.models import Event, Passenger
import datetime

t_e1 = Event(
    date=datetime.date(2022, 12, 1),
    passengerID=1,
    geo_location='123.3, 20.34',
    description='test1',
    status='unknown',
    other_pass='',
    comments='good')

t_e2 = Event(
    date=datetime.date(2022, 12, 15),
    passengerID=2,
    geo_location='100.3, 20.34',
    description='test2',
    status='success',
    other_pass='1',
    comments='bad')

t_e3 = Event(
    date=datetime.date(2023, 1, 15),
    passengerID=1,
    geo_location='90.3, 20.34',
    description='test3',
    status='failure',
    other_pass='2',
    comments='ugly')


t_p1 = Passenger(
    fname='tester',
    lname='testerson',
    seatno='10A',
    address='place1',
    dob=datetime.date(2000, 1, 1),
    status='live',
    comments='nice guy')

t_p2 = Passenger(
    fname='test',
    lname='testersonny',
    seatno='01B',
    address='place2',
    dob=datetime.date(1990, 1, 1),
    status='dead',
    comments='bad guy')

t_p3 = Passenger(
    fname='test',
    lname='testersonny',
    seatno='01B',
    address='place2',
    dob=datetime.date(1995, 1, 1),
    status='unknown',
    comments='super cool guy')

t_events = [t_e1, t_e2, t_e3]
t_passes = [t_p1, t_p2, t_p3]
t_all = [t_events, t_passes]
