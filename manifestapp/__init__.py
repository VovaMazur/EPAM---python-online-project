import os
from flask import Flask
from .db_instance import db, migrate
from manifestapp.models import Event, Passenger

def create_app():
    application = Flask(__name__)
    application.config.from_pyfile('config.py')

    # Initialize Flask extensions here
    db.init_app(application)
    MIGRATION_DIR = os.path.join('manifestapp', 'migrations')
    migrate.init_app(application, db, directory=MIGRATION_DIR)

    # Register blueprints here
    from manifestapp.views import events_bp, passengers_bp
    application.register_blueprint(events_bp, url_prefix='/events')
    application.register_blueprint(passengers_bp, url_prefix='/passengers')

    @application.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return application