"""Tests for Event API module"""
import unittest
from manifestapp import create_app


class TestAppFactory(unittest.TestCase):
    def test_factory_function(self):
        app = create_app()
        self.assertEqual(app.name, 'manifestapp')
        self.assertEqual(app.testing, False)
        self.assertEqual(app.blueprints.keys(), dict({'events': '', 'passengers': '', 'log': ''}).keys())
        self.assertIn('mysql://app:password', app.config['SQLALCHEMY_DATABASE_URI'])
