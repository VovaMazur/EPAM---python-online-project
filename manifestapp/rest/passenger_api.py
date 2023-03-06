"""Passenger API main functionality"""
import json
from flask_restful import Resource
from flask import request, Response
from manifestapp.service import pass_get_bystatus, pass_get_byid, pass_post, pass_delete
from manifestapp.logger import logger_setup

logger = logger_setup(__name__, '%(levelname)s::%(name)s::%(asctime)s'
                                '::%(message)s', 'apicalls.log', 'DEBUG')


class PassengerApi(Resource):
    """API class for passengers data"""

    def get(self, pass_id='all', status=None):
        """GET method to retrieve passengers data"""

        if pass_id == 'all':
            resp = pass_get_bystatus(status)
            if resp[1] == 200:
                logger.debug('Get all items with status %s. Status code: %s',
                             status, resp[1])
            else:
                logger.error('Item(s) not found with status %s. Status code: %s',
                             status, resp[1])
            resp = Response(json.dumps(resp[0]), resp[1], mimetype='application/json')


        else:
            resp = pass_get_byid(pass_id)
            if resp[1] == 200:
                logger.debug('Get item with id %s. Status code: %s ',
                             pass_id, resp[1])
            else:
                logger.error('Item with id %s not found. Status code: %s',
                             pass_id, resp[1])
            resp = Response(json.dumps(resp[0]), resp[1], mimetype='application/json')

        return resp

    def delete(self, pass_id):
        """DELETE method to delete passenger record"""

        res = pass_delete(pass_id)
        if res[1] != 200:
            logger.error('DELETE. %s. Status code: %s', res[0]['message'], res[1])

        else:
            logger.debug('DELETE. %s. Status code: %s', res[0]['message'], res[1])

        resp = Response(json.dumps(res[0]), res[1], mimetype='application/json')
        return resp

    def post(self, pass_id=None):
        """POST method to create passenger record"""

        payload = request.get_json()
        res = pass_post(payload, pass_id)

        if res[1] != 200:
            logger.error('POST. %s. Status code: %s', res[0]['message'], res[1])

        elif res[1] == 200:
            logger.debug('POST. %s. Status code: %s', res[0]['message'], res[1])

        resp = Response(json.dumps(res[0]), res[1], mimetype='application/json')

        return resp
