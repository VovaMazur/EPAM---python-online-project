from flask_restful import Resource
from manifestapp.models import Event
import datetime
from manifestapp.logger import logger_setup
from jsonschema import validate
from flask import request

logger = logger_setup(__name__, '%(levelname)s::%(name)s::%(asctime)s::%(message)s', 'apicalls.log', 'DEBUG')


error_msgs = [
    [{'message': 'EventID parameter should be an integer'}, 400],
    [{'message': 'Event not found'}, 404],
    [{'message': 'Date parameter should be a valid date, format YYYY-MM-DD'}, 400]
]

create_schema = {
    'type': 'object',
    'properties': {
        'date': {'type': 'string',
                 'format': 'date'},
        'passengerID': {'type': 'integer'},
        'geo_location': {'type': 'string',
                         'pattern': '^[-]?[0-9]+[.][0-9]+[,][ ]?[-]?[0-9]+[.][0-9]+$'},
        'description': {'type': 'string',
                        'maxLength': 90},
        'status': {'type': 'string',
                   'pattern': 'unknown|success|failure'},
        'other_pass': {'type': 'string'},
        'comments': {'type': 'string',
                     'maxLength': 140}
    },
    'additionalProperties': False,
    'required': ['date', 'passengerID', 'geo_location', 'description', 'status']
}

update_schema = {}
update_schema = create_schema.copy()
update_schema.pop('required')


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

    def delete(self, event_id):
        """DELETE method to delete event record"""

        if event_id.isdigit():
            resp = Event.fs_get_delete_put_post(event_id)
            if resp.__class__.__name__ == 'Response':
                logger.debug(f'Item with id {event_id} is deleted. Status code: {resp.status_code}')
            else:
                logger.error(f'Error during item deletion. {resp}. Status code: 400')

            return resp

        logger.error(f'DELETE method. Invalid event_id parameter. Status code: {error_msgs[0][1]}')
        return error_msgs[0][0], error_msgs[0][1]

    def post(self, event_id=None):
        """POST method to create/update event record"""

        if not event_id:
            payload = request.get_json()
            try:
                validate(payload, schema=create_schema)
            except Exception as e:
                logger.error(f'POST method (create). Invalid payload. {str(e)}. Status code: 400')
                return 'Your payload is incorrect. '+str(e.message), 400

            resp = Event.fs_get_delete_put_post()
            if resp.__class__.__name__ == 'Response':
                logger.debug(f'Item is created. Status code: {resp.status_code}')
            else:
                logger.error(f'Error during item creation. {resp}. Status code: 400')

        else:
            if event_id.isdigit():
                payload = request.get_json()
                try:
                    validate(payload, schema=update_schema)
                except Exception as e:
                    logger.error(f'POST method (update). Invalid payload. {str(e)}. Status code: 400')
                    return 'Your payload is incorrect.' + str(e.message), 400

                resp = Event.fs_get_delete_put_post(event_id)
                if resp.__class__.__name__ == 'Response':
                    logger.debug(f'Item with id {event_id} is updated. Status code: {resp.status_code}')
                else:
                    logger.error(f'Error during update. {resp}. Status code: 400')

            else:
                logger.error(f'POST method (update). Invalid event_id {event_id} parameter. Status code: {error_msgs[0][1]}')
                return error_msgs[0][0], error_msgs[0][1]

        return resp
