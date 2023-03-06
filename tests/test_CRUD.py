"""Tests for components"""
import unittest
from manifestapp import create_app, db
from manifestapp.service import event_get_bypass, event_get_byid, event_post, \
    event_delete, event_get_summary, pass_get_bystatus, pass_get_byid, pass_post, \
    pass_delete, pass_getall_list
from .data import t_passes, t_events


class TestCrud(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Test setup')
        t_config = {
            'ENV': 'development',
            'DEBUG': True,
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db',
            'SECRET_KEY': 'test'
        }

        cls.app = create_app(t_config)

        with cls.app.app_context():
            db.create_all()

            db.session.add_all(t_events + t_passes)
            db.session.commit()


        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        print('Test teardown')
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_event_get(self):
        with TestCrud.app.app_context():
            test_resp = event_get_bypass() # get all
            self.assertEqual(test_resp[1], 200)
            self.assertEqual(test_resp[0].get('message'), 'Item(s) retrieved')
            self.assertGreater(len(test_resp[0].get('item')), 0)

            test_resp = event_get_bypass(passid='all') # get all
            self.assertEqual(test_resp[1], 200)
            self.assertEqual(test_resp[0].get('message'), 'Item(s) retrieved')
            self.assertGreater(len(test_resp[0].get('item')), 0)

            test_resp = event_get_bypass(passid='all', datefrom='2022-01-01')
            self.assertEqual(test_resp[1], 200)
            self.assertEqual(test_resp[0].get('message'), 'Item(s) retrieved')
            self.assertGreater(len(test_resp[0].get('item')), 0)

            test_resp = event_get_bypass(passid='1', datefrom='2022-01-01')
            self.assertEqual(test_resp[1], 200)
            self.assertEqual(test_resp[0].get('message'), 'Item(s) retrieved')
            self.assertGreater(len(test_resp[0].get('item')), 0)

            test_resp = event_get_bypass(passid='10000')
            self.assertEqual(test_resp[1], 404)
            self.assertEqual(test_resp[0].get('message'), 'Item(s) not found')
            self.assertEqual(len(test_resp[0].get('item')), 0)

            test_resp = event_get_bypass(passid='1', datefrom='2022-01-01', dateto='2023-03-01')
            self.assertEqual(test_resp[1], 200)
            self.assertEqual(test_resp[0].get('message'), 'Item(s) retrieved')
            self.assertGreater(len(test_resp[0].get('item')), 0)

            test_resp = event_get_bypass(passid='1', dateto='2023-03-01')
            self.assertEqual(test_resp[1], 200)
            self.assertEqual(test_resp[0].get('message'), 'Item(s) retrieved')
            self.assertGreater(len(test_resp[0].get('item')), 0)

            test_resp = event_get_bypass(passid='1')
            self.assertEqual(test_resp[1], 200)
            self.assertEqual(test_resp[0].get('message'), 'Item(s) retrieved')
            self.assertGreater(len(test_resp[0].get('item')), 0)

            test_resp = event_get_bypass(passid='all', datefrom='2022-01-01', dateto='-')
            self.assertEqual(test_resp[1], 200)
            self.assertEqual(test_resp[0].get('message'), 'Item(s) retrieved')
            self.assertGreater(len(test_resp[0].get('item')), 0)

            test_resp = event_get_bypass(passid='all', dateto='2023-02-01')
            self.assertEqual(test_resp[1], 200)
            self.assertEqual(test_resp[0].get('message'), 'Item(s) retrieved')
            self.assertGreater(len(test_resp[0].get('item')), 0)

            test_resp = event_get_bypass(passid='all', datefrom='-', dateto='2023-02-01')
            self.assertEqual(test_resp[1], 200)
            self.assertEqual(test_resp[0].get('message'), 'Item(s) retrieved')
            self.assertGreater(len(test_resp[0].get('item')), 0)

            test_resp = event_get_bypass(passid='all', datefrom='2022-01-01', dateto='2023-02-01')
            self.assertEqual(test_resp[1], 200)
            self.assertEqual(test_resp[0].get('message'), 'Item(s) retrieved')
            self.assertGreater(len(test_resp[0].get('item')), 0)

    def test_event_get_by_id(self):
        with TestCrud.app.app_context():
            test_resp = event_get_byid(event_id=2)
            self.assertEqual(test_resp[1], 200)
            self.assertEqual(test_resp[0].get('message'), 'Item(s) retrieved')
            self.assertEqual(len(test_resp[0].get('item')), 8)

            test_resp = event_get_byid(event_id=10000)
            self.assertEqual(test_resp[1], 404)
            self.assertEqual(test_resp[0].get('message'), 'Item(s) not found')
            self.assertEqual(len(test_resp[0].get('item')), 0)

    def test_event_post(self):
        test_payload = {
                        'date': '2022-12-15',
                        'passengerID': 1,
                        'geo_location': '12.45, 23.45',
                        'description': 'auto testing dummy descp',
                        'status': 'success',
                        'other_pass': '',
                        'comments': ''}

        test_invalid_payload = {
                'date': '2022-12-15',
                'passengerID': '1',
                'geo_location': '12.45, 23.45',
                'description': 'auto testing dummy descp',
                'status': 'success',
                'other_pass': '',
                'comments': ''}

        with TestCrud.app.app_context():
            test_resp = event_post(payload=test_payload)
            self.assertEqual(test_resp[1], 200)
            self.assertEqual(test_resp[0].get('message'), 'Item created')
            self.assertEqual(len(test_resp[0].get('item')), 8)

            test_resp = event_post(payload=test_payload, event_id=2)
            self.assertEqual(test_resp[1], 200)
            self.assertEqual(test_resp[0].get('message'), 'Item updated')
            self.assertEqual(len(test_resp[0].get('item')), 8)

            test_resp = event_post(payload=test_payload, event_id=10000)
            self.assertEqual(test_resp[1], 404)
            self.assertEqual(test_resp[0].get('message'), 'Item(s) not found')
            self.assertEqual(len(test_resp[0].get('item')), 0)

            test_resp = event_post(payload=test_invalid_payload)
            self.assertEqual(test_resp[1], 400)
            self.assertIn('Incorrect payload', test_resp[0].get('message'))

    def test_event_delete(self):
        with TestCrud.app.app_context():
            test_resp = event_delete(event_id=10000)
            self.assertEqual(test_resp[1], 404)
            self.assertEqual(test_resp[0].get('message'), 'Item(s) not found')

            test_resp = event_delete(event_id=1)
            self.assertEqual(test_resp[1], 200)
            self.assertEqual(test_resp[0].get('message'), 'Item deleted')
            self.assertEqual(len(test_resp[0].get('item')), 8)

    def test_event_summary(self):
        with TestCrud.app.app_context():
            test_resp = event_get_summary()
            total_events = len(event_get_bypass()[0].get('item'))
            self.assertEqual(type(test_resp), dict)
            self.assertEqual(sum(test_resp.values()), total_events)

    def test_pass_get(self):
        with TestCrud.app.app_context():
            test_resp = pass_get_bystatus()  # get all
            self.assertEqual(test_resp[1], 200)
            self.assertEqual(test_resp[0].get('message'), 'Item(s) retrieved')
            self.assertGreater(len(test_resp[0].get('item')), 0)

            test_resp = pass_get_bystatus(status='all')
            self.assertEqual(test_resp[1], 200)
            self.assertEqual(test_resp[0].get('message'), 'Item(s) retrieved')
            self.assertGreater(len(test_resp[0].get('item')), 0)

            test_resp = pass_get_bystatus(status='unknown')
            self.assertEqual(test_resp[1], 200)
            self.assertEqual(test_resp[0].get('message'), 'Item(s) retrieved')
            self.assertGreater(len(test_resp[0].get('item')), 0)

            test_resp = pass_get_bystatus(status='some')
            self.assertEqual(test_resp[1], 404)
            self.assertEqual(test_resp[0].get('message'), 'Item(s) not found')
            self.assertEqual(len(test_resp[0].get('item')), 0)

    def test_pass_get_by_id(self):
        with TestCrud.app.app_context():
            test_resp = pass_get_byid(passid=2)
            self.assertEqual(test_resp[1], 200)
            self.assertEqual(test_resp[0].get('message'), 'Item(s) retrieved')
            self.assertGreater(len(test_resp[0].get('item')), 0)

            test_resp = pass_get_byid(passid=10000)
            self.assertEqual(test_resp[1], 404)
            self.assertEqual(test_resp[0].get('message'), 'Item(s) not found')
            self.assertEqual(len(test_resp[0].get('item')), 0)

    def test_pass_getall_list(self):
        with TestCrud.app.app_context():
            test_resp = pass_getall_list()
            total_pass = len(pass_get_bystatus()[0].get('item'))
            self.assertEqual(type(test_resp), dict)
            self.assertIn('all', test_resp)
            self.assertEqual(len(test_resp), total_pass + 1)

    def test_pass_post(self):
        test_payload = {
                'fname': 'Test',
                'lname': 'Tester',
                'seatno': '33A',
                'address': '',
                'dob': '1980-12-31',
                'status': 'dead',
                'comments': ''}

        test_invalid_payload = {
                'fname': 'Test',
                'lname': 'Tester',
                'seatno': '334',
                'address': '',
                'dob': '1980-12-31',
                'status': 'dead',
                'comments': ''}

        with TestCrud.app.app_context():
            test_resp = pass_post(payload=test_payload)
            self.assertEqual(test_resp[1], 200)
            self.assertEqual(test_resp[0].get('message'), 'Item created')
            self.assertEqual(len(test_resp[0].get('item')), 8)

            test_resp = pass_post(payload=test_payload, pass_id=2)
            self.assertEqual(test_resp[1], 200)
            self.assertEqual(test_resp[0].get('message'), 'Item updated')
            self.assertEqual(len(test_resp[0].get('item')), 8)

            test_resp = pass_post(payload=test_payload, pass_id=10000)
            self.assertEqual(test_resp[1], 404)
            self.assertEqual(test_resp[0].get('message'), 'Item(s) not found')
            self.assertEqual(len(test_resp[0].get('item')), 0)

            test_resp = pass_post(payload=test_invalid_payload)
            self.assertEqual(test_resp[1], 400)
            self.assertIn('Incorrect payload', test_resp[0].get('message'))

    def test_pass_delete(self):
        with TestCrud.app.app_context():
            test_resp = pass_delete(pass_id=10000)
            self.assertEqual(test_resp[1], 404)
            self.assertEqual(test_resp[0].get('message'), 'Item(s) not found')

            test_resp = pass_delete(pass_id=1)
            self.assertEqual(test_resp[1], 200)
            self.assertEqual(test_resp[0].get('message'), 'Item deleted')
            self.assertEqual(len(test_resp[0].get('item')), 8)

