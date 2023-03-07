"""API module initiation"""
from flask_restful import Api
from .event_api import EventApi, EventSummaryApi
from .passenger_api import PassengerApi, PassengerSummaryApi

api = Api()

# API URLs
api.add_resource(PassengerApi,
                 '/passapi',
                 '/passapi/<pass_id>',
                 '/passapi/<pass_id>/<string:status>')

api.add_resource(PassengerSummaryApi,
                 '/passlistapi')

api.add_resource(EventApi,
                '/eventapi',
                '/eventapi/all',
                '/eventapi/all/<pass_id>',
                '/eventapi/all/<pass_id>/<datefrom>',
                '/eventapi/all/<pass_id>/<datefrom>/<dateto>',
                '/eventapi/<event_id>')

api.add_resource(EventSummaryApi,
                 '/eventsummaryapi')
