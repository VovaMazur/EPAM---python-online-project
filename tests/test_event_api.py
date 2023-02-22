"""Tests for Event API module"""
import unittest
import json
from manifestapp import create_app
from manifestapp.rest import EventApi


class TestEventAPI(unittest.TestCase):
    app = create_app()
    test_inst = EventApi()

    def test_get_all_events(self):
        test_resp = TestEventAPI.app.test_client().get('http://localhost:5000/eventapi')
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

        test_resp = TestEventAPI.app.test_client().get('http://localhost:5000/eventapi/all')
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

    def test_get_all_events_from_to(self):
        test_resp = TestEventAPI.app.test_client().get('http://localhost:5000/eventapi/all/2022-01-01')
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

        test_resp = TestEventAPI.app.test_client().get('http://localhost:5000/eventapi/all/2022-01-01/2022-12-31')
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

        test_resp = TestEventAPI.app.test_client().get('http://localhost:5000/eventapi/all/-/2022-12-31')
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

        test_resp = TestEventAPI.app.test_client().get('http://localhost:5000/eventapi/all/rtert/2022-12-31')
        self.assertEqual(test_resp.status_code, 400)
        self.assertTrue(test_resp.is_json)

        test_resp = TestEventAPI.app.test_client().get('http://localhost:5000/eventapi/all/2022-01-01/ff31')
        self.assertEqual(test_resp.status_code, 400)
        self.assertTrue(test_resp.is_json)

    def test_get_specific_events(self):
        test_resp = TestEventAPI.app.test_client().get('http://localhost:5000/eventapi/2')
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

        test_resp = TestEventAPI.app.test_client().get('http://localhost:5000/eventapi/3')
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

        test_resp = TestEventAPI.app.test_client().get('http://localhost:5000/eventapi/10000')
        self.assertEqual(test_resp.status_code, 404)
        self.assertTrue(test_resp.is_json)

        test_resp = TestEventAPI.app.test_client().get('http://localhost:5000/eventapi/1')
        self.assertEqual(test_resp.status_code, 404)
        self.assertTrue(test_resp.is_json)

        test_resp = TestEventAPI.app.test_client().get('http://localhost:5000/eventapi/fgfdg')
        self.assertEqual(test_resp.status_code, 400)
        self.assertTrue(test_resp.is_json)

    def test_create_delete_events(self):
        test_event = {
                    "comments": "",
                    "date": "2023-02-22",
                    "description": "I see the great testing coming",
                    "geo_location": "-20.344, 130.031",
                    "passengerID": 1,
                    "status": "success"}

        headers = {'Content-Type': 'application/json'}

        test_resp = TestEventAPI.app.test_client().post('http://localhost:5000/eventapi', data=json.dumps(test_event), headers=headers)
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)
        test_id = test_resp.json.get('id')

        test_resp = TestEventAPI.app.test_client().delete('http://localhost:5000/eventapi/'+str(test_id))
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

    def test_create_wrongpayload_events(self):
        test_event = {
                    "comments": "",
                    "date": "2023-02-22",
                    "description": "I see the great testing coming",
                    "geo_location": "-20.344, 130.031",
                    "passengerID": 1,
                    "status": "gkhkkl"} #wrong status
        headers = {'Content-Type': 'application/json'}
        test_resp = TestEventAPI.app.test_client().post('http://localhost:5000/eventapi', data=json.dumps(test_event), headers=headers)
        self.assertEqual(test_resp.status_code, 400)
        self.assertTrue(test_resp.is_json)

        test_event = {
                    "comments": "",
                    "date": "2023-02-22",
                    "description": "I see the great testing coming",
                    "geo_location": "-20.344, 130.031",
                    "passengerID": '1', #wrong ID
                    "status": "success"}
        test_resp = TestEventAPI.app.test_client().post('http://localhost:5000/eventapi', data=json.dumps(test_event), headers=headers)
        self.assertEqual(test_resp.status_code, 400)
        self.assertTrue(test_resp.is_json)

        test_event = {
                    "comments": "",
                    "date": "2023-02-22",
                    "description": "I see the great testing coming",
                    "geo_location": "-20.344 / 130.031", #wrong geo location
                    "passengerID": 1,
                    "status": "success"}
        test_resp = TestEventAPI.app.test_client().post('http://localhost:5000/eventapi', data=json.dumps(test_event), headers=headers)
        self.assertEqual(test_resp.status_code, 400)
        self.assertTrue(test_resp.is_json)

        long_str = 'x' * 91
        test_event = {
                    "comments": "",
                    "date": "2023-02-22",
                    "description": long_str, #very long description
                    "geo_location": "-20.344, 130.031",
                    "passengerID": 1,
                    "status": "success"}
        test_resp = TestEventAPI.app.test_client().post('http://localhost:5000/eventapi', data=json.dumps(test_event), headers=headers)
        self.assertEqual(test_resp.status_code, 400)
        self.assertTrue(test_resp.is_json)

        long_str = 'x' * 141
        test_event = {
                    "comments": long_str, #very long comments
                    "date": "2023-02-22",
                    "description": "I see the great testing coming",
                    "geo_location": "-20.344, 130.031",
                    "passengerID": 1,
                    "status": "success"}
        test_resp = TestEventAPI.app.test_client().post('http://localhost:5000/eventapi', data=json.dumps(test_event), headers=headers)
        self.assertEqual(test_resp.status_code, 400)
        self.assertTrue(test_resp.is_json)

    def test_create_update_delete_events(self):
        test_event = {
                    "comments": "",
                    "date": "2023-02-22",
                    "description": "I see the great testing coming",
                    "geo_location": "-20.344, 130.031",
                    "passengerID": 1,
                    "status": "success"}

        headers = {'Content-Type': 'application/json'}

        test_resp = TestEventAPI.app.test_client().post('http://localhost:5000/eventapi', data=json.dumps(test_event), headers=headers)
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)
        test_id = test_resp.json.get('id')
        test_new_comment = {"comments": "NEW COMMENT"}

        test_resp = TestEventAPI.app.test_client().post('http://localhost:5000/eventapi/' + str(test_id), data=json.dumps(test_new_comment), headers=headers)
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)
        self.assertEqual(test_resp.json.get('item').get('comments'), test_new_comment.get('comments'))

        test_resp = TestEventAPI.app.test_client().delete('http://localhost:5000/eventapi/'+ str(test_id))
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

    def test_delete_missing_invalid_events(self):
        test_resp = TestEventAPI.app.test_client().delete('http://localhost:5000/eventapi/dgdfg')
        self.assertEqual(test_resp.status_code, 400)
        self.assertTrue(test_resp.is_json)

        test_resp = TestEventAPI.app.test_client().delete('http://localhost:5000/eventapi/10000')
        self.assertEqual(test_resp.status_code, 404)
        self.assertTrue(test_resp.is_json)

    def test_post_missing_invalid_events(self):
        test_update = {"comments": "HAHA"}
        headers = {'Content-Type': 'application/json'}
        test_resp = TestEventAPI.app.test_client().post('http://localhost:5000/eventapi/dgdfg', data=json.dumps(test_update), headers=headers)
        self.assertEqual(test_resp.status_code, 400)
        self.assertTrue(test_resp.is_json)

        test_update = {"comments": "HAHA"}
        headers = {'Content-Type': 'application/json'}
        test_resp = TestEventAPI.app.test_client().post('http://localhost:5000/eventapi/10000', data=json.dumps(test_update), headers=headers)
        self.assertEqual(test_resp.status_code, 404)
        self.assertTrue(test_resp.is_json)

