"""Events routes"""
import os
from dotenv import load_dotenv
from flask import Blueprint, request, flash
from flask import render_template, redirect, url_for
from manifestapp.logger import logger_setup
from manifestapp.service import event_get_bypass, pass_getall_list, \
    event_get_byid, event_post, event_delete

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

    #setup
    data = pass_getall_list()

    if request.method == 'POST':
        pass_id = request.form.get('filter') if request.form.get('filter') != 'all' else 'all'
        datefrom = request.form.get('datefrom') if request.form.get('datefrom') else '-'
        dateto = request.form.get('dateto') if request.form.get('dateto') else '-'
        logger.debug('Page filters are updated. %s %s %s', pass_id, datefrom, dateto)

    all_events = event_get_bypass(pass_id, datefrom, dateto)
    if all_events:
        all_events = all_events[0]['item']

    #processing raw data
    events = []
    for event in all_events:
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
    selected_pass = data[pass_id if pass_id == 'all' else int(pass_id)]
    selected_dates = [datefrom, dateto]

    logger.debug('Page to be rendered. Parameters: %s %s', selected_pass, selected_dates)

    return render_template('events.html', selected_pass=selected_pass,
                           dates=selected_dates, passengers=data, events=events)


@events_bp.route('/edit/<item>', methods=['GET', 'POST'])
def edit(item):
    """edit route"""

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
            resp = event_post(payload=updated_item, event_id=item)

        else:
            #create
            resp = event_post(payload=updated_item)

        if resp[1] == 200:
            flash('Record is created/updated', 'success')
            logger.debug('Record is created / update. Response code: %s', resp[1])
            return redirect(url_for('events.main'))

        message = resp[0].get('message')
        flash(f'Some error during update. {message}', 'error')
        logger.error('Some error during update %s. Response code: %s', message, resp[1])
        item_data = updated_item

    passes = pass_getall_list()
    if passes.get('all'):
        passes.pop('all')

    if item != 'add':
        item_data = event_get_byid(int(item))[0]['item']

    if 'other_pass' in item_data and item_data.get('other_pass') != '':
        item_data['other_pass'] = [int(x) for x in item_data.get('other_pass').split(',')]
    else:
        item_data['other_pass'] = []

    apiKey = os.getenv('API_KEY')

    return render_template('eventform.html', item=item, data=item_data, passengers=passes, key=apiKey)


@events_bp.route('/delete/<item>')
def delete(item):
    """edit route"""

    resp = event_delete(item)
    if resp[1] == 200:
        flash('Record is deleted', 'success')
        logger.debug('Record is deleted. Response code: %s', resp[1])
    else:
        message = resp[0].get('message')
        flash(f'Some error during deletion. {message}', 'error')
        logger.error('Some error during deletion %s. Response code: %s', message, resp[1])

    return redirect(url_for('events.main'))
