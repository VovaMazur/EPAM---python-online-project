"""Passenger routes"""
from flask import Blueprint, request, flash
from flask import render_template, redirect, url_for
from manifestapp.logger import logger_setup
from manifestapp.service import pass_get_bystatus, pass_get_byid, pass_post, pass_delete, event_get_summary

passengers_bp = Blueprint('passengers', __name__, static_folder='static', url_prefix='/passengers')

logger = logger_setup(__name__, '%(levelname)s::%(name)s::%(asctime)s'
                                '::%(message)s', 'webapp.log', 'DEBUG')

#initial setup
events_summary = {}
status = 'all'


@passengers_bp.route('/', methods=['GET', 'POST'])
def main():
    """main route"""

    global events_summary, status

    events_summary = event_get_summary()

    if request.method == 'POST':
        status = request.form.get('selected_status')
        logger.debug('Page filter is updated. %s', status)

    db_passes = pass_get_bystatus(status=status)[0]['item']

    data = []
    #processing raw data
    for passenger in db_passes:
        data.append(passenger)
        data[-1]['callings'] = events_summary[passenger['id']] \
            if passenger['id'] in events_summary else 0

    logger.debug('Page to be rendered. Parameters: %s', status)

    return render_template('passengers.html', cur_status=status, passengers=data)


@passengers_bp.route('/edit/<item>', methods=['GET', 'POST'])
def edit(item):
    """edit route"""

    item_data = {}
    if item != 'add':
        item_data = pass_get_byid(item)[0]['item']

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
            resp = pass_post(payload=updated_item, pass_id=item)
        else:
            #create
            resp = pass_post(payload=updated_item)


        if resp[1] == 200:
            flash('Record is created/updated', 'success')
            logger.debug('Record is created / update. Response code: %s', resp[1])
            return redirect(url_for('passengers.main'))

        message = resp[0].get('message')
        flash(f'Some error during update. {message}', 'error')
        logger.error('Some error during update %s. Response code: %s', message, resp[1])

    return render_template('passform.html', data=item_data, item=item)


@passengers_bp.route('/delete/<item>')
def delete(item):
    """edit route"""

    if int(item) not in events_summary:
        resp = pass_delete(item)
        if resp[1] == 200:
            flash('Record is deleted', 'success')
            logger.debug('Record is deleted. Response code: %s', resp[1])
        else:
            message = resp[0].get('message')
            flash(f'Some error during deletion. {message}', 'error')
            logger.error('Some error during deletion %s. Response code: %s', message, resp[1])
    else:
        flash('You cannot delete a passenger data if he logged callings', 'error')
        logger.error('You cannot delete a passenger data if there are logged callings')

    return redirect(url_for('passengers.main'))
