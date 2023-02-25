"""API module initiation"""
from flask_restful import Api
from .event_api import EventApi
from .passenger_api import PassengerApi

api = Api()

# API URLs
api.add_resource(PassengerApi,
                 '/passapi',
                 '/passapi/<pass_id>',
                 '/passapi/<pass_id>/<string:status>')

api.add_resource(EventApi,
                '/eventapi',
                '/eventapi/all',
                '/eventapi/all/<pass_id>',
                '/eventapi/all/<pass_id>/<datefrom>',
                '/eventapi/all/<pass_id>/<datefrom>/<dateto>',
                '/eventapi/<event_id>')
