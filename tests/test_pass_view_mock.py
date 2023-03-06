"""Tests for components"""
import unittest
from unittest.mock import patch
from manifestapp import create_app


class TestPassView(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    @patch('manifestapp.views.passengers_view.event_get_summary')
    @patch('manifestapp.views.passengers_view.pass_get_bystatus')
    def test_main_route(self, mock_getpasses, mock_get_summary):
        mock_get_summary.return_value = {
            1: 2,
            2: 1
        }

        mock_getpasses.side_effect = [
            [{'message': 'Item(s) retrieved', 'item': [{
                "id": 1,
                "fname": "Ben",
                "lname": "Stone",
                "seatno": "12C",
                "address": "NY, Some place",
                "dob": "1980-01-23",
                "status": "live",
                "comments": ""
            }, {
                "id": 2,
                "fname": "Mac",
                "lname": "Stone",
                "seatno": "12A",
                "address": "NY, Some other place",
                "dob": "1985-04-19",
                "status": "some",
                "comments": ""
            }]}, 200],
            [{'message': 'Item(s) retrieved', 'item': [{
                "id": 2,
                "fname": "Mac",
                "lname": "Stone",
                "seatno": "12A",
                "address": "NY, Some other place",
                "dob": "1985-04-19",
                "status": "some",
                "comments": ""
            }]}, 200],
            [{'message': 'Item(s) not found', 'item': {}}, 404]
        ]

        test_resp = TestPassView.client.get('/passengers/')
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')
        self.assertIn('''<td>1</td>
                <td>Ben</td>
                <td>Stone</td>
                <td>12C</td>
                <td>NY, Some place</td>
                <td>1980-01-23</td>
                <td>live</td>
                <td>2</td>''', test_resp.text)

        test_form_data = {'selected_status': 'some'}
        test_resp = TestPassView.client.post('/passengers/', data=test_form_data)
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')
        self.assertNotIn('''<td>1</td>
                <td>Ben</td>
                <td>Stone</td>
                <td>12C</td>
                <td>NY, Some place</td>
                <td>1980-01-23</td>
                <td>live</td>
                <td>2</td>''', test_resp.text)

        test_form_data = {'selected_status': 'invalid'}
        test_resp = TestPassView.client.post('/passengers/', data=test_form_data)
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')

    @patch('manifestapp.views.passengers_view.pass_get_byid')
    def test_edit_route_get(self, mock_getpass):
        mock_getpass.return_value = [{'message': 'Item(s) retrieved', 'item': {
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

        test_resp = TestPassView.client.get('/passengers/edit/1')
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')
        self.assertIn('value="Ben"', test_resp.text)
        self.assertIn('value="Stone"', test_resp.text)
        self.assertIn('value="12C"', test_resp.text)
        self.assertIn('value="NY, Some place"', test_resp.text)
        self.assertIn('value="1980-01-23"', test_resp.text)
        self.assertIn('''<option value="live"
                    
                        selected="selected"
                    
                >Live</option>''', test_resp.text)

        test_resp = TestPassView.client.get('/passengers/edit/add')
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')

    @patch('manifestapp.views.passengers_view.pass_post')
    def test_edit_route_post(self, mock_postpass):
        mock_postpass.side_effect = [
            [{'message': 'Item created', 'item': {
                "id": 50,
                "fname": "Test",
                "lname": "Tester",
                "seatno": "33A",
                "address": "",
                "dob": "1980-01-01",
                "status": "dead",
                "comments": ""
            }}, 200],
            [{'message': 'Item updated', 'item': {
                "id": 1,
                "fname": "Test",
                "lname": "Tester",
                "seatno": "33A",
                "address": "",
                "dob": "1980-01-01",
                "status": "dead",
                "comments": ""
            }}, 200],
            [{'message': 'Incorrect payload', 'item': {}}, 400]
        ]

        test_payload = {
                "fname": "Test",
                "lname": "Tester",
                "seatno": "33A",
                "address": "",
                "dob": "1980-01-01",
                "status": "dead",
                "comments": ""
            }

        test_invalid_payload = {
                "fname": "Test",
                "lname": "Tester",
                "seatno": "333",
                "address": "",
                "dob": "",
                "status": "dead",
                "comments": ""
            }

        test_resp = TestPassView.client.post('/passengers/edit/add', data=test_payload)
        self.assertEqual(test_resp.status_code, 302)
        self.assertEqual(test_resp.mimetype, 'text/html')
        self.assertEqual(test_resp.headers['Location'], "/passengers/")

        test_resp = TestPassView.client.post('/passengers/edit/1', data=test_payload)
        self.assertEqual(test_resp.status_code, 302)
        self.assertEqual(test_resp.mimetype, 'text/html')
        self.assertEqual(test_resp.headers['Location'], "/passengers/")

        test_resp = TestPassView.client.post('/passengers/edit/add', data=test_invalid_payload)
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')
        self.assertIn('div id="div_flash" class="error"', test_resp.text)

    @patch('manifestapp.views.passengers_view.event_get_summary')
    @patch('manifestapp.views.passengers_view.pass_delete')
    def test_delete_route(self, mock_pass_delete_f, mock_get_summary):
        mock_pass_delete_f.side_effect = [
            [{'message': 'Item(s) not found', 'item': {}}, 404],
            [{'message': 'Item deleted', 'item': {
                "id": 3,
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

        mock_get_summary.return_value = {
            1: 2,
            2: 1
        }

        test_resp = TestPassView.client.get('/passengers/delete/10000')
        self.assertEqual(test_resp.status_code, 302)
        self.assertEqual(test_resp.mimetype, 'text/html')
        self.assertEqual(test_resp.headers['Location'], "/passengers/")

        test_resp = TestPassView.client.get('/passengers/delete/3')
        self.assertEqual(test_resp.status_code, 302)
        self.assertEqual(test_resp.mimetype, 'text/html')
        self.assertEqual(test_resp.headers['Location'], "/passengers/")

        test_resp = TestPassView.client.get('/passengers/delete/1')
        self.assertEqual(test_resp.status_code, 302)
        self.assertEqual(test_resp.mimetype, 'text/html')
        self.assertEqual(test_resp.headers['Location'], "/passengers/")

