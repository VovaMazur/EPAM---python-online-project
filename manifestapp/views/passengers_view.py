"""Passenger routes"""
import requests
from flask import Blueprint, request, flash, render_template, redirect, url_for, session
from flask_login import login_required
from manifestapp.logger import logger_setup

passengers_bp = Blueprint('passengers', __name__, static_folder='static', url_prefix='/passengers')

logger = logger_setup(__name__, '%(levelname)s::%(name)s::%(asctime)s'
                                '::%(message)s', 'webapp.log', 'DEBUG')


@passengers_bp.route('/', methods=['GET', 'POST'])
@login_required
def main():
    """main route"""

    status = session.get('pass_status', 'all')

    url = request.url_root

    events_summary = requests.get(f'{url}/eventsummaryapi', timeout=3).json()

    if request.method == 'POST':
        status = request.form.get('selected_status')
        session['pass_status'] = status
        session.modified = True
        logger.debug('Page filter is updated. %s', status)

    db_passes = requests.get(f'{url}/passapi/all/{status}', timeout=3)
    if db_passes.status_code == 200:
        db_passes = db_passes.json().get('item')
    else:
        db_passes = []

    data = []
    #processing raw data
    for passenger in db_passes:
        data.append(passenger)
        data[-1]['callings'] = events_summary.get(str(passenger['id']), 0)

    logger.debug('Page to be rendered. Parameters: %s', status)

    return render_template('passengers.html', cur_status=status, passengers=data)


@passengers_bp.route('/edit/<item>', methods=['GET', 'POST'])
@login_required
def edit(item):
    """edit route"""

    url = request.url_root

    item_data = {}

    if request.method == 'POST':
        updated_item = {}
        updated_item['fname'] = request.form.get('fname')
        updated_item['lname'] = request.form.get('lname')
        updated_item['seatno'] = request.form.get('seatno')
        updated_item['address'] = request.form.get('address')
        if request.form.get('dob'):
            updated_item['dob'] = request.form.get('dob')
        updated_item['status'] = request.form.get('status')
        updated_item['comments'] = request.form.get('comments')

        logger.debug('Updated data is received from the form. %s', updated_item)


        if item != 'add':
            #update
            resp = requests.post(f'{url}/passapi/{item}', json=updated_item, timeout=3)
        else:
            #create
            resp = requests.post(f'{url}/passapi', json=updated_item, timeout=3)


        if resp.status_code == 200:
            flash('Record is created/updated', 'success')
            logger.debug('Record is created / update. Response code: %s', resp.status_code)
            return redirect(url_for('passengers.main'))

        message = resp.json().get('message')
        flash(f'Some error during update. {message}', 'error')
        logger.error('Some error during update %s. Response code: %s', message, resp.status_code)
        item_data = updated_item

    if item != 'add':
        item_data = requests.get(f'{url}/passapi/{item}', timeout=3).json().get('item')

    return render_template('passform.html', data=item_data, item=item)


@passengers_bp.route('/delete/<item>')
@login_required
def delete(item):
    """edit route"""

    url = request.url_root

    events_summary = requests.get(f'{url}/eventsummaryapi', timeout=3).json()

    if str(item) not in events_summary:
        resp = requests.delete(f'{url}/passapi/{item}', timeout=3)

        if resp.status_code == 200:
            flash('Record is deleted', 'success')
            logger.debug('Record is deleted. Response code: %s', resp.status_code)
        else:
            message = resp.json().get('message')
            flash(f'Some error during deletion. {message}', 'error')
            logger.error('Some error during deletion %s. Response code: %s',
                         message, resp.status_code)
    else:
        flash('You cannot delete a passenger data if he logged callings', 'error')
        logger.error('You cannot delete a passenger data if there are logged callings')

    return redirect(url_for('passengers.main'))
