"""Passenger routes"""
import json
import requests
from flask import Blueprint, request, flash
from flask import render_template, redirect, url_for
from manifestapp.logger import logger_setup

passengers_bp = Blueprint('passengers', __name__, static_folder='static')

logger = logger_setup(__name__, '%(levelname)s::%(name)s::%(asctime)s'
                                '::%(message)s', 'webapp.log', 'DEBUG')

#initial setup
URL = ''
events_summary = {}
status = 'all'


def get_events_summary():
    """function to prepare list of passengers"""
    global URL, events

    if URL == '':
        URL = request.url_root

    db_events = requests.get(URL+'eventapi', timeout=3).json()
    for i in db_events:
        id_item = i.get('passengerID')
        if id_item in events_summary:
            events_summary[id_item] += 1
        else:
            events_summary[id_item] = 1


@passengers_bp.route('/', methods=['GET', 'POST'])
def main():
    """main route"""

    global URL, events_summary, status

    #setup
    if URL == '':
        URL = request.url_root
    events_summary = {}
    get_events_summary()
    if not status:
        status = 'all'

    if request.method == 'POST':
        status = request.form.get('selected_status')
        logger.debug('Page filter is updated')

    if status == 'all':
        db_passes = requests.get(f'{URL}passapi', timeout=3).json()
    else:
        db_passes = requests.get(f'{URL}passapi/all/{status}', timeout=3).json()

    data = []
    #processing raw data
    for passenger in db_passes:
        if isinstance(passenger, dict):
            data.append(passenger)
            data[-1]['callings'] = events_summary[passenger['id']] \
                if passenger['id'] in events_summary else 0

    logger.debug('Page to be rendered. Parameters: %s', status)

    return render_template('passengers.html', cur_status=status, passengers=data)


@passengers_bp.route('/edit/<item>', methods=['GET', 'POST'])
def edit(item):
    """edit route"""

    global URL

    #setup
    if URL == '':
        URL = request.url_root

    item_data = {}
    if item != 'add':
        item_data = requests.get(f'{URL}passapi/{item}', timeout=3).json()[0]

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

        headers = {'Content-Type': 'application/json'}

        if item != 'add':
            resp = requests.post(f'{URL}passapi/{item}',
                                 data=json.dumps(updated_item), headers=headers, timeout=3)
        else:
            resp = requests.post(f'{URL}passapi', data=json.dumps(updated_item),
                                 headers=headers, timeout=3)

        if resp.status_code == 200:
            flash('Record is created/updated', 'success')
            logger.debug('Record is created / update. Response code: %s', resp.status_code)
            return redirect(url_for('passengers.main'))

        message = resp.json().get('message')
        flash(f'Some error during update. {message}', 'error')
        logger.error('Some error during update %s. Response code: %s', message, resp.status_code)

    return render_template('passform.html', data=item_data, item=item)


@passengers_bp.route('/delete/<item>')
def delete(item):
    """edit route"""

    global URL
    #setup
    if URL == '':
        URL = request.url_root

    if int(item) not in events_summary:
        resp = requests.delete(f'{URL}passapi/{item}', timeout=3)
        if resp.status_code == 200:
            flash('Record is deleted', 'success')
            logger.debug('Record is deleted. Response code: %s', resp.status_code)
        else:
            message = resp.json().get('message')
            flash(f'Some error during deletion. {message}', 'error')
            logger.error('Some error during deletion %s. Response code: %s', message, resp.status_code)
    else:
        flash('You cannot delete a passenger data if he logged callings', 'error')
        logger.error('You cannot delete a passenger data if he logged callings')

    return redirect(url_for('passengers.main'))
