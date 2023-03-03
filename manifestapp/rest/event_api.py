"""Event API main functionality"""
import datetime
import json
from flask_restful import Resource
from flask import request, Response
from manifestapp.service import event_get_bypass, event_get_byid, \
    event_post, event_delete, error_msgs
from manifestapp.logger import logger_setup

logger = logger_setup(__name__, '%(levelname)s::%(name)s::%(asctime)s'
                                '::%(message)s', 'apicalls.log', 'DEBUG')


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


        if (datefrom and not validatedate(datefrom)) or \
                (dateto and not validatedate(dateto)):
            resp = Response(json.dumps(error_msgs[2][0]), error_msgs[2][1],
                            mimetype='application/json')
            logger.error('Invalid %s parameter. '
                         'Status code: %s', ("datefrom" if datefrom else "dateto"),
                         error_msgs[2][1])

        else:
            if event_id == 'all':
                resp = event_get_bypass(passid=pass_id, datefrom=datefrom, dateto=dateto)

                if resp[1] == 200:
                    logger.debug('Get items. Passid:%s, datefrom:%s, dateto:%s. Status code: %s',
                                 pass_id, datefrom, dateto, resp[1])
                else:
                    logger.error('%s. Passid:%s, datefrom:%s, dateto:%s. '
                                 'Status code: %s', resp[0]['message'],
                                 pass_id, datefrom, dateto, resp[1])
                    resp = Response(json.dumps(resp[0]), resp[1], mimetype='application/json')
            else:
                resp = event_get_byid(event_id)
                if resp[1] == 200:
                    logger.debug('Get items. Passid:%s, datefrom:%s, dateto:%s. Status code: %s',
                                 pass_id, datefrom, dateto, resp[1])
                else:
                    logger.error('%s. EventID:%s, datefrom:%s, dateto:%s. '
                                 'Status code: %s', resp[0]['message'],
                                 event_id, datefrom, dateto, resp[1])
                    resp = Response(json.dumps(resp[0]), resp[1], mimetype='application/json')

        return resp

    def delete(self, event_id):
        """DELETE method to delete event record"""

        res = event_delete(event_id)
        if res[1] != 200:
            logger.error('DELETE. %s. Status code: %s', res[0]['message'], res[1])

        else:
            logger.debug('DELETE. %s. Status code: %s', res[0]['message'], res[1])

        resp = Response(json.dumps(res[0]), res[1], mimetype='application/json')
        return resp

    def post(self, event_id=None):
        """POST method to create/update event record"""

        payload = request.get_json()
        res = event_post(payload, event_id)

        if res[1] != 200:
            logger.error('POST. %s. Status code: %s', res[0]['message'], res[1])

        elif res[1] == 200:
            logger.debug('POST. %s. Status code: %s', res[0]['message'], res[1])

        resp = Response(json.dumps(res[0]), res[1], mimetype='application/json')

        return resp
