"""Tests for components"""
import unittest
import responses
from manifestapp import create_app
from manifestapp.views.events_view import main, edit, delete


class TestEvView(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()

    @responses.activate
    def test_main_route(self):
        responses.get(
            url='http://localhost//passlistapi',
            json={
            'all': 'All',
            1: 'Mack Macker',
            2: 'Test Tester',
            3: 'Mack Mackerson'
        },
            status=200)

        responses.get(
            url='http://localhost//eventapi/all/all/-/-',
            json={'message': 'Item(s) retrieved', 'item': [
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
                'comments': ''}]},
            status=200)

        with TestEvView.app.test_request_context():
            test_resp = main()
            self.assertIn('Registered callings of passenger(s): All', test_resp)
            self.assertIn('''<td>1</td>
                <td>2022-12-15</td>
                <td>Mack Macker</td>
                <td>12.45, 23.45</td>
                <td>auto testing dummy descp</td>
                <td>success</td>''', test_resp)

        responses.get(
            url='http://localhost//eventapi/all/2/-/-',
            json={'message': 'Item(s) retrieved', 'item': [
            {
                'id': 2,
                'date': '2022-12-15',
                'passengerID': 1,
                'geo_location': '12.45, 23.45',
                'description': 'auto testing dummy descp',
                'status': 'success',
                'other_pass': '',
                'comments': ''}]},
            status=200)

        test_form_data = {'filter': 2}
        with TestEvView.app.test_request_context(method='POST', data=test_form_data):
            test_resp = main()
            self.assertIn('Registered callings of passenger(s): Test Tester', test_resp)
            self.assertNotIn('''<td>1</td>
                <td>2022-12-15</td>
                <td>Mack Macker</td>
                <td>12.45, 23.45</td>
                <td>auto testing dummy descp</td>
                <td>success</td>''', test_resp)

        responses.get(
            url='http://localhost//eventapi/all/3/-/-',
            json={'message': 'Item(s) not found', 'item': {}},
            status=404)

        test_form_data = {'filter': 3}
        with TestEvView.app.test_request_context(method='POST', data=test_form_data):
            test_resp = main()
            self.assertIn('Registered callings of passenger(s): Mack Mackerson', test_resp)
            self.assertIn('''<tbody>
            
        </tbody>''', test_resp)

    @responses.activate
    def test_edit_route_get(self):
        responses.get(
            url='http://localhost//passlistapi',
            json={
                'all': 'All',
                1: 'Mack Macker',
                2: 'Test Tester'
                },
            status=200)

        responses.get(
            url='http://localhost//eventapi/1',
            json={'message': 'Item(s) retrieved', 'item':
                {
                'id': 1,
                'date': '2022-12-15',
                'passengerID': 1,
                'geo_location': '12.45, 23.45',
                'description': 'auto testing dummy descp',
                'status': 'success',
                'other_pass': '1',
                'comments': ''}},
            status=200)

        with TestEvView.app.test_request_context():
            test_resp = edit('add')
            self.assertIn('form action="/events/edit/add" id="event-details" method="POST"', test_resp)

            test_resp = edit('1')
            self.assertIn('form action="/events/edit/1" id="event-details" method="POST"', test_resp)
            self.assertIn('value="2022-12-15"', test_resp)
            self.assertIn('''<option value="1"
                            
                                selected="selected"
                            >
                        Mack Macker</option>''', test_resp)
            self.assertIn('value="12.45, 23.45"', test_resp)
            self.assertIn('value="auto testing dummy descp"', test_resp)
            self.assertIn('''<option value="success"
                            
                                selected="selected"
                            >Success</option>''', test_resp)

        test_payload = {
            'date': '2022-12-15',
            'passengerID': 1,
            'geo_location': '12.45, 23.45',
            'description': 'auto testing dummy descp',
            'status': 'success',
            'other_pass': '',
            'comments': ''
        }

        responses.post(
            url='http://localhost//eventapi/1',
            json={'message': 'Item updated', 'item': {
                'id': 1,
                'date': '2022-12-15',
                'passengerID': 1,
                'geo_location': '12.45, 23.45',
                'description': 'auto testing dummy descp',
                'status': 'success',
                'other_pass': '',
                'comments': ''}},
            status=200)

        responses.post(
            url='http://localhost//eventapi',
            json={'message': 'Item created', 'item': {
                'id': 30,
                'date': '2022-12-15',
                'passengerID': 1,
                'geo_location': '12.45, 23.45',
                'description': 'auto testing dummy descp',
                'status': 'success',
                'other_pass': '',
                'comments': ''}},
            status=200)

        with TestEvView.app.test_request_context(method='POST', data=test_payload):
            test_resp = edit('1')
            self.assertEqual(test_resp.status_code, 302)
            self.assertEqual(test_resp.mimetype, 'text/html')
            self.assertEqual(test_resp.headers['Location'], "/events/")

            test_resp = edit('add')
            self.assertEqual(test_resp.status_code, 302)
            self.assertEqual(test_resp.mimetype, 'text/html')
            self.assertEqual(test_resp.headers['Location'], "/events/")


        test_invalid_payload = {
            'date': '2022-12-15',
            'passengerID': 1,
            'geo_location': '12.45 / 23.45',
            'description': 'auto testing dummy descp',
            'status': 'success',
            'other_pass': '',
            'comments': ''
        }

        responses.post(
            url='http://localhost//eventapi',
            json={'message': 'Incorrect payload', 'item': {}},
            status=400)

        with TestEvView.app.test_request_context(method='POST', data=test_invalid_payload):
            test_resp = edit('add')
            self.assertIn('div id="div_flash" class="error"', test_resp)
            self.assertIn('form action="/events/edit/add" id="event-details" method="POST', test_resp)
            self.assertIn('value="2022-12-15"', test_resp)
            self.assertIn('''<option value="1"
                            
                                selected="selected"
                            >
                        Mack Macker</option>''', test_resp)
            self.assertIn('value="12.45 / 23.45"', test_resp)
            self.assertIn('value="auto testing dummy descp"', test_resp)
            self.assertIn('''<option value="success"
                            
                                selected="selected"
                            >Success</option>''', test_resp)

    @responses.activate
    def test_delete_route(self):
        responses.delete(
            url='http://localhost//eventapi/10000',
            json={'message': 'Item(s) not found', 'item': {}},
            status=404)

        responses.delete(
            url='http://localhost//eventapi/1',
            json={'message': 'Item deleted', 'item': {
                'id': 1,
                'date': '2022-12-15',
                'passengerID': 1,
                'geo_location': '12.45, 23.45',
                'description': 'auto testing dummy descp',
                'status': 'success',
                'other_pass': '',
                'comments': ''}
              },
            status=200)

        with TestEvView.app.test_request_context():
            test_resp = delete('10000')
            self.assertEqual(test_resp.status_code, 302)
            self.assertEqual(test_resp.mimetype, 'text/html')
            self.assertEqual(test_resp.headers['Location'], "/events/")

            test_resp = delete('1')
            self.assertEqual(test_resp.status_code, 302)
            self.assertEqual(test_resp.mimetype, 'text/html')
            self.assertEqual(test_resp.headers['Location'], "/events/")
