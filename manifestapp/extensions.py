"""Script to instantiate database and migrate functionality"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
app_bcrypt = Bcrypt()
login_manager = LoginManager()
