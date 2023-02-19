from flask_restful import Resource
from manifestapp.models import Passenger
from manifestapp.logger import logger_setup
from jsonschema import validate
from flask import request

logger = logger_setup(__name__, '%(levelname)s::%(name)s::%(asctime)s::%(message)s', 'apicalls.log', 'DEBUG')


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
                logger.debug(f'Get all items with status {status}. Status code: {resp.status_code}')
            else:
                resp = Passenger.fs_get_delete_put_post()
                logger.debug(f'Get all items. Status code: {resp.status_code}')
            return resp

        else:
            if pass_id.isdigit():
                item = Passenger.query.get(pass_id)
                if not item:
                    logger.error(f'Item with id {pass_id} not found. Status code: {error_msgs[1][1]}')
                    return error_msgs[1][0], error_msgs[1][1]

                resp = Passenger.fs_json_list([item])
                logger.debug(f'Get item with id {pass_id}. Status code: {resp.status_code}')
                return resp

            else:
                logger.error(f'GET method. Invalid pass_id parameter. Status code: {error_msgs[0][1]}')
                return error_msgs[0][0], error_msgs[0][1]

    def delete(self, pass_id):
        """DELETE method to delete passenger record"""

        if pass_id.isdigit():
            resp = Passenger.fs_get_delete_put_post(pass_id)
            if resp.__class__.__name__ == 'Response':
                logger.debug(f'Item with id {pass_id} is deleted. Status code: {resp.status_code}')
            else:
                logger.error(f'Error during item deletion. {resp}. Status code: 400')

            return resp

        logger.error(f'DELETE method. Invalid pass_id parameter. Status code: {error_msgs[0][1]}')
        return error_msgs[0][0], error_msgs[0][1]

    def post(self, pass_id):
        """POST method to create passenger record"""

        if not pass_id:
            payload = request.get_json()
            try:
                validate(payload, schema=create_schema)
            except Exception as e:
                logger.error(f'POST method (create). Invalid payload. {str(e)}. Status code: 400')
                return 'Your payload is incorrect. ' + str(e.message), 400

            resp = Passenger.fs_get_delete_put_post()
            if resp.__class__.__name__ == 'Response':
                logger.debug(f'Item is created. Status code: {resp.status_code}')
            else:
                logger.error(f'Error during item creation. {resp}. Status code: 400')

        else:
            if pass_id.isdigit():
                payload = request.get_json()
                try:
                    validate(payload, schema=update_schema)
                except Exception as e:
                    logger.error(f'POST method (update). Invalid payload. {str(e)}. Status code: 400')
                    return 'Your payload is incorrect.' + str(e.message), 400

                resp = Passenger.fs_get_delete_put_post(pass_id)
                if resp.__class__.__name__ == 'Response':
                    logger.debug(f'Item with id {pass_id} is updated. Status code: {resp.status_code}')
                else:
                    logger.error(f'Error during update. {resp}. Status code: 400')

            else:
                logger.error(f'POST method (update). Invalid pass_id {pass_id} parameter. Status code: {error_msgs[0][1]}')
                return error_msgs[0][0], error_msgs[0][1]

        return resp


