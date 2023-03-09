"""Tests for Event API module"""
import unittest
from manifestapp import create_app


class TestAppFactory(unittest.TestCase):
    def test_factory_function(self):
        app = create_app()
        self.assertEqual(app.name, 'manifestapp')
        self.assertEqual(app.testing, False)
        self.assertEqual(app.blueprints.keys(), dict({'events': '', 'passengers': '', 'log': ''}).keys())
        self.assertEqual(app.config['SQLALCHEMY_DATABASE_URI'], 'mysql://app:password@192.168.0.110:3306/manifestapp')
