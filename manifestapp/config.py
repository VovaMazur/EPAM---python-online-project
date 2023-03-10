"""Manifest application config file"""
import os

SQLALCHEMY_DATABASE_URI = 'mysql://app:password@192.168.0.111:3306/manifestapp'
SECRET_KEY = os.urandom(12)
ENV = 'production'