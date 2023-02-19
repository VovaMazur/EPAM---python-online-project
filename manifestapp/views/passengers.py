"""Passenger routes"""
from flask import Blueprint
from flask import render_template

passengers_bp = Blueprint('passengers', __name__)

@passengers_bp.route('/')
def index():
    """main route"""
    return render_template('passengers.html')

@passengers_bp.route('/edit')
def pass_edit():
    """edit route"""
    return render_template('passform.html')
