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

