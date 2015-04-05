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
