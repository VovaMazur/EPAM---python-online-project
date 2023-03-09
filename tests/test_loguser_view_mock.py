"""Tests for components"""
import unittest
from flask_login import current_user
from manifestapp import create_app
from manifestapp.extensions import db
from .data_users import t_users


class TestLogView(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Test setup')
        t_config = {
            'ENV': 'development',
            'DEBUG': True,
            'TESTING': True,
            'LOGIN_DISABLED': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db',
            'SECRET_KEY': 'test'
        }
        cls.app = create_app(t_config)

        with cls.app.app_context():
            db.drop_all()
            db.create_all()

            db.session.add_all(t_users)
            db.session.commit()

        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        print('Test teardown')
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login(self):
        with TestLogView.client as client:
            test_resp = client.get('/log/in').text
            self.assertIn('Login form:', test_resp)
            self.assertIn('form action="/log/in" id="login" method="POST"', test_resp)

        test_form_data = {
            'username': 'test1',
            'password': '123456',
        }
        with TestLogView.client as client:
            test_resp = client.post('/log/in', data=test_form_data)
            self.assertEqual(current_user.is_authenticated, 1)
            self.assertEqual(test_resp.status_code, 302)
            self.assertEqual(test_resp.mimetype, 'text/html')
            self.assertEqual(test_resp.headers['Location'], "/events/")

        test_invalid_form_data = {
            'username': 'test',
            'password': 'test',
        }
        with TestLogView.client as client:
            test_resp = client.post('/log/in', data=test_invalid_form_data).text
            self.assertIn('Login form:', test_resp)
            self.assertIn('form action="/log/in" id="login" method="POST"', test_resp)
            self.assertIn('div id="div_flash" class="info"', test_resp)

    def test_register_invalid(self):
        with TestLogView.client as client:
            test_resp = client.get('/log/register').text
            self.assertEqual(current_user.is_authenticated, False)
            self.assertIn('Registration form:', test_resp)
            self.assertIn('form action="/log/register" id="register" method="POST"', test_resp)

        #passwords do not match
        test_inv_form_data = {
            'username': 'test3',
            'password': '123456',
            'password2': '1234566'
        }
        with TestLogView.client as client:
            test_resp = client.post('/log/register', data=test_inv_form_data).text
            self.assertEqual(current_user.is_authenticated, False)
            self.assertIn('div id="div_flash" class="info"', test_resp)
            self.assertIn('Registration form:', test_resp)
            self.assertIn('form action="/log/register" id="register" method="POST"', test_resp)

        #password do not comply with policy
        test_inv_form_data = {
            'username': 'test3',
            'password': '123456',
            'password2': '123456'
        }
        with TestLogView.client as client:
            test_resp = client.post('/log/register', data=test_inv_form_data).text
            self.assertEqual(current_user.is_authenticated, False)
            self.assertIn('div id="div_flash" class="info"', test_resp)
            self.assertIn('Password is not strong enough', test_resp)
            self.assertIn('Registration form:', test_resp)
            self.assertIn('form action="/log/register" id="register" method="POST"', test_resp)

    def test_register_existing(self):
        test_form_data = {
            'username': 'test2',
            'password': '123456qwE',
            'password2': '123456qwE'
        }
        with TestLogView.client as client:
            test_resp = client.post('/log/register', data=test_form_data).text
            self.assertEqual(current_user.is_authenticated, False)
            self.assertIn('div id="div_flash" class="info"', test_resp)
            self.assertIn('User &lt;test2&gt; already exists. Please, use another username or go to login page', test_resp)
            self.assertIn('Registration form:', test_resp)
            self.assertIn('form action="/log/register" id="register" method="POST"', test_resp)

    def test_register_new(self):
        test_form_data = {
            'username': 'test3',
            'password': '123456qwE',
            'password2': '123456qwE'
        }
        with TestLogView.client as client:
            test_resp = client.post('/log/register', data=test_form_data)
            self.assertEqual(test_resp.status_code, 302)
            self.assertEqual(test_resp.mimetype, 'text/html')
            self.assertEqual(test_resp.headers['Location'], "/events/")

    def test_logout(self):
        with TestLogView.client as client:
            test_resp = client.get('/log/out')
            self.assertEqual(current_user.is_authenticated, False)
            self.assertEqual(test_resp.status_code, 302)
            self.assertEqual(test_resp.mimetype, 'text/html')
            self.assertIn("/log/in", test_resp.headers['Location'])