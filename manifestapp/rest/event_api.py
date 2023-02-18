from flask_restful import Resource
from manifestapp.models import Event
import datetime
from manifestapp.logger import logger_setup

logger = logger_setup(__name__, '%(levelname)s::%(name)s::%(asctime)s::%(message)s', 'apicalls.log', 'DEBUG')


error_msgs = [
    [{'message': 'EventID parameter should be an integer'}, 400],
    [{'message': 'Event not found'}, 404],
    [{'message': 'Date parameter should be a valid date, format YYYY-MM-DD'}, 400]
]


def validatedate(datestring):
    """function to validate if string passed is valid date"""

    try:
        datetime.date.fromisoformat(datestring)
        return True
    except:
        return False


class EventApi(Resource):
    """API class for events data"""

    def get(self, event_id='all', datefrom=None, dateto=None):
        """GET method to retrieve events data"""

        if event_id == 'all':
            if not (datefrom or dateto):
                resp = Event.fs_get_delete_put_post()
                logger.debug(f'Get all items. Status code: {resp.status_code}')
                return resp

            else:
                if datefrom == '-':
                    datefrom = None

                if datefrom:
                    if not validatedate(datefrom):
                        logger.error(f'Invalid datefrom parameter. Status code: {error_msgs[2][1]}')
                        return error_msgs[2][0], error_msgs[2][1]

                if dateto:
                    if not validatedate(dateto):
                        logger.error(f'Invalid dateto parameter. Status code: {error_msgs[2][1]}')
                        return error_msgs[2][0], error_msgs[2][1]


                if datefrom and dateto:
                    items = Event.query.filter(Event.date >= datefrom, Event.date <= dateto).all()

                elif datefrom:
                    items = Event.query.filter(Event.date >= datefrom).all()

                else:
                    items = Event.query.filter(Event.date <= dateto).all()

                resp = Event.fs_json_list(items)
                logger.debug(f'Get items from {datefrom} to {dateto}. Status code: {resp.status_code}')
                return resp

        else:
            if event_id.isdigit():
                item = Event.query.get(event_id)
                if not item:
                    logger.error(f'Item with id {event_id} not found. Status code: {error_msgs[1][1]}')
                    return error_msgs[1][0], error_msgs[1][1]

                resp = Event.fs_json_list([item])
                logger.debug(f'Get item with id {event_id}. Status code: {resp.status_code}')
                return resp

            else:
                logger.error(f'GET method. Invalid event_id parameter. Status code: {error_msgs[0][1]}')
                return error_msgs[0][0], error_msgs[0][1]


    def put(self, event_id):
        """PUT method to update event data"""

        if event_id.isdigit():
            resp = Event.fs_get_delete_put_post(event_id)
            logger.debug(f'Item with id {event_id} is updated. Status code: {resp.status_code}')
            return resp

        logger.error(f'PUT method. Invalid event_id parameter. Status code: {error_msgs[0][1]}')
        return error_msgs[0][0], error_msgs[0][1]

    def delete(self, event_id):
        """DELETE method to delete event record"""

        if event_id.isdigit():
            resp = Event.fs_get_delete_put_post(event_id)
            logger.debug(f'Item with id {event_id} is deleted. Status code: {resp.status_code}')
            return resp

        logger.error(f'DELETE method. Invalid event_id parameter. Status code: {error_msgs[0][1]}')
        return error_msgs[0][0], error_msgs[0][1]

    def post(self):
        """POST method to create event record"""

        resp = Event.fs_get_delete_put_post()
        logger.debug(f'Item is created. Status code: {resp.status_code}')
        return resp
