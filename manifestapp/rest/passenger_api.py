from flask_restful import Resource
from manifestapp.models import Passenger
from manifestapp.logger import logger_setup

logger = logger_setup(__name__, '%(levelname)s::%(name)s::%(asctime)s::%(message)s', 'apicalls.log', 'DEBUG')


error_msgs = [
    [{'message': 'PassengerID parameter should be an integer'}, 400],
    [{'message': 'Passenger data not found'}, 404],
]


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


    def put(self, pass_id):
        """PUT method to update passengers data"""

        if pass_id.isdigit():
            resp = Passenger.fs_get_delete_put_post(pass_id)
            logger.debug(f'Item with id {pass_id} is updated. Status code: {resp.status_code}')
            return resp

        logger.error(f'PUT method. Invalid pass_id parameter. Status code: {error_msgs[0][1]}')
        return error_msgs[0][0], error_msgs[0][1]

    def delete(self, pass_id):
        """DELETE method to delete passenger record"""

        if pass_id.isdigit():
            resp = Passenger.fs_get_delete_put_post(pass_id)
            logger.debug(f'Item with id {pass_id} is deleted. Status code: {resp.status_code}')
            return resp

        logger.error(f'DELETE method. Invalid pass_id parameter. Status code: {error_msgs[0][1]}')
        return error_msgs[0][0], error_msgs[0][1]

    def post(self):
        """POST method to create passenger record"""

        resp = Passenger.fs_get_delete_put_post()
        logger.debug(f'Item is created. Status code: {resp.status_code}')
        return resp
