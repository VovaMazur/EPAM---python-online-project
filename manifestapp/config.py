"""Manifest application config file"""
import os

SQLALCHEMY_DATABASE_URI = 'mysql://app:password@localhost:3306/manifestapp'
SECRET_KEY = os.urandom(12)
