from __future__ import print_function

from contextlib import contextmanager
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import func


from .errors import ServerError

db = SQLAlchemy()

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = db.session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

@contextmanager
def db_safety():
    try:
        with session_scope() as session:
            yield session
    except Exception as e:
        raise ServerError()

class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    public_key = db.Column(db.String(68))

    @staticmethod
    def lookup_from_username(username):
        return Account.query.filter(func.lower(Account.username) == func.lower(username)).first()

    @staticmethod
    def create(session, username, public_key):
        new_account = Account(username, public_key)
        session.add(new_account)
        session.flush()

        return new_account.id

    def __init__(self, username, public_key):
        self.username = username
        self.public_key = public_key

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    start = db.Column(db.DateTime())
    end = db.Column(db.DateTime())
    description = db.Column(db.String(1000))

    @staticmethod
    def create(session, name, start, end, description):
        new_event = Event(name, start, end, description)
        session.add(new_event)
        session.flush()

        return new_event.id

    def __init__(self, name, start, end, description):
        self.name = name
        self.start = start
        self.end = end
        self.description = description

class Attendee(db.Model):
    __tablename__ = 'attendees'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer(), db.ForeignKey('events.id'))
    account_id = db.Column(db.Integer(), db.ForeignKey('accounts.id'))

    @staticmethod
    def lookup_from_ids(account_id ,event_id):
        return Attendee.query.filter((Attendee.account_id == account_id) and \
            (Attendee.event_id == event_id)).first()

    @staticmethod
    def create(session, event_id, account_id):
        new_attendee = Account(event_id, account_id)
        session.add(new_attendee)
        session.flush()

        return new_attendee.id

    def __init__(self, event_id, account_id):
        self.event_id = event_id
        self.account_id = account_id

class Checkin(db.Model):
    __tablename__ = 'checkins'

    id = db.Column(db.Integer, primary_key=True)
    attendee_id = db.Column(db.Integer(), db.ForeignKey('attendees.id'))
    timestamp = db.Column(db.DateTime())
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())

    @staticmethod
    def create(session, attendee_id, timestamp, latitude, longitude):
        new_checkin = Checkin(attendee_id, timestamp, latitude, longitude)
        session.add(new_checkin)
        session.flush()

        return new_checkin.id

    def __init__(self, attendee_id, timestamp, latitude, longitude):
        self.attendee_id = attendee_id
        self.timestamp = timestamp
        self.latitude = latitude
        self.longitude = longitude
