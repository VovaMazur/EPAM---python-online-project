"""CRUD Functions with app models"""
from jsonschema import validate, exceptions
from manifestapp.db_instance import db
from manifestapp.models import Event, Passenger

error_msgs = [
    [{'message': 'ID parameter should be an integer'}, 400],
    [{'message': 'Item(s) not found'}, 404],
    [{'message': 'Date parameter should be a valid date, format YYYY-MM-DD'}, 400],
    [{'message': 'Incorrect payload'}, 400],
    [{'message': 'Unknown error during record creation'}, 400],
    [{'message': 'Item created'}, 200],
    [{'message': 'Item updated'}, 200],
    [{'message': 'Item deleted'}, 200],
    [{'message': 'Item(s) retrieved'}, 200]
]

create_schema_event = {
    'type': 'object',
    'properties': {
        'date': {'type': 'string',
                 'format': 'date'},
        'passengerID': {'type': 'integer'},
        'geo_location': {'type': 'string',
                         'pattern': '^[-]?[0-9]+[.][0-9]+[,][ ]?[-]?[0-9]+[.][0-9]+$'},
        'description': {'type': 'string',
                        'maxLength': 90},
        'status': {'type': 'string',
                   'pattern': 'unknown|success|failure'},
        'other_pass': {'type': 'string'},
        'comments': {'type': 'string',
                     'maxLength': 140}
    },
    'additionalProperties': False,
    'required': ['date', 'passengerID', 'geo_location', 'description', 'status']
}

update_schema_event = {}
update_schema_event = create_schema_event.copy()
update_schema_event.pop('required')


create_schema_pass = {
    'type': 'object',
    'properties': {
        'fname': {'type': 'string',
                 'maxLength': 45},
        'lname': {'type': 'string',
                  'maxLength': 45},
        'seatno': {'type': 'string',
                 'pattern': '^[0-9]{2}[A-Z]$'},
        'address': {'type': 'string',
                  'maxLength': 100},
        'dob': {'type': 'string',
                 'format': 'date'},
        'status': {'type': 'string',
                   'pattern': 'unknown|live|dead'},
        'comments': {'type': 'string',
                     'maxLength': 140}
    },
    'additionalProperties': False,
    'required': ['fname', 'lname', 'seatno', 'status']
}

update_schema_pass = {}
update_schema_pass = create_schema_pass.copy()
update_schema_pass.pop('required')


def event_get_bypass(passid=None, datefrom=None, dateto=None):
    """Read function with Event model by other parameters"""

    passid = None if (passid is None or not passid.isdigit()) else int(passid)
    datefrom = None if datefrom == '-' else datefrom
    dateto = None if dateto == '-' else dateto

    if passid:
        if datefrom and dateto:
            items = Event.query.filter(Event.date >= datefrom,
                                       Event.date <= dateto,
                                       Event.passengerID == passid).all()
        elif datefrom:
            items = Event.query.filter(Event.date >= datefrom,
                                       Event.passengerID == passid).all()

        elif dateto:
            items = Event.query.filter(Event.date <= dateto,
                                       Event.passengerID == passid).all()

        else:
            items = Event.query.filter(Event.passengerID == passid).all()


    else:
        if datefrom and dateto:
            items = Event.query.filter(Event.date >= datefrom,
                                       Event.date <= dateto).all()
        elif datefrom:
            items = Event.query.filter(Event.date >= datefrom).all()

        elif dateto:
            items = Event.query.filter(Event.date <= dateto).all()

        else:
            items = Event.query.all()

    if items:
        resp = error_msgs[8]
        temp = []
        for i in items:
            temp.append(i.fs_as_dict)
        resp[0]['item'] = temp
    else:
        resp = error_msgs[1]

    return resp


def event_get_byid(event_id):
    """Read function with Event model by event ID"""

    item = Event.query.get(event_id)
    if item:
        resp = error_msgs[8]
        resp[0]['item'] = item.fs_as_dict
    else:
        resp = error_msgs[1]

    return resp


