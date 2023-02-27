"""Event API main functionality"""
import datetime
import json
from flask_restful import Resource
from jsonschema import validate, exceptions
from flask import request, Response
from manifestapp.service import event_get_bypass, event_get_byid
from manifestapp.models import Event
from manifestapp.logger import logger_setup

logger = logger_setup(__name__, '%(levelname)s::%(name)s::%(asctime)s'
                                '::%(message)s', 'apicalls.log', 'DEBUG')


error_msgs = [
    [{'message': 'EventID parameter should be an integer'}, 400],
    [{'message': 'Event(s) not found'}, 404],
    [{'message': 'Date parameter should be a valid date, format YYYY-MM-DD'}, 400],
    [{'message': 'Incorrect payload'}, 400],
    [{'message': 'Unknown error during record creation'}, 400]
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

    def get(self, event_id='all', pass_id='all', datefrom=None, dateto=None):
        """GET method to retrieve events data"""

        datefrom = None if datefrom in ('-', 'None') else datefrom
        dateto = None if dateto in ('-', 'None') else dateto


        if event_id == 'all':
            if (datefrom and not validatedate(datefrom)) or \
                    (dateto and not validatedate(dateto)):
                resp = Response(json.dumps(error_msgs[2][0]), error_msgs[2][1],
                                mimetype='application/json')
                logger.error('Invalid %s parameter. '
                             'Status code: %s', ("datefrom" if datefrom else "dateto"),
                             error_msgs[2][1])

            else:
                resp = event_get_bypass(passid=pass_id, datefrom=datefrom, dateto=dateto)
                if resp:
                    logger.debug('Get items. Passid:%s, datefrom:%s, dateto:%s. Status code: %s',
                                 pass_id, datefrom, dateto, resp.status_code)
                else:
                    resp = Response(json.dumps(error_msgs[1][0]), error_msgs[1][1],
                                    mimetype='application/json')
                    logger.error('Items not found. Passid:%s, datefrom:%s, dateto:%s. '
                                 'Status code: %s', pass_id, datefrom, dateto, error_msgs[1][1])

            return resp

        if event_id.isdigit():
            resp = event_get_byid(event_id)
            if resp:
                logger.debug('Get item with id %s. Status code: %s',
                             event_id, resp.status_code)
            else:
                logger.error('Item with id %s not found. Status code: %s',
                             event_id, error_msgs[1][1])
                resp = Response(json.dumps(error_msgs[1][0]), error_msgs[1][1],
                                mimetype='application/json')

        else:
            logger.error('GET method. Invalid event_id (%s) parameter. Status code: %s',
                         event_id, error_msgs[0][1])
            resp = Response(json.dumps(error_msgs[0][0]), error_msgs[0][1],
                            mimetype='application/json')

        return resp

    def delete(self, event_id):
        """DELETE method to delete event record"""

        if event_id.isdigit():
            item = event_get_byid(event_id)
            if item:
                resp = Event.fs_get_delete_put_post(event_id)
                logger.debug('Item with id %s is deleted. Status code: %s',
                             event_id, resp.status_code)
            else:
                logger.error('Item with id %s not found. Status code: %s',
                             event_id, error_msgs[1][1])
                resp = Response(json.dumps(error_msgs[1][0]), error_msgs[1][1],
                                mimetype='application/json')

        else:
            resp = Response(json.dumps(error_msgs[0][0]), error_msgs[0][1],
                            mimetype='application/json')
            logger.error('DELETE method. Invalid event_id parameter. Status code: %s',
                         error_msgs[0][1])
        return resp

    def post(self, event_id=None):
        """POST method to create/update event record"""

        payload = request.get_json()
        try:
            if not event_id:
                validate(payload, schema=create_schema)
            else:
                validate(payload, schema=update_schema)

        except exceptions.ValidationError as error:
            logger.error('POST method. Invalid payload. %s. Status code: 400', str(error))
            resp = Response(json.dumps(error_msgs[3][0]), error_msgs[3][1],
                            mimetype='application/json')

        else:
            if not event_id:
                resp = Event.fs_get_delete_put_post()
                if resp.__class__.__name__ == 'Response':
                    logger.debug('Item is created. Status code: %s', resp.status_code)
                else:
                    logger.error('Error during item creation. %s. Status code: 400', resp)
                    resp = Response(json.dumps(error_msgs[4][0]), error_msgs[4][1],
                                    mimetype='application/json')

            elif event_id.isdigit():
                item = event_get_byid(event_id)
                if item:
                    resp = Event.fs_get_delete_put_post(event_id)
                    logger.debug('Item with id %s is updated. Status code: %s',
                                 event_id, resp.status_code)

                else:
                    logger.error('Item with id %s not found. Status code: %s',
                                 event_id, error_msgs[1][1])
                    resp = Response(json.dumps(error_msgs[1][0]), error_msgs[1][1],
                                    mimetype='application/json')

            else:
                logger.error('POST (update). Invalid event_id %s parameter. Status code: %s',
                             event_id, error_msgs[0][1])
                resp = Response(json.dumps(error_msgs[0][0]), error_msgs[0][1],
                                mimetype='application/json')

        return resp
