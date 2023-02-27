"""Passenger API main functionality"""
import json
from flask_restful import Resource
from jsonschema import validate, exceptions
from flask import request, Response
from manifestapp.service import pass_get_bystatus, pass_get_byid
from manifestapp.models import Passenger
from manifestapp.logger import logger_setup

logger = logger_setup(__name__, '%(levelname)s::%(name)s::%(asctime)s'
                                '::%(message)s', 'apicalls.log', 'DEBUG')


error_msgs = [
    [{'message': 'PassengerID parameter should be an integer'}, 400],
    [{'message': 'Passenger data not found'}, 404],
    [{'message': 'Incorrect payload'}, 400],
    [{'message': 'Unknown error during record creation'}, 400]
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
        'dob': {'type': 'string',
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
            resp = pass_get_bystatus(status)
            if resp:
                logger.debug('Get all items with status %s. Status code: %s',
                             status, resp.status_code)

        elif pass_id.isdigit():
            resp = pass_get_byid(pass_id)
            if resp:
                logger.debug('Get item with id %s. Status code: %s ',
                             pass_id, resp.status_code)
            else:
                logger.error('Item with id %s not found. Status code: %s',
                             pass_id, error_msgs[1][1])
                resp = Response(json.dumps(error_msgs[1][0]), error_msgs[1][1],
                                mimetype='application/json')

        else:
            logger.error('GET method. Invalid pass_id parameter. Status code: %s',
                         error_msgs[0][1])
            resp = Response(json.dumps(error_msgs[0][0]), error_msgs[0][1],
                            mimetype='application/json')

        return resp

    def delete(self, pass_id):
        """DELETE method to delete passenger record"""

        if pass_id.isdigit():
            item = pass_get_byid(pass_id)
            if not item:
                logger.error('Item with id %s not found. Status code: %s',
                             pass_id, error_msgs[1][1])
                resp = Response(json.dumps(error_msgs[1][0]), error_msgs[1][1],
                                mimetype='application/json')

            else:
                resp = Passenger.fs_get_delete_put_post(pass_id)
                logger.debug('Item with id %s is deleted. Status code: %s',
                             pass_id, resp.status_code)

        else:
            logger.error('DELETE method. Invalid pass_id %s parameter. Status code: %s',
                         pass_id, error_msgs[0][1])
            resp = Response(json.dumps(error_msgs[0][0]), error_msgs[0][1],
                            mimetype='application/json')

        return resp

    def post(self, pass_id=None):
        """POST method to create passenger record"""

        payload = request.get_json()
        try:
            if not pass_id:
                validate(payload, schema=create_schema)
            else:
                validate(payload, schema=update_schema)

        except exceptions.ValidationError as error:
            logger.error('POST (create). Invalid payload. %s. Status code: 400', str(error))
            resp = Response(json.dumps(error_msgs[2][0]), error_msgs[2][1],
                            mimetype='application/json')

        else:
            if not pass_id:
                resp = Passenger.fs_get_delete_put_post()
                if resp.__class__.__name__ == 'Response':
                    logger.debug('Item is created. Status code: %s', resp.status_code)
                else:
                    logger.error('Error during item creation. %s. Status code: 400', resp)
                    resp = Response(json.dumps(error_msgs[3][0]), error_msgs[3][1],
                                    mimetype='application/json')

            elif pass_id.isdigit():
                item = pass_get_byid(pass_id)
                if not item:
                    logger.error('Item with id %s not found. Status code: %s',
                                 pass_id, error_msgs[1][1])
                    resp = Response(json.dumps(error_msgs[1][0]), error_msgs[1][1],
                                    mimetype='application/json')

                else:
                    resp = Passenger.fs_get_delete_put_post(pass_id)
                    logger.debug('Item with id %s is updated. Status code: %s',
                                 pass_id, resp.status_code)

            else:
                logger.error('POST (update). Invalid pass_id %s parameter. Status code: %s',
                             pass_id, error_msgs[0][1])
                resp = Response(json.dumps(error_msgs[0][0]), error_msgs[0][1],
                                mimetype='application/json')

        return resp
