"""Tests for Event view"""
import unittest
from manifestapp import create_app


class TestEventView(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()
        self.url = 'http://'+self.client.environ_base.get('REMOTE_ADDR')+':5000'

    def test_main_route_get(self):
        test_resp = self.client.get('http://127.0.0.1:5000/events/')  #f'{self.url}/events/'
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')

    # def test_main_route_post(self):
    #     test_form_data = 'filter=all'
    #     headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    #
    #     test_resp = self.client.post(f'{self.url}/events/', data=test_form_data, headers=headers)
    #     self.assertEqual(test_resp.status_code, 200)
    #     self.assertEqual(test_resp.mimetype, 'text/html')
    #
    #     test_form_data = 'filter=1'
    #     test_resp = self.client.post(f'{self.url}/events/', data=test_form_data, headers=headers)
    #     self.assertEqual(test_resp.status_code, 200)
    #     self.assertEqual(test_resp.mimetype, 'text/html')
    #
    #     test_form_data = 'filter=all&datefrom=2022-01-01'
    #     test_resp = self.client.post(f'{self.url}/events/', data=test_form_data, headers=headers)
    #     self.assertEqual(test_resp.status_code, 200)
    #     self.assertEqual(test_resp.mimetype, 'text/html')
    #
    #     test_form_data = 'filter=all&dateto=2023-01-31'
    #     test_resp = self.client.post(f'{self.url}/events/', data=test_form_data, headers=headers)
    #     self.assertEqual(test_resp.status_code, 200)
    #     self.assertEqual(test_resp.mimetype, 'text/html')
    #
    #     test_form_data = 'filter=all&datefrom=2022-01-01&dateto=2023-01-31'
    #     test_resp = self.client.post(f'{self.url}/events/', data=test_form_data, headers=headers)
    #     self.assertEqual(test_resp.status_code, 200)
    #     self.assertEqual(test_resp.mimetype, 'text/html')
    #
    #     test_form_data = 'filter=1&datefrom=2022-01-01&dateto=2023-01-31'
    #     test_resp = self.client.post(f'{self.url}/events/', data=test_form_data, headers=headers)
    #     self.assertEqual(test_resp.status_code, 200)
    #     self.assertEqual(test_resp.mimetype, 'text/html')


    # def test_main_function(self):
    #     with self.app.app_context():
    #         resp = main()
    #         print(resp)
    #         self.assertIsNotNone(resp)



