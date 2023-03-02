"""Tests for Event API module"""
import unittest
from unittest.mock import patch
from manifestapp import create_app


class TestSimpleTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    @patch('manifestapp.rest.event_api.event_get_bypass')
    def test_get_all_events(self, mock_get_events):
        test_func_resp = [{
            'message': 'all is good',
            'item': [{
                "id": 2,
                "date": "2022-08-08",
                "passengerID": 4,
                "geo_location": "-10.344, 140.031",
                "description": "I see the starts shining",
                "status": "success",
                "other_pass": "1,3",
                "comments": "ddd"
            },
            {
                "id": 3,
                "date": "2022-10-10",
                "passengerID": 5,
                "geo_location": "-15.344, 120.031",
                "description": "I see the 2 dogs but I feel there are much more",
                "status": "success",
                "other_pass": "1,2,4",
                "comments": ""
            }]
        }, 200]
        mock_get_events.return_value = test_func_resp
        
        test_resp = self.client.get('/eventapi')
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

