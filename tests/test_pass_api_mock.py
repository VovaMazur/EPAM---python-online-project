"""Tests for Passenger API module"""
import unittest
from unittest.mock import patch
from manifestapp import create_app


class TestPassAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    @patch('manifestapp.rest.passenger_api.pass_get_bystatus')
    def test_get_method_all_pass(self, mock_get_all_f):
        mock_get_all_f.side_effect = [
            [{'message': 'Item(s) not found', 'item': {}}, 404],
            [{'message': 'Item(s) retrieved', 'item': [{
                "id": 1,
                "fname": "Ben",
                "lname": "Stone",
                "seatno": "12C",
                "address": "NY, Some place",
                "dob": "1980-01-23",
                "status": "live",
                "comments": ""
            },
            {
                "id": 2,
                "fname": "Mac",
                "lname": "Stone",
                "seatno": "12A",
                "address": "NY, Some other place",
                "dob": "1985-04-19",
                "status": "live",
                "comments": ""
            }]
              }, 200]
        ]
        test_resp = TestPassAPI.client.get('/passapi/all/something')
        self.assertEqual(test_resp.status_code, 404)
        self.assertEqual(test_resp.json.get('message'), 'Item(s) not found')
        self.assertEqual(test_resp.json.get('item'), {})

        test_resp = TestPassAPI.client.get('/passapi/all/live')
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.json.get('message'), 'Item(s) retrieved')
        self.assertEqual(len(test_resp.json.get('item')), 2)

    @patch('manifestapp.rest.passenger_api.pass_get_byid')
    def test_get_method_specific_pass(self, mock_get_id_f):
        mock_get_id_f.side_effect = [
            [{'message': 'Item(s) not found', 'item': {}}, 404],
            [{'message': 'Item(s) retrieved', 'item': {
                "id": 1,
                "fname": "Ben",
                "lname": "Stone",
                "seatno": "12C",
                "address": "NY, Some place",
                "dob": "1980-01-23",
                "status": "live",
                "comments": ""
            }
              }, 200]
        ]
        test_resp = TestPassAPI.client.get('/passapi/10000')
        self.assertEqual(test_resp.status_code, 404)
        self.assertEqual(test_resp.json.get('message'), 'Item(s) not found')
        self.assertEqual(test_resp.json.get('item'), {})

        test_resp = TestPassAPI.client.get('/passapi/1')
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.json.get('message'), 'Item(s) retrieved')
        self.assertEqual(len(test_resp.json.get('item')), 8)

    @patch('manifestapp.rest.passenger_api.pass_delete')
    def test_delete_method(self, mock_delete_f):
        mock_delete_f.side_effect = [
            [{'message': 'Item(s) not found', 'item': {}}, 404],
            [{'message': 'Item deleted', 'item': {
                "id": 1,
                "fname": "Ben",
                "lname": "Stone",
                "seatno": "12C",
                "address": "NY, Some place",
                "dob": "1980-01-23",
                "status": "live",
                "comments": ""
            }
              }, 200]
        ]
        test_resp = TestPassAPI.client.delete('/passapi/10000')
        self.assertEqual(test_resp.status_code, 404)
        self.assertEqual(test_resp.json.get('message'), 'Item(s) not found')

        test_resp = TestPassAPI.client.delete('/passapi/1')
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.json.get('message'), 'Item deleted')
        self.assertEqual(test_resp.json.get('item').get('id'), 1)

    @patch('manifestapp.rest.passenger_api.pass_post')
    def test_post_method(self, mock_post_f):
        mock_post_f.side_effect = [
            [{'message': 'Item (s) not found', 'item': {}}, 404],
            [{'message': 'Item created', 'item': {
                "id": 50,
                "fname": "Test",
                "lname": "Tester",
                "seatno": "33A",
                "address": "",
                "dob": "",
                "status": "dead",
                "comments": ""
            }}, 200],
            [{'message': 'Item updated', 'item': {
                "id": 1,
                "fname": "Test",
                "lname": "Tester",
                "seatno": "33A",
                "address": "",
                "dob": "",
                "status": "dead",
                "comments": ""
            }}, 200]
        ]

        test_payload = {
                "fname": "Test",
                "lname": "Tester",
                "seatno": "33A",
                "address": "",
                "dob": "",
                "status": "dead",
                "comments": ""
            }

        test_resp = TestPassAPI.client.post('/passapi/10000', json=test_payload)
        self.assertEqual(test_resp.status_code, 404)
        self.assertEqual(test_resp.json.get('message'), 'Item (s) not found')
        self.assertEqual(test_resp.json.get('item'), {})

        test_resp = TestPassAPI.client.post('/passapi', json=test_payload)
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.json.get('message'), 'Item created')
        self.assertEqual(len(test_resp.json.get('item')), 8)
        item_created_withoutid = test_resp.json.get('item')
        item_created_withoutid.pop('id')
        self.assertEqual(item_created_withoutid, test_payload)

        test_resp = TestPassAPI.client.post('/passapi/1', json=test_payload)
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.json.get('message'), 'Item updated')
        self.assertEqual(len(test_resp.json.get('item')), 8)
        item_updated_withoutid = test_resp.json.get('item')
        item_updated_withoutid.pop('id')
        self.assertEqual(item_updated_withoutid, test_payload)

    @patch('manifestapp.rest.passenger_api.pass_getall_list')
    def test_get_passlist(self, mock_passlist_f):
        mock_passlist_f.return_value = {
            'all': 'All',
            '1': 'Ben Stone',
            '2': 'Kel Stone'
        }

        test_resp = TestPassAPI.client.get('/passlistapi')
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.json, {
            'all': 'All',
            '1': 'Ben Stone',
            '2': 'Kel Stone'
        })
