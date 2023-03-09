"""Tests for components"""
import unittest
from unittest.mock import patch, MagicMock
from flask_login import current_user, FlaskLoginClient
from manifestapp import create_app
from manifestapp.views.loguser_view import login, register


class TestLogView(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.test_client_class = FlaskLoginClient

    def test_login(self):
        with TestLogView.app.test_request_context():
            test_resp = login()
            self.assertIn('Login form:', test_resp)
            self.assertIn('form action="/log/in" id="login" method="POST"', test_resp)

        test_form_data = {
            'username': 'test',
            'password': '123456',
        }
        with TestLogView.app.test_request_context(method='POST', data=test_form_data):
            test_resp = login()
            self.assertEqual(current_user.is_authenticated, 1)
            self.assertEqual(test_resp.status_code, 302)
            self.assertEqual(test_resp.mimetype, 'text/html')
            self.assertEqual(test_resp.headers['Location'], "/events/")

        test_invalid_form_data = {
            'username': 'test',
            'password': 'test',
        }
        with TestLogView.app.test_request_context(method='POST', data=test_invalid_form_data):
            test_resp = login()
            self.assertEqual(current_user.is_authenticated, False)
            self.assertIn('Login form:', test_resp)
            self.assertIn('form action="/log/in" id="login" method="POST"', test_resp)
            self.assertIn('div id="div_flash" class="info"', test_resp)

    def test_register_invalid(self):
        with TestLogView.app.test_request_context():
            test_resp = register()
            self.assertEqual(current_user.is_authenticated, False)
            self.assertIn('Registration form:', test_resp)
            self.assertIn('form action="/log/register" id="register" method="POST"', test_resp)

        #passwords do not match
        test_inv_form_data = {
            'username': 'test2',
            'password': '123456',
            'password2': '1234566'
        }
        with TestLogView.app.test_request_context(method='POST', data=test_inv_form_data):
            test_resp = register()
            self.assertEqual(current_user.is_authenticated, False)
            self.assertIn('div id="div_flash" class="info"', test_resp)
            self.assertIn('Registration form:', test_resp)
            self.assertIn('form action="/log/register" id="register" method="POST"', test_resp)

        #password do not comply with policy
        test_inv_form_data = {
            'username': 'test2',
            'password': '123456',
            'password2': '123456'
        }
        with TestLogView.app.test_request_context(method='POST', data=test_inv_form_data):
            test_resp = register()
            self.assertEqual(current_user.is_authenticated, False)
            self.assertIn('div id="div_flash" class="info"', test_resp)
            self.assertIn('Password is not strong enough', test_resp)
            self.assertIn('Registration form:', test_resp)
            self.assertIn('form action="/log/register" id="register" method="POST"', test_resp)

    @patch('manifestapp.views.loguser_view.User')
    def test_register_existing(self, mock_user):
        mock_user.query.filter().first.return_value = MagicMock(username='test2')

        test_form_data = {
            'username': 'test2',
            'password': '123456qwE',
            'password2': '123456qwE'
        }
        with TestLogView.app.test_request_context(method='POST', data=test_form_data):
            test_resp = register()
            self.assertEqual(current_user.is_authenticated, False)
            self.assertIn('div id="div_flash" class="info"', test_resp)
            self.assertIn('User &lt;test2&gt; already exists. Please, use another username or go to login page', test_resp)
            self.assertIn('Registration form:', test_resp)
            self.assertIn('form action="/log/register" id="register" method="POST"', test_resp)

    @patch('manifestapp.views.loguser_view.db')
    @patch('manifestapp.views.loguser_view.User')
    def test_register_new(self, mock_user, mock_db):
        mock_user.query.filter().first.return_value = None
        mock_db.session.add.return_value = None
        mock_db.session.commit.return_value = None

        test_form_data = {
            'username': 'test2',
            'password': '123456qwE',
            'password2': '123456qwE'
        }
        with TestLogView.app.test_request_context(method='POST', data=test_form_data):
            test_resp = register()
            self.assertEqual(test_resp.status_code, 302)
            self.assertEqual(test_resp.mimetype, 'text/html')
            self.assertEqual(test_resp.headers['Location'], "/events/")

    def test_logout(self):
        user = MagicMock(username='test')
        user.get_id.return_value = 1

        with TestLogView.app.test_client(user=user) as client:
            test_resp = client.get('/log/out')
            self.assertEqual(current_user.is_authenticated, False)
            self.assertEqual(test_resp.status_code, 302)
            self.assertEqual(test_resp.mimetype, 'text/html')
            self.assertIn("/log/in", test_resp.headers['Location'])