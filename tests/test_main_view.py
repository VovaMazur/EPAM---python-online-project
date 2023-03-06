"""Tests for components"""
import unittest
from manifestapp import create_app


class TestMainView(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_main_route(self):
        test_resp = TestMainView.client.get('/')
        self.assertEqual(test_resp.status_code, 200)
        self.assertEqual(test_resp.mimetype, 'text/html')
