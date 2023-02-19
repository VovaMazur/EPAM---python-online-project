"""Events routes"""
from flask import Blueprint
from flask import render_template

events_bp = Blueprint('events', __name__)

@events_bp.route('/')
def index():
    """main route"""
    return render_template('events.html')

@events_bp.route('/edit')
def event_edit():
    """edit route"""
    return render_template('eventform.html')
