"""Tests for components"""
import unittest
from unittest.mock import patch
from manifestapp import create_app


class TestEvView(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    @patch('manifestapp.views.events_view.event_get_bypass')
    @patch('manifestapp.views.events_view.pass_getall_list')
    def test_main_route(self, mock_getpasses, mock_getevents):
        mock_getpasses.return_value = {
            'all': 'All',
            1: 'Mack Macker',
            2: 'Test Tester'
        }
        mock_getevents.side_effect = [[{'message': 'Item(s) retrieved', 'item': [
            {
                'id': 1,
                'date': '2022-12-15',
                'passengerID': 1,
                'geo_location': '12.45, 23.45',
                'description': 'auto testing dummy descp',
                'status': 'success',
                'other_pass': '',
                'comments': ''},
            {
                'id': 2,
                'date': '2022-12-15',
                'passengerID': 1,
                'geo_location': '12.45, 23.45',
                'description': 'auto testing dummy descp',
                'status': 'success',
                'other_pass': '',
                'comments': ''}]
              }, 200],
              [{'message': 'Item(s) retrieved', 'item': [{
                      'id': 2,
                      'date': '2022-12-15',
                      'passengerID': 1,
                      'geo_location': '12.45, 23.45',
                      'description': 'auto testing dummy descp',
                      'status': 'success',
                      'other_pass': '',
                      'comments': ''}]
                }, 200]
            ]

        test_resp = TestEvView.client.get('/events/')
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')
        self.assertIn('''                <td>1</td>
                <td>2022-12-15</td>
                <td>Mack Macker</td>
                <td>12.45, 23.45</td>
                <td>auto testing dummy descp</td>
                <td>success</td>
                <td></td>''', test_resp.text)

        test_form_data = {'filter': 2}
        test_resp = TestEvView.client.post('/events/', data=test_form_data)
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')
        self.assertNotIn('''                <td>1</td>
                <td>2022-12-15</td>
                <td>Mack Macker</td>
                <td>12.45, 23.45</td>
                <td>auto testing dummy descp</td>
                <td>success</td>
                <td></td>''', test_resp.text)

    @patch('manifestapp.views.events_view.event_get_byid')
    @patch('manifestapp.views.events_view.pass_getall_list')
    def test_edit_route_get(self, mock_getpasses, mock_getevent):
        mock_getpasses.return_value = {
            'all': 'All',
            1: 'Mack Macker',
            2: 'Test Tester'
        }
        mock_getevent.return_value = [{'message': 'Item(s) retrieved', 'item':
            {
                'id': 1,
                'date': '2022-12-15',
                'passengerID': 1,
                'geo_location': '12.45, 23.45',
                'description': 'auto testing dummy descp',
                'status': 'success',
                'other_pass': '1',
                'comments': ''}}, 200]

        test_resp = TestEvView.client.get('/events/edit/1')
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')
        self.assertIn('value="2022-12-15"', test_resp.text)
        self.assertIn('''<option value="1"
                        
                            selected="selected"
                        >
                    Mack Macker</option>''', test_resp.text)
        self.assertIn('value="12.45, 23.45"', test_resp.text)
        self.assertIn('value="auto testing dummy descp"', test_resp.text)
        self.assertIn('''<option value="success"
                        
                            selected="selected"
                        >Success</option>''', test_resp.text)

    @patch('manifestapp.views.events_view.pass_getall_list')
    @patch('manifestapp.views.events_view.event_post')
    def test_edit_route_post(self, mock_postevent, mock_getpasses):
        mock_getpasses.return_value = {
            'all': 'All',
            1: 'Mack Macker',
            2: 'Test Tester'
        }

        mock_postevent.side_effect = [
            [{'message': 'Item created', 'item': {
                'id': 50,
                'date': '2022-12-15',
                'passengerID': 1,
                'geo_location': '12.45, 23.45',
                'description': 'auto testing dummy descp',
                'status': 'success',
                'other_pass': '',
                'comments': ''}}, 200],
            [{'message': 'Item updated', 'item': {
                'id': 1,
                'date': '2022-12-15',
                'passengerID': 1,
                'geo_location': '12.45, 23.45',
                'description': 'auto testing dummy descp',
                'status': 'success',
                'other_pass': '',
                'comments': ''}}, 200],
            [{'message': 'Incorrect payload', 'item': {}}, 400]
        ]

        test_payload = {
                'date': '2022-12-15',
                'passengerID': 1,
                'geo_location': '12.45, 23.45',
                'description': 'auto testing dummy descp',
                'status': 'success',
                'other_pass': '',
                'comments': ''
        }

        test_invalid_payload = {
                'date': '2022-12-15',
                'passengerID': 1,
                'geo_location': '12.45 / 23.45',
                'description': 'auto testing dummy descp',
                'status': 'success',
                'other_pass': '',
                'comments': ''
        }

        test_resp = TestEvView.client.post('/events/edit/add', data=test_payload)
        self.assertEqual(test_resp.status_code, 302)
        self.assertEqual(test_resp.mimetype, 'text/html')
        self.assertEqual(test_resp.headers['Location'], "/events/")

        test_resp = TestEvView.client.post('/events/edit/1', data=test_payload)
        self.assertEqual(test_resp.status_code, 302)
        self.assertEqual(test_resp.mimetype, 'text/html')
        self.assertEqual(test_resp.headers['Location'], "/events/")

        test_resp = TestEvView.client.post('/events/edit/add', data=test_invalid_payload)
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')
        self.assertIn('div id="div_flash" class="error"', test_resp.text)


    @patch('manifestapp.views.events_view.event_delete')
    def test_delete_route(self, mock_event_delete_f):
        mock_event_delete_f.side_effect = [
            [{'message': 'Item(s) not found', 'item': {}}, 404],
            [{'message': 'Item deleted', 'item': {
                'id': 1,
                'date': '2022-12-15',
                'passengerID': 1,
                'geo_location': '12.45, 23.45',
                'description': 'auto testing dummy descp',
                'status': 'success',
                'other_pass': '',
                'comments': ''}
              }, 200]
        ]

        test_resp = TestEvView.client.get('/events/delete/10000')
        self.assertEqual(test_resp.status_code, 302)
        self.assertEqual(test_resp.mimetype, 'text/html')
        self.assertEqual(test_resp.headers['Location'], "/events/")

        test_resp = TestEvView.client.get('/events/delete/1')
        self.assertEqual(test_resp.status_code, 302)
        self.assertEqual(test_resp.mimetype, 'text/html')
        self.assertEqual(test_resp.headers['Location'], "/events/")
