from __future__ import absolute_import

from flask import jsonify, request, abort

from . import app
from .errors import ServerError, BadDataError
from .forms import  SignupForm, AddEventForm, CheckinForm
from .models import db_safety, Account, Event, Attendee, Checkin

@app.route('/accounts', methods=['POST'])
def signup():
    try:
      form = SignupForm.from_json(request.json)
    except Exception as e: # Otherwise there's a 400 that's propagated
      raise BadDataError()
    if not form.validate_on_submit():
      raise BadDataError()
    username = form.username.data
    public_key = form.publicKey.data
    if Account.lookup_from_username(username) != None:
      raise ServerError('This account already exists!', status_code=409)
    with db_safety() as session:
        account_id = Account.create(session, username, public_key)
    return jsonify({'message': 'Account successfully created', 'data': {'accountId': account_id}})

@app.route('/events', methods=['POST'])
def new_event():
    try:
      form = AddEventForm.from_json(request.json)
    except Exception as e: # Otherwise there's a 400 that's propagated
      raise BadDataError()
    if not form.validate_on_submit():
      raise BadDataError()
    name = form.name.data
    start = form.start.data
    end = form.end.data
    description = form.description.data
    if start >= end:
      raise BadDataError()
    with db_safety() as session:
        event_id = Event.create(session, name, start, end, description)
    return jsonify({'message': 'Event successfully created', 'data': {'eventId': event_id}})

@app.route('/events', methods=['GET'])
# TODO: generalize beyond just user events
def get_events():
    # TODO: add pagination
    attendee_ids = request.args.getlist('attendee_id')
    if len(attendee_ids) != 1:
        raise BadDataError()
    try:
        attendee_id = int(attendee_ids[0])
    except ValueError as e:
        raise BadDataError()
    with db_safety() as session:
        # TODO: check authentication simultaneously to avoid TOCTOU
        # TODO: get rest of event info i.e. attendees
        events = session.query(Event) \
          .join(Attendee, Event.id==Attendee.event_id) \
          .filter(Attendee.account_id == attendee_id).all()
        for event in events:
          attendees = session.query(Attendee) \
            .filter(Attendee.event_id == event.id).all()
          event.attendees = []
          for attendee in attendees:
            event.attendees.append(attendee.account_id)
        # TODO: fix serialization
        events = [{'id': event.id,
          'name': event.name,
          'start' : event.start.strftime('%Y-%m-%dT%H:%M:%S'), # TODO: extract constant
          'end' : event.end.strftime('%Y-%m-%dT%H:%M:%S'),
          'description': event.description,
          'attendees': event.attendees} for event in events
          ]
    return jsonify({'message': '', 'data': {'events': events}})

@app.route('/checkins', methods=['POST'])
def add_checkin():
    try:
        form = CheckinForm.from_json(request.json)
    except Exception as e: # Otherwise there's a 400 that's propagated
        raise BadDataError()
    if not form.validate_on_submit():
        raise BadDataError()
    event_id = form.eventId.data
    account_id = form.accountId.data
    timestamp = form.timestamp.data
    latitude = form.location.latitude.data
    longitude = form.location.longitude.data
    with db_safety() as session:
        attendee = Attendee.lookup_from_ids(account_id, event_id)
        if None == attendee:
            abort(404)
        checkin_id = Checkin.create(session, attendee.id, timestamp, latitude, longitude)
    return jsonify({'message': 'Checkin successfully created', 'data': {'checkinId': checkin_id}})

@app.route('/checkins', methods=['GET'])
def get_checkins():
    event_ids = request.args.getlist('event_id')
    if len(event_ids) != 1:
        raise BadDataError()
    try:
        event_id = int(event_ids[0])
    except ValueError as e:
        raise BadDataError()
    with db_safety() as session:
        attendees = session.query(Attendee).distinct(Attendee.account_id) \
          .filter(Attendee.event_id == event_id).all()
        attendee_locations = []
        for attendee in attendees:
            attendee_latest_checkin = session.query(Checkin) \
              .filter(Checkin.attendee_id == attendee.id).order_by(Checkin.timestamp).first()
            attendee_username = session.query(Account) \
              .filter(Account.id == attendee.account_id).first()
            try:
              attendee_locations.append({'account_id':attendee.account_id, \
                'username':attendee_username.username, \
                'latitude':attendee_latest_checkin.latitude, \
                'longitude':attendee_latest_checkin.longitude})
            except Exception as e:
                print e, 'attendee probably has not checked in yet' #TODO: make this better
    return jsonify({'message': '', 'data': {'attendee_locations': attendee_locations}})
