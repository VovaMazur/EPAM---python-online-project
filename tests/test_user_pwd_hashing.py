"""Tests for Event API module"""
import unittest
from manifestapp.models import User


class TestUserAPI(unittest.TestCase):
    def test_user_pwd_hashing(self):
        m = User(username='test', password='admin1234')
        self.assertNotEqual(m.pwd_hash, 'admin1234')
        self.assertEqual(m.pwd_hash, m.password)
        self.assertGreater(len(m.pwd_hash), 30)

