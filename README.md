[![Build Status](https://app.travis-ci.com/VovaMazur/EPAM---python-online-project.svg?branch=master)](https://app.travis-ci.com/VovaMazur/EPAM---python-online-project)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
[![Coverage Status](https://coveralls.io/repos/github/VovaMazur/EPAM---python-online-project/badge.svg?branch=master)](https://coveralls.io/github/VovaMazur/EPAM---python-online-project?branch=master)
***

# Project description:

Manifestapp is the pet project on Python with the Flask framework. MySQL DB is used for the data storage.
Instance is run on the local machine (http://localhost:5000).

Application has web app and web api service. It was inspired by the [MANIFEST TV Series](https://en.wikipedia.org/wiki/Manifest_(TV_series))

Application CRUDs 2 entities related to the mentioned TV show:
- events details (callings of passengers)
- passenger details


# Instructions:

- [ ] Make sure you have python3.8+ and pip installed on your machine.
- [ ] App uses MySQL so you may need mysql-client installed as well.
- [ ] Create your virtual environment (e.g. `python -m venv venv`) and git clone from this repo.
- [ ] Enter newly installed directory (EPAM--..., equal to the project name).
- [ ] To install all dependencies, run `pip install -r requirements.txt`
- [ ] If all were done well, you may run application (`python app.py` in the root folder).

# Enjoy!


## Endpoints available:

|Endpoint|Methods|Rule|Description|
| --- | --- | --- | --- |
|***web api***|  |  |  |
|eventapi|DELETE, GET, POST|`/eventapi/all/<pass_id>/<datefrom>/<dateto>`|access all events by pass_id between datefrom and dateto|
|eventapi|DELETE, GET, POST|/eventapi/all/<pass_id> /<datefrom>|access all events by pass_id starting from datefrom|
|eventapi|DELETE, GET, POST|/eventapi/all/<pass_id>|access all events by pass_id|
|eventapi|DELETE, GET, POST|/eventapi/<event_id>|access event with event_id|
|eventapi|DELETE, GET, POST|/eventapi|access all events in the database|
|eventapi|DELETE, GET, POST|/eventapi/all|access all events in the database|
| | | | |
|passengerapi|DELETE, GET, POST|/passapi/<pass_id>/<string:status>|access passenger data with passenger_id (can be 'all') and having status|
|passengerapi|DELETE, GET, POST|/passapi/<pass_id>|access passenger data with passenger_id (can be 'all')| 
|passengerapi|DELETE, GET, POST|/passapi|access all passengers data|
| | | | |
|***web app***|  |  |  |
|events.main|GET, POST|/events/|events list, main screen for events|
|events.delete|GET|/events/delete/<item>|delete selected event|
|events.edit|GET, POST|/events/edit/<item>|update & create an event data|
| | | | |
|passengers.main|GET, POST|/passengers/|passengers list, main screen for passengers data|
|passengers.delete|GET|/passengers/delete/<item>|delete selected passenger|
|passengers.edit|GET, POST|/passengers/edit/<item>|update & create an passenger data|