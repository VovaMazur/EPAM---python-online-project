"""Tests for Event API module"""
import unittest
from unittest.mock import patch
from manifestapp import create_app


class TestEventAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_get_method_invalid_dates(self):
        test_resp = TestEventAPI.client.get('/eventapi/all/-/2023-01-32')
        self.assertEqual(test_resp.status_code, 400)
        self.assertEqual(test_resp.json.get('message'), 'Date parameter should be a valid date, format YYYY-MM-DD')

        test_resp = TestEventAPI.client.get('/eventapi/all/-/-/2023-02-31')
        self.assertEqual(test_resp.status_code, 400)
        self.assertEqual(test_resp.json.get('message'), 'Date parameter should be a valid date, format YYYY-MM-DD')

    @patch('manifestapp.rest.event_api.event_get_bypass')
    def test_get_method_all_events(self, mock_get_all_f):
        mock_get_all_f.side_effect = [
            [{'message': 'Item(s) not found', 'item': {}}, 404],
            [{'message': 'Item(s) retrieved', 'item': [{
                'id': 1,
                'date': '2022-12-15',
                'passengerID': 1,
                'geo_location': '12.45, 23.45',
                'description': 'auto testing dummy descp',
                'status': 'success',
                'other_pass': '',
                'comments': ''},
                 {'id': 2,
                'date': '2022-12-15',
                'passengerID': 1,
                'geo_location': '12.45, 23.45',
                'description': 'auto testing dummy descp',
                'status': 'success',
                'other_pass': '',
                'comments': ''}]
              }, 200]
        ]
        test_resp = TestEventAPI.client.get('/eventapi/all/10000/2022-01-01')
        self.assertEqual(test_resp.status_code, 404)
        self.assertEqual(test_resp.json.get('message'), 'Item(s) not found')
        self.assertEqual(test_resp.json.get('item'), {})

        test_resp = TestEventAPI.client.get('/eventapi/all/all/2022-01-01/2023-03-06')
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.json.get('message'), 'Item(s) retrieved')
        self.assertEqual(len(test_resp.json.get('item')), 2)

    @patch('manifestapp.rest.event_api.event_get_byid')
    def test_get_method_specific_event(self, mock_get_id_f):
        mock_get_id_f.side_effect = [
            [{'message': 'Item(s) not found', 'item': {}}, 404],
            [{'message': 'Item(s) retrieved', 'item': {
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
        test_resp = TestEventAPI.client.get('/eventapi/10000')
        self.assertEqual(test_resp.status_code, 404)
        self.assertEqual(test_resp.json.get('message'), 'Item(s) not found')
        self.assertEqual(test_resp.json.get('item'), {})

        test_resp = TestEventAPI.client.get('/eventapi/1')
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.json.get('message'), 'Item(s) retrieved')
        self.assertEqual(len(test_resp.json.get('item')), 8)

    @patch('manifestapp.rest.event_api.event_delete')
    def test_delete_method(self, mock_delete_f):
        mock_delete_f.side_effect = [
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
        test_resp = TestEventAPI.client.delete('/eventapi/10000')
        self.assertEqual(test_resp.status_code, 404)
        self.assertEqual(test_resp.json.get('message'), 'Item(s) not found')

        test_resp = TestEventAPI.client.delete('/eventapi/1')
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.json.get('message'), 'Item deleted')
        self.assertEqual(test_resp.json.get('item').get('id'), 1)

    @patch('manifestapp.rest.event_api.event_post')
    def test_post_method(self, mock_post_f):
        mock_post_f.side_effect = [
            [{'message': 'Item (s) not found', 'item': {}}, 404],
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
                'comments': ''}}, 200]
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

        test_resp = TestEventAPI.client.post('/eventapi/10000', json=test_payload)
        self.assertEqual(test_resp.status_code, 404)
        self.assertEqual(test_resp.json.get('message'), 'Item (s) not found')
        self.assertEqual(test_resp.json.get('item'), {})

        test_resp = TestEventAPI.client.post('/eventapi', json=test_payload)
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.json.get('message'), 'Item created')
        self.assertEqual(len(test_resp.json.get('item')), 8)
        item_created_withoutid = test_resp.json.get('item')
        item_created_withoutid.pop('id')
        self.assertEqual(item_created_withoutid, test_payload)

        test_resp = TestEventAPI.client.post('/eventapi/1', json=test_payload)
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.json.get('message'), 'Item updated')
        self.assertEqual(len(test_resp.json.get('item')), 8)
        item_updated_withoutid = test_resp.json.get('item')
        item_updated_withoutid.pop('id')
        self.assertEqual(item_updated_withoutid, test_payload)

    @patch('manifestapp.rest.event_api.event_get_summary')
    def test_get_summary(self, mock_get_summary):
        mock_get_summary.return_value = {
            '1': 1,
            '2': 1
        }

        test_resp = TestEventAPI.client.get('/eventsummaryapi')
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.json, {
            '1': 1,
            '2': 1
        })