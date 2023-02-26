"""Manifest application module"""
import os
from flask import Flask, render_template
from manifestapp.db_instance import db, migrate
from manifestapp.models import Event, Passenger
from manifestapp.rest import api
from manifestapp.views import events_bp, passengers_bp


def create_app():
    """Flask application factory"""

    application = Flask(__name__)
    application.config.from_pyfile('config.py')

    with application.app_context():
        # Initialize Flask extensions here
        db.init_app(application)

        migration_dir = os.path.join('manifestapp', 'migrations')
        migrate.init_app(application, db, directory=migration_dir)

        api.init_app(application)

        # Register blueprints here
        application.register_blueprint(events_bp, url_prefix='/events')
        application.register_blueprint(passengers_bp, url_prefix='/passengers')

    application.app_context().push()

    @application.route('/')
    def title_page():
        """Function for home route"""

        return render_template('main.html')

    return application
