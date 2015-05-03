from __future__ import absolute_import

from flask import jsonify, request

from . import app
from .errors import ServerError, BadDataError
from .forms import  SignupForm, AddEventForm
from .models import db_safety, Account, Event, Attendee

@app.route('/accounts', methods=['POST'])
def signup():
    try:
      form = SignupForm(csrf_enabled=False)
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
    return jsonify({'message': 'Account successfully created'})

@app.route('/events', methods=['POST'])
def new_event():
    try:
      form = AddEventForm(csrf_enabled=False)
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
    return jsonify({'message': 'Event successfully created', 'event_id': event_id})

@app.route('/events', methods=['GET'])
# TODO: generalize beyond just user events
def get_events():
    # TODO: add pagination
    attendee_ids = request.args.getlist("attendee_id")
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
        # TODO: fix serialization
        events = [{'id': event.id,
          'name': event.name,
          'start' : event.start.strftime("%Y-%m-%dT%H:%M:%S"), # TODO: extract constant
          'end' : event.end.strftime("%Y-%m-%dT%H:%M:%S"),
          'description': event.description} for event in events]
    return jsonify({"events": events})
