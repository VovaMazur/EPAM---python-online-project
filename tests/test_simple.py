"""Tests for Event API module"""
import unittest
from manifestapp import create_app


class TestSimpleTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    def test_get_all_events(self):
        self.assertEqual(200, 200)

        test_resp = self.client.get('/eventapi')
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)

