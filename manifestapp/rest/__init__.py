#
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
                '/eventapi/<event_id>',
                '/eventapi/<event_id>/<datefrom>',
                '/eventapi/<event_id>/<datefrom>/<dateto>')