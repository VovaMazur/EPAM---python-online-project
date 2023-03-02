"""Manifest application module"""
import os
from flask import Flask, render_template
from manifestapp.db_instance import db, migrate
from manifestapp.models import Event, Passenger
from manifestapp.rest import api
from manifestapp.views import events_bp, passengers_bp


def create_app(test_config=None):
    """Flask application factory"""

    application = Flask(__name__)
    if test_config is None:
        application.config.from_pyfile('config.py')
    else:
        application.config.from_mapping(test_config)

    # Initialize Flask extensions here
    db.init_app(application)

    if test_config is None:
        migration_dir = os.path.join('manifestapp', 'migrations')
        migrate.init_app(application, db, directory=migration_dir)

    api.init_app(application)

    # Register blueprints here
    application.register_blueprint(events_bp)
    application.register_blueprint(passengers_bp)

    @application.route('/')
    def title_page():
        """Function for home route"""

        return render_template('main.html')

    return application
