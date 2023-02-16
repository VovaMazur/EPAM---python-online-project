# app config
import os

SQLALCHEMY_DATABASE_URI = 'mysql://app:password@localhost:3306/manifestapp'
SECRET_KEY = os.environ.get('SECRET_KEY')
