"""Read Functions"""
from manifestapp.models import Event, Passenger


def event_get_bypass(passid=None, datefrom=None, dateto=None):
    """Read function with Event model by other parameters"""

    passid = None if not passid.isdigit() else int(passid)

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

    outcome = Event.fs_json_list(items) if items else []

    return outcome


def event_get_byid(event_id):
    """Read function with Event model by event ID"""

    item = Event.query.get(event_id)
    outcome = Event.fs_json_list([item]) if item else []

    return outcome


def pass_get_bystatus(status=None):
    """Read function with Passenger model all / by statuses"""

    if status:
        items = Passenger.query.filter(Passenger.status == status).all()
    else:
        items = Passenger.query.all()

    outcome = Passenger.fs_json_list(items) if items else []

    return outcome


def pass_get_byid(passid):
    """Read function with Passenger model by passenger ID"""

    item = Passenger.query.get(passid)
    outcome = Passenger.fs_json_list([item]) if item else []

    return outcome


