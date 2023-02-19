"""Event API main functionality"""
import datetime
from flask_restful import Resource
from jsonschema import validate, exceptions
from flask import request
from manifestapp.models import Event
from manifestapp.logger import logger_setup

logger = logger_setup(__name__, '%(levelname)s::%(name)s::%(asctime)s'
                                '::%(message)s', 'apicalls.log', 'DEBUG')


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
    except ValueError:
        return False


class EventApi(Resource):
    """API class for events data"""

    def get(self, event_id='all', datefrom=None, dateto=None):
        """GET method to retrieve events data"""

        if event_id == 'all':
            if not (datefrom or dateto):
                resp = Event.fs_get_delete_put_post()
                logger.debug('Get all items. Status code: %s', resp.status_code)

            else:
                datefrom = None if datefrom == '-' else datefrom

                if (datefrom and not validatedate(datefrom)) or \
                        (dateto and not validatedate(dateto)):
                    logger.error('Invalid %s parameter. '
                                 'Status code: %s', ("datefrom" if datefrom else "dateto"),
                                 error_msgs[2][1])
                    return error_msgs[2][0], error_msgs[2][1]

                if datefrom and dateto:
                    items = Event.query.filter(Event.date >= datefrom, Event.date <= dateto).all()

                elif datefrom:
                    items = Event.query.filter(Event.date >= datefrom).all()

                else:
                    items = Event.query.filter(Event.date <= dateto).all()

                resp = Event.fs_json_list(items)
                logger.debug('Get items from %s to %s. Status code: %s',
                             datefrom, dateto, resp.status_code)
            return resp

        if event_id.isdigit():
            item = Event.query.get(event_id)
            if not item:
                logger.error('Item with id %s not found. Status code: %s',
                             event_id, error_msgs[1][1])
                return error_msgs[1][0], error_msgs[1][1]

            resp = Event.fs_json_list([item])
            logger.debug('Get item with id %s. Status code: %s',
                         event_id, resp.status_code)
            return resp

        logger.error('GET method. Invalid event_id parameter. Status code: %s',
                     error_msgs[0][1])
        return error_msgs[0][0], error_msgs[0][1]

    def delete(self, event_id):
        """DELETE method to delete event record"""

        if event_id.isdigit():
            resp = Event.fs_get_delete_put_post(event_id)
            if resp.__class__.__name__ == 'Response':
                logger.debug('Item with id %s is deleted. Status code: %s',
                             event_id, resp.status_code)
            else:
                logger.error('Error during item deletion. %s. Status code: 400', resp)

            return resp

        logger.error('DELETE method. Invalid event_id parameter. Status code: %s',
                     error_msgs[0][1])
        return error_msgs[0][0], error_msgs[0][1]

    def post(self, event_id=None):
        """POST method to create/update event record"""

        if not event_id:
            payload = request.get_json()
            try:
                validate(payload, schema=create_schema)
            except exceptions.ValidationError as error:
                logger.error('POST (create). Invalid payload. %s. Status code: 400', str(error))
                return 'Your payload is incorrect. '+str(error), 400

            resp = Event.fs_get_delete_put_post()
            if resp.__class__.__name__ == 'Response':
                logger.debug('Item is created. Status code: %s', resp.status_code)
            else:
                logger.error('Error during item creation. %s. Status code: 400', resp)

        else:
            if event_id.isdigit():
                payload = request.get_json()
                try:
                    validate(payload, schema=update_schema)
                except exceptions.ValidationError as error:
                    logger.error('POST (update). Invalid payload. %s. Status code: 400', str(error))
                    return 'Your payload is incorrect.' + str(error), 400

                resp = Event.fs_get_delete_put_post(event_id)
                if resp.__class__.__name__ == 'Response':
                    logger.debug('Item with id %s is updated. Status code: %s',
                                 event_id, resp.status_code)
                else:
                    logger.error('Error during update. %s. Status code: 400', resp)

            else:
                logger.error('POST (update). Invalid event_id %s parameter. Status code: %s',
                             event_id, error_msgs[0][1])
                return error_msgs[0][0], error_msgs[0][1]

        return resp
