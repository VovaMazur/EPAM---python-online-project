"""Manifest application module"""
import os
from datetime import timedelta
from flask import Flask, render_template
from manifestapp.extensions import db, migrate, app_bcrypt, login_manager
from manifestapp.models import Event, Passenger, User
from manifestapp.rest import api
from manifestapp.views import events_bp, passengers_bp, loguser_bp


def create_app(test_config=None):
    """Flask application factory"""

    application = Flask(__name__)
    if test_config is None:
        application.config.from_pyfile('config.py')
    else:
        application.config.from_mapping(test_config)
    application.permanent_session_lifetime = timedelta(hours=1)

    # Initialize Flask extensions here
    db.init_app(application)

    if test_config is None:
        migration_dir = os.path.join('manifestapp', 'migrations')
        migrate.init_app(application, db, directory=migration_dir)
    api.init_app(application)

    app_bcrypt.init_app(application)
    login_manager.init_app(application)
    login_manager.login_view = 'log.login'
    login_manager.login_message = 'Please, login to access the web application'
    login_manager.login_message_category = "info"



    # Register blueprints here
    application.register_blueprint(events_bp)
    application.register_blueprint(passengers_bp)
    application.register_blueprint(loguser_bp)

    @application.route('/')
    def title_page():
        """Function for home route"""

        return render_template('main.html')

    return application
