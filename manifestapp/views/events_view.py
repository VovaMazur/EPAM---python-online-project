"""Events routes"""
import json
import requests
from flask import Blueprint, request, flash
from flask import render_template, redirect, url_for
from manifestapp.logger import logger_setup

events_bp = Blueprint('events', __name__, static_folder='static')

logger = logger_setup(__name__, '%(levelname)s::%(name)s::%(asctime)s'
                                '::%(message)s', 'webapp.log', 'DEBUG')


#initial setup
URL = ''
passengers = {}
pass_id, datefrom, dateto = 'all', '-', '-'

def get_list_pass():
    """function to prepare list of passengers"""
    global URL, passengers

    if URL == '':
        URL = request.url_root

    db_passengers = requests.get(URL+'passapi', timeout=3).json()
    passengers = {'all': 'All'}
    for i in db_passengers:
        passengers[int(i['id'])] = i['fname'] + ' ' + i['lname']


@events_bp.route('/', methods=['GET', 'POST'])
def main():
    """main route"""
    global URL, passengers, pass_id, datefrom, dateto

    #setup
    get_list_pass()
    data = passengers.copy()

    if request.method == 'POST':
        pass_id = int(request.form.get('filter')) if request.form.get('filter') != 'all' else 'all'
        datefrom = request.form.get('datefrom') if request.form.get('datefrom') else '-'
        dateto = request.form.get('dateto') if request.form.get('dateto') else '-'
        logger.debug('Page filters are updated')

    db_events = requests.get(f'{URL}eventapi/all/{pass_id}/{datefrom}/{dateto}', timeout=3).json()
    #processing raw data
    events = []
    for event in db_events:
        if isinstance(event, dict):
            events.append({
                'id': event.get('id'),
                'date': event.get('date'),
                'passenger': data.get(event.get('passengerID')),
                'geo_location': event.get('geo_location'),
                'description': event.get('description'),
                'status': event.get('status'),
                'other_pass': ', '.join([data.get(int(x)) for x in
                                         event.get('other_pass').split(',') if x != ''])
            })
    selected_pass = data[pass_id]
    selected_dates = [datefrom, dateto]

    logger.debug('Page to be rendered. Parameters: %s %s', selected_pass, selected_dates)

    return render_template('events.html', selected_pass=selected_pass,
                           dates=selected_dates, passengers=data, events=events)


@events_bp.route('/edit/<item>', methods=['GET', 'POST'])
def edit(item):
    """edit route"""

    global URL, passengers

    #setup
    if URL == '':
        URL = request.url_root
    if not passengers:
        get_list_pass()

    passes = passengers.copy()
    if passes.get('all'):
        passes.pop('all')

    item_data = {}
    if item != 'add':
        item_data = requests.get(f'{URL}eventapi/{item}', timeout=3).json()[0]
        item_data['other_pass'] = [int(x) for x in item_data.get('other_pass').split(',')] \
            if item_data.get('other_pass') != '' else []

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

        headers = {'Content-Type': 'application/json'}

        if item != 'add':
            resp = requests.post(f'{URL}eventapi/{item}',
                                 data=json.dumps(updated_item), headers=headers, timeout=3)
        else:
            resp = requests.post(f'{URL}eventapi', data=json.dumps(updated_item),
                                 headers=headers, timeout=3)

        if resp.status_code == 200:
            flash('Record is created/updated', 'success')
            logger.debug('Record is created / update. Response code: %s', resp.status_code)
            return redirect(url_for('events.main'))

        message = resp.json().get('message')
        flash(f'Some error during update. {message}', 'error')
        logger.error('Some error during update %s. Response code: %s', message, resp.status_code)

    return render_template('eventform.html', item=item, data=item_data, passengers=passes)


@events_bp.route('/delete/<item>')
def delete(item):
    """edit route"""

    global URL
    #setup
    if URL == '':
        URL = request.url_root

    resp = requests.delete(f'{URL}eventapi/{item}', timeout=3)
    if resp.status_code == 200:
        flash('Record is deleted', 'success')
        logger.debug('Record is deleted. Response code: %s', resp.status_code)
    else:
        message = resp.json().get('message')
        flash(f'Some error during deletion. {message}', 'error')
        logger.error('Some error during deletion %s. Response code: %s', message, resp.status_code)

    return redirect(url_for('events.main'))
