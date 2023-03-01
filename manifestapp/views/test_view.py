"""Events routes"""
from flask import Blueprint

test_bp = Blueprint('tests', __name__, static_folder='static', url_prefix='/anothertest')

@test_bp.route('/')
def main():
    return '<p>Hello, it`s !!! another !!! good testing here!</p>'