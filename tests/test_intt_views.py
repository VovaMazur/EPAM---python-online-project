"""Tests for Event view"""
import unittest
from manifestapp import create_app


class TestViews(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    def test_main_routes_get(self):
        test_resp = self.client.get('/events/')
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')

        test_resp = self.client.get('/passengers/')
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')

    def test_main_routes_post(self):
        # Events View
        test_form_data = {'filter': 'all'}
        test_resp = self.client.post('/events/', data=test_form_data)
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')

        test_form_data = {'filter': 1}
        test_resp = self.client.post('/events/', data=test_form_data)
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')

        test_form_data = {
                    'filter': 'all',
                    'datefrom': '2022-01-01'}
        test_resp = self.client.post('/events/', data=test_form_data)
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')

        test_form_data = {
                    'filter': 'all',
                    'dateto': '2023-01-31'}
        test_resp = self.client.post('/events/', data=test_form_data)
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')

        test_form_data = {
                    'filter': 'all',
                    'datefrom': '2022-01-01',
                    'dateto': '2023-01-31'}
        test_resp = self.client.post('/events/', data=test_form_data)
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')

        test_form_data = {
                    'filter': 1,
                    'datefrom': '2022-01-01',
                    'dateto': '2023-01-31'}
        test_resp = self.client.post('/events/', data=test_form_data)
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')


        #Passengers View
        test_form_data = {'selected_status': 'unknown'}
        test_resp = self.client.post('/passengers/', data=test_form_data)
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')

        test_form_data = {'selected_status': 'all'}
        test_resp = self.client.post('/passengers/', data=test_form_data)
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')

    def test_edit_routes_get(self):
        test_resp = self.client.get('/events/edit/add')
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')

        test_resp = self.client.get('/events/edit/2')
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')

        test_resp = self.client.get('/passengers/edit/add')
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')

        test_resp = self.client.get('/passengers/edit/1')
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')

    def test_edit_routes_post(self):
        test_form_data = {
                    'date': '2022-12-15',
                    'passengerID': 1,
                    'geo_location': '12.45, 23.45',
                    'description': 'auto testing dummy descp',
                    'status': 'success',
                    'other_pass': '',
                    'comments': ''}
        test_resp = self.client.post('/events/edit/add', data=test_form_data)
        self.assertEqual(test_resp.status_code, 302)
        self.assertEqual(test_resp.mimetype, 'text/html')


        test_form_data = {
                    'fname': 'Test',
                    'lname': 'Tester',
                    'seatno': '33A',
                    'address': '',
                    'dob': '',
                    'status': 'dead',
                    'comments': ''}
        test_resp = self.client.post('/passengers/edit/add', data=test_form_data)
        self.assertEqual(test_resp.status_code, 302)
        self.assertEqual(test_resp.mimetype, 'text/html')

        test_form_data = {
                    'date': '2022-12-15',
                    'passengerID': 1,
                    'geo_location': '12.45, 23.45',
                    'description': 'auto testing dummy descp',
                    'status': 'success',
                    'other_pass': '',
                    'comments': 'HUGE UPDATE'}
        test_resp = self.client.post('/events/edit/143', data=test_form_data)
        self.assertEqual(test_resp.status_code, 302)
        self.assertEqual(test_resp.mimetype, 'text/html')

        test_form_data = {
                    'fname': 'Test',
                    'lname': 'Tester',
                    'seatno': '33A',
                    'address': '',
                    'dob': '',
                    'status': 'dead',
                    'comments': 'HUGE UPDATE'}
        test_resp = self.client.post('/passengers/edit/55', data=test_form_data)
        self.assertEqual(test_resp.status_code, 302)
        self.assertEqual(test_resp.mimetype, 'text/html')

        test_form_data = {
                    'date': '2022-12-15',
                    'passengerID': 1,
                    'geo_location': '12.45 // 23.45',
                    'description': 'auto testing dummy descp',
                    'status': 'success',
                    'other_pass': '',
                    'comments': ''}
        test_resp = self.client.post('/events/edit/add', data=test_form_data)
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')
        err_msg = 'class="error"'
        self.assertIn(err_msg, test_resp.get_data(as_text=True))

        test_form_data = {
                    'fname': 'Test',
                    'lname': 'Tester',
                    'seatno': '333',
                    'address': '',
                    'dob': '',
                    'status': 'dead',
                    'comments': ''}
        test_resp = self.client.post('/passengers/edit/add', data=test_form_data)
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')
        err_msg = 'class="error"'
        self.assertIn(err_msg, test_resp.get_data(as_text=True))


    def test_delete_routes_post(self):
        # test_resp = self.client.get('/events/delete/139')
        # self.assertEqual(test_resp.status_code, 302)
        # self.assertEqual(test_resp.mimetype, 'text/html')

        test_resp = self.client.get('/events/delete/10000')
        self.assertEqual(test_resp.status_code, 302)
        self.assertEqual(test_resp.mimetype, 'text/html')

        # test_resp = self.client.get('/passengers/delete/51')
        # self.assertEqual(test_resp.status_code, 302)
        # self.assertEqual(test_resp.mimetype, 'text/html')

        test_resp = self.client.get('/passengers/delete/10000')
        self.assertEqual(test_resp.status_code, 302)
        self.assertEqual(test_resp.mimetype, 'text/html')
