"""Data for testing"""
from manifestapp.models import User

t_u1 = User(
    username='test1',
    password='123456')

t_u2 = User(
    username='test2',
    password='password')

t_users = [t_u1, t_u2]
