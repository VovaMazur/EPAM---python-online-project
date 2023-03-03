"""Tests for Passenger API module"""
import unittest
from manifestapp import create_app, db
from .data import test_passes


class TestPassengerAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('TestPassAPI setup')
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

            for obj in test_passes:
                db.session.add(obj)
                db.session.commit()

        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        print('TestPassAPI teardown')
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_all_items(self):
        test_resp = TestPassengerAPI.client.get('/passapi')
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

        test_resp = TestPassengerAPI.client.get('/passapi/all')
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

    def test_get_all_items_status(self):
        test_resp = TestPassengerAPI.client.get('/passapi/all/live')
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

        test_resp = TestPassengerAPI.client.get('/passapi/all/dead')
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

    def test_get_specific_item(self):
        test_resp = TestPassengerAPI.client.get('/passapi/1')
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

        test_resp = TestPassengerAPI.client.get('/passapi/2')
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

        test_resp = TestPassengerAPI.client.get('/passapi/10000')
        self.assertEqual(test_resp.status_code, 404)
        self.assertTrue(test_resp.is_json)

        test_resp = TestPassengerAPI.client.get('/passapi/fgfdg')
        self.assertEqual(test_resp.status_code, 404)
        self.assertTrue(test_resp.is_json)

    def test_create_delete_items(self):
        test_item = {
                        "address": "Somewhere",
                        "comments": "",
                        "dob": "1985-04-19",
                        "fname": "Nick",
                        "lname": "Nickelson",
                        "seatno": "05A",
                        "status": "live"
                      }

        test_resp = TestPassengerAPI.client.post('/passapi', json=test_item)
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)
        test_id = test_resp.json.get('item').get('id')

        test_resp = TestPassengerAPI.client.delete('/passapi/'+str(test_id))
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

    def test_create_wrongpayload_items(self):
        test_item = {
                        "address": "Somewhere",
                        "comments": "",
                        "dob": "1985-04-19",
                        "fname": "Nik",
                        "lname": "Nickelson",
                        "seatno": "05A",
                        "status": "like" #wrong status
                      }

        test_resp = TestPassengerAPI.client.post('/passapi', json=test_item)
        self.assertEqual(test_resp.status_code, 400)
        self.assertTrue(test_resp.is_json)

        test_item = {
                        "address": "Somewhere",
                        "comments": "",
                        "dob": "1985-04-19",
                        "fname": "Nik",
                        "lname": "Nickelson",
                        "seatno": "AAA",  #wrong seatno
                        "status": "live"
                      }
        test_resp = TestPassengerAPI.client.post('/passapi', json=test_item)
        self.assertEqual(test_resp.status_code, 400)
        self.assertTrue(test_resp.is_json)

        long_str = 'k' * 46
        test_item = {
                        "address": "Somewhere",
                        "comments": "",
                        "dob": "1985-04-19",
                        "fname": "Nik",
                        "lname": long_str, #long lname
                        "seatno": "05A",
                        "status": "live"
                      }
        test_resp = TestPassengerAPI.client.post('/passapi', json=test_item)
        self.assertEqual(test_resp.status_code, 400)
        self.assertTrue(test_resp.is_json)

        long_str = 'k' * 46
        test_item = {
                        "address": "Somewhere",
                        "comments": "",
                        "dob": "1985-04-19",
                        "fname": long_str, #long fname
                        "lname": "Nickelson",
                        "seatno": "05A",
                        "status": "live"
                      }
        test_resp = TestPassengerAPI.client.post('/passapi', json=test_item)
        self.assertEqual(test_resp.status_code, 400)
        self.assertTrue(test_resp.is_json)

        long_str = 'k' * 101
        test_item = {
                        "address": long_str, #long address
                        "comments": "",
                        "dob": "1985-04-19",
                        "fname": "Nik",
                        "lname": "Nickelson",
                        "seatno": "05A",
                        "status": "live"
                      }
        test_resp = TestPassengerAPI.client.post('/passapi', json=test_item)
        self.assertEqual(test_resp.status_code, 400)
        self.assertTrue(test_resp.is_json)

        long_str = 'k' * 141
        test_item = {
                        "address": "Somewhere",
                        "comments": long_str, #long address
                        "dob": "1985-04-19",
                        "fname": "Nik",
                        "lname": "Nickelson",
                        "seatno": "05A",
                        "status": "live"
                      }
        test_resp = TestPassengerAPI.client.post('/passapi', json=test_item)
        self.assertEqual(test_resp.status_code, 400)
        self.assertTrue(test_resp.is_json)

    def test_create_update_delete_items(self):
        test_item = {
                        "address": "Somewhere",
                        "comments": "",
                        "dob": "1985-04-19",
                        "fname": "Nik",
                        "lname": "Nickelson",
                        "seatno": "05A",
                        "status": "live"
                      }

        test_resp = TestPassengerAPI.client.post('/passapi', json=test_item)
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)
        test_id = test_resp.json.get('item').get('id')
        test_new_comment = {"comments": "NEW COMMENT"}

        test_resp = TestPassengerAPI.client.post('/passapi/' + str(test_id), json=test_new_comment)
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)
        self.assertEqual(test_resp.json.get('item').get('comments'), test_new_comment.get('comments'))

        test_resp = TestPassengerAPI.client.delete('/passapi/'+ str(test_id))
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

    def test_delete_missing_invalid_items(self):
        test_resp = TestPassengerAPI.client.delete('/passapi/dgdfg')
        self.assertEqual(test_resp.status_code, 404)
        self.assertTrue(test_resp.is_json)

        test_resp = TestPassengerAPI.client.delete('/passapi/10000')
        self.assertEqual(test_resp.status_code, 404)
        self.assertTrue(test_resp.is_json)

    def test_post_missing_invalid_items(self):
        test_update = {"comments": "HAHA"}
        test_resp = TestPassengerAPI.client.post('/passapi/dgdfg', json=test_update)
        self.assertEqual(test_resp.status_code, 404)
        self.assertTrue(test_resp.is_json)
 
        test_update = {"comments": "HAHA"}
        test_resp = TestPassengerAPI.client.post('/passapi/10000', json=test_update)
        self.assertEqual(test_resp.status_code, 404)
        self.assertTrue(test_resp.is_json)

