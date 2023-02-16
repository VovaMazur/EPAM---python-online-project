from flask import Blueprint
from flask import render_template

events_bp = Blueprint('events', __name__)

@events_bp.route('/')
def index():
    return render_template('events.html')

@events_bp.route('/edit')
def event_edit():
    return render_template('eventform.html')