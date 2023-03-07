"""Tests for components"""
import unittest
import responses
from manifestapp import create_app
from manifestapp.views.passengers_view import main, edit, delete


class TestPassView(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()

    @responses.activate
    def test_main_route(self):
        responses.get(
            url='http://localhost//eventsummaryapi',
            json={
                "1": 1,
                "2": 1},
            status=200
        )

        responses.get(
            url='http://localhost//passapi/all/all',
            json={'message': 'Item(s) retrieved', 'item': [{
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
            }]},
            status=200
        )

        responses.get(
            url='http://localhost//passapi/all/invalid',
            json={'message': 'Item(s) not found', 'item': {}},
            status=404
        )

        with TestPassView.app.test_request_context():
            test_resp = main()
            self.assertIn('''<td>1</td>
                <td>Ben</td>
                <td>Stone</td>
                <td>12C</td>
                <td>NY, Some place</td>
                <td>1980-01-23</td>
                <td>live</td>
                <td>1</td>''', test_resp)


        test_form_data = {'selected_status': 'invalid'}
        with TestPassView.app.test_request_context(method='POST', data=test_form_data):
            test_resp = main()
            self.assertIn('''        <tbody>
            
        </tbody>''', test_resp)

    @responses.activate
    def test_edit_route(self):
        # fill the edit form
        responses.get(
            url='http://localhost//passapi/1',
            json={'message': 'Item(s) retrieved', 'item': {
                "id": 1,
                "fname": "Ben",
                "lname": "Stone",
                "seatno": "12C",
                "address": "NY, Some place",
                "dob": "1980-01-23",
                "status": "live",
                "comments": ""
            }},
            status=200)

        with TestPassView.app.test_request_context():
            test_resp = edit('1')
            self.assertEqual(True, True)
            self.assertIn('form action="/passengers/edit/1" id="pass-details" method="POST"', test_resp)
            self.assertIn('value="Ben"', test_resp)
            self.assertIn('value="Stone"', test_resp)
            self.assertIn('value="12C"', test_resp)
            self.assertIn('value="NY, Some place"', test_resp)
            self.assertIn('value="1980-01-23"', test_resp)
            self.assertIn('''<option value="live"
                    
                        selected="selected"
                    
                >Live</option>''', test_resp)

        # update item
        responses.post(
            url='http://localhost//passapi/10',
            json={'message': 'Item(s) updated', 'item': {
                "id": 10,
                "fname": "Ben",
                "lname": "Stone",
                "seatno": "12C",
                "address": "NY, Some place",
                "dob": "1980-01-23",
                "status": "live",
                "comments": ""
            }},
            status=200)

        test_payload = {
                "fname": "Ben",
                "lname": "Stone",
                "seatno": "12C",
                "address": "NY, Some place",
                "dob": "1980-01-23",
                "status": "live",
                "comments": ""
            }

        with TestPassView.app.test_request_context(method='POST', data=test_payload):
            test_resp = edit('10')
            self.assertEqual(test_resp.status_code, 302)
            self.assertEqual(test_resp.mimetype, 'text/html')
            self.assertEqual(test_resp.headers['Location'], "/passengers/")

        #create item
        responses.post(
            url='http://localhost//passapi',
            json={'message': 'Item(s) updated', 'item': {
                "id": 50,
                "fname": "Ben",
                "lname": "Stone",
                "seatno": "12C",
                "address": "NY, Some place",
                "dob": "1980-01-23",
                "status": "live",
                "comments": ""
            }},
            status=200)

        with TestPassView.app.test_request_context(method='POST', data=test_payload):
            test_resp = edit('add')
            self.assertEqual(test_resp.status_code, 302)
            self.assertEqual(test_resp.mimetype, 'text/html')
            self.assertEqual(test_resp.headers['Location'], "/passengers/")


        #item not found / 404
        responses.post(
            url='http://localhost//passapi/20',
            json={'message': 'Item not found', 'item': {}},
            status=404)

        responses.get(
            url='http://localhost//passapi/20',
            json={'message': 'Item(s) updated', 'item': {
                "id": 20,
                "fname": "Ben",
                "lname": "Stone",
                "seatno": "12C",
                "address": "NY, Some place",
                "dob": "1980-01-23",
                "status": "live",
                "comments": ""
            }},
            status=200)

        test_notfound = {
                "fname": "Ben",
                "lname": "Stone",
                "seatno": "12C",
                "address": "NY, Some place",
                "dob": "1980-01-23",
                "status": "live",
                "comments": ""
            }

        with TestPassView.app.test_request_context(method='POST', data=test_notfound):
            test_resp = edit('20')
            self.assertIn('div id="div_flash" class="error"', test_resp)

    @responses.activate
    def test_delete_route(self):
        responses.get(
            url='http://localhost//eventsummaryapi',
            json={
                "1": 1,
                "2": 1},
            status=200
        )

        responses.delete(
            url='http://localhost//passapi/3',
            json={'message': 'Item deleted', 'item': {
                "id": 3,
                "fname": "Ben",
                "lname": "Stone",
                "seatno": "12C",
                "address": "NY, Some place",
                "dob": "1980-01-23",
                "status": "live",
                "comments": ""
                }},
            status=200
        )

        responses.delete(
            url='http://localhost//passapi/10000',
            json={'message': 'Item(s) not found', 'item': {}},
            status=404
        )

        with TestPassView.app.test_request_context():
            test_resp = delete('3')
            self.assertEqual(test_resp.status_code, 302)
            self.assertEqual(test_resp.mimetype, 'text/html')
            self.assertEqual(test_resp.headers['Location'], "/passengers/")

            test_resp = delete('10000')
            self.assertEqual(test_resp.status_code, 302)
            self.assertEqual(test_resp.mimetype, 'text/html')
            self.assertEqual(test_resp.headers['Location'], "/passengers/")

            test_resp = delete('1')
            self.assertEqual(test_resp.status_code, 302)
            self.assertEqual(test_resp.mimetype, 'text/html')
            self.assertEqual(test_resp.headers['Location'], "/passengers/")
