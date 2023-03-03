"""Tests for Event API module"""
import unittest
from manifestapp import create_app, db
from .data import test_events


class TestEventAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('TestEventAPI setup')
        test_config = {
            'ENV': 'development',
            'DEBUG': True,
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db',
            'SECRET_KEY': 'test'
        }

        cls.app = create_app(test_config)
        with cls.app.app_context():
            db.create_all()

            for obj in test_events:
                db.session.add(obj)
                db.session.commit()

        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        print('TestEventAPI teardown')
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_all_events(self):
        test_resp = TestEventAPI.client.get('/eventapi')
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

        test_resp = TestEventAPI.client.get('/eventapi/all')
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

        test_resp = TestEventAPI.client.get('/eventapi/all/all')
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

    def test_get_all_events_for_pass(self):
        test_resp = TestEventAPI.client.get('/eventapi/all/1')
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

        test_resp = TestEventAPI.client.get('/eventapi/all/2')
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

        test_resp = TestEventAPI.client.get('/eventapi/all/10000')
        self.assertEqual(test_resp.status_code, 404)
        self.assertTrue(test_resp.is_json)

        test_resp = TestEventAPI.client.get('/eventapi/all/tyty')
        self.assertEqual(test_resp.status_code, 404)
        self.assertTrue(test_resp.is_json)

    def test_get_all_events_from_to(self):
        test_resp = TestEventAPI.client.get('/eventapi/all/all/2022-01-01')
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

        test_resp = TestEventAPI.client.get('/eventapi/all/all/2022-01-01/2022-12-31')
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

        test_resp = TestEventAPI.client.get('/eventapi/all/all/-/2022-12-31')
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

        test_resp = TestEventAPI.client.get('/eventapi/all/all/rtert/2022-12-31')
        self.assertEqual(test_resp.status_code, 400)
        self.assertTrue(test_resp.is_json)

        test_resp = TestEventAPI.client.get('/eventapi/all/all/2022-01-01/ff31')
        self.assertEqual(test_resp.status_code, 400)
        self.assertTrue(test_resp.is_json)

        test_resp = TestEventAPI.client.get('/eventapi/all/1/2022-01-01')
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

        test_resp = TestEventAPI.client.get('/eventapi/all/1/2022-01-01/2022-12-31')
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

        test_resp = TestEventAPI.client.get('/eventapi/all/2/-/2022-12-31')
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

    def test_get_specific_events(self):
        test_resp = TestEventAPI.client.get('/eventapi/2')
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

        test_resp = TestEventAPI.client.get('/eventapi/1')
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

        test_resp = TestEventAPI.client.get('/eventapi/10000')
        self.assertEqual(test_resp.status_code, 404)
        self.assertTrue(test_resp.is_json)

        test_resp = TestEventAPI.client.get('/eventapi/fgfdg')
        self.assertEqual(test_resp.status_code, 404)
        self.assertTrue(test_resp.is_json)

    def test_create_delete_events(self):
        test_event = {
                    "comments": "",
                    "date": '2023-02-22',
                    "description": "I see the great testing coming",
                    "geo_location": "-20.344, 130.031",
                    "passengerID": 1,
                    "other_pass": "",
                    "status": "success"}

        test_resp = TestEventAPI.client.post('/eventapi', json=test_event)
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)
        test_id = test_resp.json.get('item').get('id')

        test_resp = TestEventAPI.client.delete('/eventapi/'+str(test_id))
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
        test_resp = TestEventAPI.client.post('/eventapi', json=test_event)
        self.assertEqual(test_resp.status_code, 400)
        self.assertTrue(test_resp.is_json)

        test_event = {
                    "comments": "",
                    "date": "2023-02-22",
                    "description": "I see the great testing coming",
                    "geo_location": "-20.344, 130.031",
                    "passengerID": '1', #wrong ID
                    "status": "success"}
        test_resp = TestEventAPI.client.post('/eventapi', json=test_event)
        self.assertEqual(test_resp.status_code, 400)
        self.assertTrue(test_resp.is_json)

        test_event = {
                    "comments": "",
                    "date": "2023-02-22",
                    "description": "I see the great testing coming",
                    "geo_location": "-20.344 / 130.031", #wrong geo location
                    "passengerID": 1,
                    "status": "success"}
        test_resp = TestEventAPI.client.post('/eventapi', json=test_event)
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
        test_resp = TestEventAPI.client.post('/eventapi', json=test_event)
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
        test_resp = TestEventAPI.client.post('/eventapi', json=test_event)
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

        test_resp = TestEventAPI.client.post('/eventapi', json=test_event)
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)
        test_id = test_resp.json.get('item').get('id')
        test_new_comment = {"comments": "NEW COMMENT"}

        test_resp = TestEventAPI.client.post('/eventapi/' + str(test_id), json=test_new_comment)
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)
        self.assertEqual(test_resp.json.get('item').get('comments'), test_new_comment.get('comments'))

        test_resp = TestEventAPI.client.delete('/eventapi/'+ str(test_id))
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

    def test_delete_missing_invalid_events(self):
        test_resp = TestEventAPI.client.delete('/eventapi/dgdfg')
        self.assertEqual(test_resp.status_code, 404)
        self.assertTrue(test_resp.is_json)

        test_resp = TestEventAPI.client.delete('/eventapi/10000')
        self.assertEqual(test_resp.status_code, 404)
        self.assertTrue(test_resp.is_json)

    def test_post_missing_invalid_events(self):
        test_update = {"comments": "HAHA"}
        test_resp = TestEventAPI.client.post('/eventapi/dgdfg', json=test_update)
        self.assertEqual(test_resp.status_code, 404)
        self.assertTrue(test_resp.is_json)

        test_update = {"comments": "HAHA"}
        test_resp = TestEventAPI.client.post('/eventapi/10000', json=test_update)
        self.assertEqual(test_resp.status_code, 404)
        self.assertTrue(test_resp.is_json)

