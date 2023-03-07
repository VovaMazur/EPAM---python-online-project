"""Events routes"""
import os
import requests
from dotenv import load_dotenv
from flask import Blueprint, request, flash
from flask import render_template, redirect, url_for
from manifestapp.logger import logger_setup

events_bp = Blueprint('events', __name__, static_folder='static', url_prefix='/events')

logger = logger_setup(__name__, '%(levelname)s::%(name)s::%(asctime)s'
                                '::%(message)s', 'webapp.log', 'DEBUG')

#initial setup
pass_id, datefrom, dateto = 'all', '-', '-'
load_dotenv()

@events_bp.route('/', methods=['GET', 'POST'])
def main():
    """main route"""
    global pass_id, datefrom, dateto

    url = request.url_root

    #setup
    data = requests.get(f'{url}/passlistapi', timeout=3).json()

    if request.method == 'POST':
        pass_id = request.form.get('filter') if request.form.get('filter') != 'all' else 'all'
        datefrom = request.form.get('datefrom') if request.form.get('datefrom') else '-'
        dateto = request.form.get('dateto') if request.form.get('dateto') else '-'
        logger.debug('Page filters are updated. %s %s %s', pass_id, datefrom, dateto)

    all_events = requests.get(f'{url}/eventapi/all/{pass_id}/{datefrom}/{dateto}', timeout=3)
    if all_events:
        all_events = all_events.json().get('item')
    else:
        all_events = []

    #processing raw data
    events = []
    for event in all_events:
        events.append({
            'id': event.get('id'),
            'date': event.get('date'),
            'passenger': data.get(str(event.get('passengerID'))),
            'geo_location': event.get('geo_location'),
            'description': event.get('description'),
            'status': event.get('status'),
            'other_pass': ', '.join([data.get(x.strip()) if data.get(x.strip()) is not None
                                        else 'Deleted' for x in event.get('other_pass').split(',')])
                                        if event.get('other_pass').split(',') != [''] else ''
        })
    selected_pass = data[pass_id if pass_id == 'all' else pass_id]
    selected_dates = [datefrom, dateto]

    logger.debug('Page to be rendered. Parameters: %s %s', selected_pass, selected_dates)

    return render_template('events.html', selected_pass=selected_pass,
                           dates=selected_dates, passengers=data, events=events)


@events_bp.route('/edit/<item>', methods=['GET', 'POST'])
def edit(item):
    """edit route"""

    url = request.url_root

    item_data = {}

    if request.method == 'POST':
        updated_item = {}
        updated_item['date'] = request.form.get('date')
        updated_item['passengerID'] = int(request.form.get('passengerID'))
        updated_item['geo_location'] = request.form.get('geo_location')
        updated_item['description'] = request.form.get('description')
        updated_item['status'] = request.form.get('status')
        updated_item['other_pass'] = ','.join(request.form.getlist('other_pass'))
        updated_item['comments'] = request.form.get('comments')

        logger.debug('Updated data is received from the form. %s', updated_item)

        if item != 'add':
            #update
            resp = requests.post(f'{url}/eventapi/{item}', json=updated_item, timeout=3)

        else:
            #create
            resp = requests.post(f'{url}/eventapi', json=updated_item, timeout=3)

        if resp.status_code == 200:
            flash('Record is created/updated', 'success')
            logger.debug('Record is created / update. Response code: %s', resp.status_code)
            return redirect(url_for('events.main'))

        message = resp.json().get('message')
        flash(f'Some error during update. {message}', 'error')
        logger.error('Some error during update %s. Response code: %s', message, resp.status_code)
        item_data = updated_item

    passes = requests.get(f'{url}/passlistapi', timeout=3).json()
    if passes.get('all'):
        passes.pop('all')

    if item != 'add':
        item_data = requests.get(f'{url}/eventapi/{item}', timeout=3).json().get('item')

    if 'other_pass' in item_data and item_data.get('other_pass') != '':
        item_data['other_pass'] = [int(x) for x in item_data.get('other_pass').split(',')]
    else:
        item_data['other_pass'] = []

    api_key = os.getenv('API_KEY')

    return render_template('eventform.html', item=item, data=item_data,
                           passengers=passes, key=api_key)


@events_bp.route('/delete/<item>')
def delete(item):
    """edit route"""

    url = request.url_root

    resp = requests.delete(f'{url}/eventapi/{item}', timeout=3)

    if resp.status_code == 200:
        flash('Record is deleted', 'success')
        logger.debug('Record is deleted. Response code: %s', resp.status_code)
    else:
        message = resp.json().get('message')
        flash(f'Some error during deletion. {message}', 'error')
        logger.error('Some error during deletion %s. Response code: %s', message, resp.status_code)

    return redirect(url_for('events.main'))