def event_post(payload, event_id=None):
    """POST function with Event model and payload validation"""

    try:
        if not event_id:
            validate(payload, schema=create_schema_event)
        else:
            validate(payload, schema=update_schema_event)

    except exceptions.ValidationError as error:
        resp = error_msgs[3]
        resp[0]['message'] = f'{resp[0]["message"]} {error}'

    else:
        if not event_id:
            try:
                #create new item
                item = Event()
                for k in payload:
                    setattr(item, k, payload[k])
                db.session.add(item)
                db.session.commit()
                resp = error_msgs[5]
                resp[0]['item'] = item.fs_as_dict

            except Exception:
                resp = error_msgs[4]

        else:
            #update existing item
            old_item = Event.query.filter(Event.id == event_id).first()
            if old_item:
                for k, v in payload.items():
                    setattr(old_item, k, v)
                db.session.commit()
                resp = error_msgs[6]
                resp[0]['item'] = old_item.fs_as_dict
            else:
                resp = error_msgs[1]

    return resp


def event_delete(event_id):
    """DELETE function with Event model"""

    item = Event.query.filter(Event.id == event_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        resp = error_msgs[7]
        resp[0]['item'] = item.fs_as_dict
    else:
        resp = error_msgs[1]

    return resp


def event_get_summary():
    """function to summary number of logged events per passenger"""

    events_summary = {}

    db_events = event_get_bypass()[0]['item']

    for i in db_events:
        id_item = i.get('passengerID')
        if id_item in events_summary:
            events_summary[id_item] += 1
        else:
            events_summary[id_item] = 1

    return events_summary


def pass_get_bystatus(status=None):
    """Read function with Passenger model all / by statuses"""

    status = None if status in ('all', None) else status

    if status:
        items = Passenger.query.filter(Passenger.status == status).all()
    else:
        items = Passenger.query.all()

    if items:
        resp = error_msgs[8]
        temp = []
        for i in items:
            temp.append(i.fs_as_dict)
        resp[0]['item'] = temp
    else:
        resp = error_msgs[1]

    return resp


def pass_get_byid(passid):
    """Read function with Passenger model by passenger ID"""

    item = Passenger.query.get(passid)
    if item:
        resp = error_msgs[8]
        resp[0]['item'] = item.fs_as_dict
    else:
        resp = error_msgs[1]

    return resp


def pass_getall_list():
    """function to prepare list of passengers for view html page"""

    db_items = Passenger.query.all()
    items = [x.fs_as_dict for x in db_items]
    passengers = {'all': 'All'}
    for i in items:
        passengers[i['id']] = i['fname'] + ' ' + i['lname']

    return passengers


def pass_post(payload, pass_id=None):
    """POST function with Passenger model and payload validation"""

    try:
        if not pass_id:
            validate(payload, schema=create_schema_pass)
        else:
            validate(payload, schema=update_schema_pass)

    except exceptions.ValidationError as error:
        resp = error_msgs[3]
        resp[0]['message'] = f'{resp[0]["message"]} {error}'

    else:
        if not pass_id:
            try:
                #create new item
                item = Passenger()
                for k in payload:
                    setattr(item, k, payload[k])
                db.session.add(item)
                db.session.commit()
                resp = error_msgs[5]
                resp[0]['item'] = item.fs_as_dict

            except Exception:
                resp = error_msgs[4]

        else:
            #update existing item
            old_item = Passenger.query.filter(Passenger.id == pass_id).first()
            if old_item:
                for k, v in payload.items():
                    setattr(old_item, k, v)
                db.session.commit()
                resp = error_msgs[6]
                resp[0]['item'] = old_item.fs_as_dict
            else:
                resp = error_msgs[1]

    return resp


def pass_delete(pass_id):
    """DELETE function with Passenger model"""

    item = Passenger.query.filter(Passenger.id == pass_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        resp = error_msgs[7]
        resp[0]['item'] = item.fs_as_dict
    else:
        resp = error_msgs[1]

    return resp
