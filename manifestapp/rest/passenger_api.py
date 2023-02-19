"""Passenger API main functionality"""
from flask_restful import Resource
from jsonschema import validate, exceptions
from flask import request
from manifestapp.models import Passenger
from manifestapp.logger import logger_setup

logger = logger_setup(__name__, '%(levelname)s::%(name)s::%(asctime)s'
                                '::%(message)s', 'apicalls.log', 'DEBUG')


error_msgs = [
    [{'message': 'PassengerID parameter should be an integer'}, 400],
    [{'message': 'Passenger data not found'}, 404],
]

create_schema = {
    'type': 'object',
    'properties': {
        'fname': {'type': 'string',
                 'maxLength': 45},
        'lname': {'type': 'string',
                  'maxLength': 45},
        'seatno': {'type': 'string',
                 'pattern': '^[0-9]{2}[A-Z]$'},
        'address': {'type': 'string',
                  'maxLength': 100},
        'date': {'type': 'string',
                 'format': 'date'},
        'status': {'type': 'string',
                   'pattern': 'unknown|live|dead'},
        'comments': {'type': 'string',
                     'maxLength': 140}
    },
    'additionalProperties': False,
    'required': ['fname', 'lname', 'seatno', 'status']
}

update_schema = {}
update_schema = create_schema.copy()
update_schema.pop('required')


class PassengerApi(Resource):
    """API class for passengers data"""

    def get(self, pass_id='all', status=None):
        """GET method to retrieve passengers data"""

        if pass_id == 'all':
            if status:
                resp = Passenger.fs_get_delete_put_post(prop_filters={'status': status})
                logger.debug('Get all items with status %s. Status code: %s',
                             status, resp.status_code)
            else:
                resp = Passenger.fs_get_delete_put_post()
                logger.debug('Get all items. Status code: %s', resp.status_code)
            return resp

        if pass_id.isdigit():
            item = Passenger.query.get(pass_id)
            if not item:
                logger.error('Item with id %s not found. Status code: %s',
                             pass_id, error_msgs[1][1])
                return error_msgs[1][0], error_msgs[1][1]

            resp = Passenger.fs_json_list([item])
            logger.debug('Get item with id %s. Status code: %s ',
                         pass_id, resp.status_code)
            return resp

        logger.error('GET method. Invalid pass_id parameter. Status code: %s',
                     error_msgs[0][1])
        return error_msgs[0][0], error_msgs[0][1]

    def delete(self, pass_id):
        """DELETE method to delete passenger record"""

        if pass_id.isdigit():
            resp = Passenger.fs_get_delete_put_post(pass_id)
            if resp.__class__.__name__ == 'Response':
                logger.debug('Item with id %s is deleted. Status code: %s',
                             pass_id, resp.status_code)
            else:
                logger.error('Error during item deletion. %s. Status code: 400', resp)

            return resp

        logger.error('DELETE method. Invalid pass_id %s parameter. Status code: %s',
                     pass_id, error_msgs[0][1])
        return error_msgs[0][0], error_msgs[0][1]

    def post(self, pass_id):
        """POST method to create passenger record"""

        if not pass_id:
            payload = request.get_json()
            try:
                validate(payload, schema=create_schema)
            except exceptions.ValidationError as error:
                logger.error('POST (create). Invalid payload. %s. Status code: 400', str(error))
                return 'Your payload is incorrect. ' + str(error), 400

            resp = Passenger.fs_get_delete_put_post()
            if resp.__class__.__name__ == 'Response':
                logger.debug('Item is created. Status code: %s', resp.status_code)
            else:
                logger.error('Error during item creation. %s. Status code: 400', resp)

        else:
            if pass_id.isdigit():
                payload = request.get_json()
                try:
                    validate(payload, schema=update_schema)
                except exceptions.ValidationError as error:
                    logger.error('POST (update). Invalid payload. %s. Status code: 400', str(error))
                    return 'Your payload is incorrect.' + str(error), 400

                resp = Passenger.fs_get_delete_put_post(pass_id)
                if resp.__class__.__name__ == 'Response':
                    logger.debug('Item with id %s is updated. Status code: %s',
                                 pass_id, resp.status_code)
                else:
                    logger.error('Error during update. %s. Status code: 400', resp)

            else:
                logger.error('POST (update). Invalid pass_id %s parameter. Status code: %s',
                             pass_id, error_msgs[0][1])
                return error_msgs[0][0], error_msgs[0][1]

        return resp
