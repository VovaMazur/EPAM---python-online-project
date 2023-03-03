"""Tests for components"""
import unittest
from manifestapp import create_app, db
from manifestapp.models import Event, Passenger
from .data2 import t_passes, t_events


class TestViews(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('TestViews setup')
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

            print('Number of event records', len(Event.query.all()))
            print('Number of pass records', len(Passenger.query.all()))


        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        print('TestViews teardown')
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_main_routes_get(self):
        test_resp = TestViews.client.get('/')
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')

        test_resp = TestViews.client.get('/events/')
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')

        test_resp = TestViews.client.get('/passengers/')
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')

    def test_main_routes_post(self):
        # Events View
        test_form_data = {'filter': 'all'}
        test_resp = TestViews.client.post('/events/', data=test_form_data)
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')

        test_form_data = {'filter': 1}
        test_resp = TestViews.client.post('/events/', data=test_form_data)
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')

        test_form_data = {
                    'filter': 'all',
                    'datefrom': '2022-01-01'}
        test_resp = TestViews.client.post('/events/', data=test_form_data)
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')

        test_form_data = {
                    'filter': 'all',
                    'dateto': '2023-01-31'}
        test_resp = TestViews.client.post('/events/', data=test_form_data)
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')

        test_form_data = {
                    'filter': 'all',
                    'datefrom': '2022-01-01',
                    'dateto': '2023-01-31'}
        test_resp = TestViews.client.post('/events/', data=test_form_data)
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')

        test_form_data = {
                    'filter': 1,
                    'datefrom': '2022-01-01',
                    'dateto': '2023-01-31'}
        test_resp = TestViews.client.post('/events/', data=test_form_data)
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')


        #Passengers View
        test_form_data = {'selected_status': 'unknown'}
        test_resp = TestViews.client.post('/passengers/', data=test_form_data)
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')

        test_form_data = {'selected_status': 'all'}
        test_resp = TestViews.client.post('/passengers/', data=test_form_data)
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')

    def test_edit_routes_get(self):
        test_resp = TestViews.client.get('/events/edit/add')
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')

        with TestViews.app.app_context():
            item = Event.query.first().id
        test_resp = TestViews.client.get(f'/events/edit/{item}')
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')

        test_resp = TestViews.client.get('/passengers/edit/add')
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')

        with TestViews.app.app_context():
            item = Passenger.query.first().id
        test_resp = TestViews.client.get(f'/passengers/edit/{item}')
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')

    def test_edit_routes_post(self):
        #add new event
        test_form_data = {
                    'date': '2022-12-15',
                    'passengerID': 1,
                    'geo_location': '12.45, 23.45',
                    'description': 'auto testing dummy descp',
                    'status': 'success',
                    'other_pass': '',
                    'comments': ''}
        test_resp = TestViews.client.post('/events/edit/add', data=test_form_data)
        self.assertEqual(test_resp.status_code, 302)
        self.assertEqual(test_resp.mimetype, 'text/html')
        self.assertIn(test_resp.headers['Location'], '/events/')

        # add new passenger
        test_form_data = {
                    'fname': 'Test',
                    'lname': 'Tester',
                    'seatno': '33A',
                    'address': '',
                    'dob': '1980-12-31',
                    'status': 'dead',
                    'comments': ''}
        test_resp = TestViews.client.post('/passengers/edit/add', data=test_form_data)
        self.assertEqual(test_resp.status_code, 302)
        self.assertEqual(test_resp.mimetype, 'text/html')
        self.assertIn(test_resp.headers['Location'], '/passengers/')

        # update event
        with TestViews.app.app_context():
            item = Event.query.first().id
        test_form_data = {
                    'date': '2022-12-15',
                    'passengerID': 1,
                    'geo_location': '12.45, 23.45',
                    'description': 'auto testing dummy descp',
                    'status': 'success',
                    'other_pass': '',
                    'comments': 'HUGE UPDATE'}
        test_resp = TestViews.client.post(f'/events/edit/{item}', data=test_form_data)
        self.assertEqual(test_resp.status_code, 302)
        self.assertEqual(test_resp.mimetype, 'text/html')
        self.assertIn(test_resp.headers['Location'], '/events/')

        # update passenger
        with TestViews.app.app_context():
            item = Passenger.query.first().id
        test_form_data = {
                    'fname': 'Test',
                    'lname': 'Tester',
                    'seatno': '33A',
                    'address': '',
                    'dob': '',
                    'status': 'dead',
                    'comments': 'HUGE UPDATE'}
        test_resp = TestViews.client.post(f'/passengers/edit/{item}', data=test_form_data)
        self.assertEqual(test_resp.status_code, 302)
        self.assertEqual(test_resp.mimetype, 'text/html')
        self.assertIn(test_resp.headers['Location'], '/passengers/')

        # add event with invalid data
        test_form_data = {
                    'date': '2022-12-15',
                    'passengerID': 1,
                    'geo_location': '12.45 // 23.45',  #error here
                    'description': 'auto testing dummy descp',
                    'status': 'success',
                    'other_pass': '',
                    'comments': ''}
        test_resp = TestViews.client.post('/events/edit/add', data=test_form_data)
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')
        err_msg = 'class="error"'
        self.assertIn(err_msg, test_resp.get_data(as_text=True))

        # add passenger with invalid data
        test_form_data = {
                    'fname': 'Test',
                    'lname': 'Tester',
                    'seatno': '333',   #error here
                    'address': '',
                    'dob': '',
                    'status': 'dead',
                    'comments': ''}
        test_resp = TestViews.client.post('/passengers/edit/add', data=test_form_data)
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')
        err_msg = 'class="error"'
        self.assertIn(err_msg, test_resp.get_data(as_text=True))

    def test_delete_routes_post(self):
        test_resp = TestViews.client.get('/events/delete/3')
        self.assertEqual(test_resp.status_code, 302)
        self.assertEqual(test_resp.mimetype, 'text/html')
        self.assertIn(test_resp.headers['Location'], '/events/')

        test_resp = TestViews.client.get('/events/delete/10000')
        self.assertEqual(test_resp.status_code, 302)
        self.assertEqual(test_resp.mimetype, 'text/html')
        self.assertIn(test_resp.headers['Location'], '/events/')

        test_resp = TestViews.client.get('/passengers/delete/3')
        self.assertEqual(test_resp.status_code, 302)
        self.assertEqual(test_resp.mimetype, 'text/html')
        self.assertIn(test_resp.headers['Location'], '/passengers/')

        test_resp = TestViews.client.get('/passengers/delete/10000')
        self.assertEqual(test_resp.status_code, 302)
        self.assertEqual(test_resp.mimetype, 'text/html')
        self.assertIn(test_resp.headers['Location'], '/passengers/')

        test_resp = TestViews.client.get('/passengers/delete/1')
        self.assertEqual(test_resp.status_code, 302)
        self.assertEqual(test_resp.mimetype, 'text/html')
        self.assertIn(test_resp.headers['Location'], '/passengers/')