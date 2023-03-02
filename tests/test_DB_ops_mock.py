"""Tests for Event API module"""
import unittest
from manifestapp import create_app, db
from .test_data import test_events, test_pass


class TestNewEnv(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        test_config = {
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db',
            'SECRET_KEY': 'test'
        }

        cls.app = create_app(test_config)
        with cls.app.app_context():
            db.create_all()

            for obj in test_pass:
                db.session.add(obj)
                db.session.commit()

            for obj in test_events:
                db.session.add(obj)
                db.session.commit()

        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.drop_all()

    def test_get_all(self):
        test_resp = TestNewEnv.client.get('/eventapi')
        self.assertEqual(test_resp.status_code, 200)
        self.assertTrue(test_resp.is_json)






