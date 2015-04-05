from __future__ import print_function
from os import environ

from flask import Flask, jsonify, request
from flask_socketio import SocketIO

app = Flask(__name__, static_url_path='/s', instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
socketio = SocketIO(app)

# USE ONLY ENV VARS FOR config

from .errors import ServerError, BadDataError, NotFoundError
from .forms import SignupForm
from .models import db, Account, db_safety

app.secret_key = app.config['SECRET_KEY'] # For Flask

db.init_app(app)

@app.errorhandler(404)
def not_found(error):
    return handle_server_error(NotFoundError())

@app.errorhandler(405)
def method_not_allowed(error):
    # 405 is method not allowed
    # just pretend the endpoint doesn't exist
    # Can't call abort because Flask won't rehandle the reraised HTTPException
    # to prevent infinite loops
    return not_found(error)

@app.errorhandler(ServerError)
def handle_server_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@socketio.on('connect')
def test_connect():
    print('got a connection')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@app.route('/accounts', methods=['POST'])
def signup():
    try:
      form = SignupForm(csrf_enabled=False)
    except Exception as e: # Otherwise there's a 400 that's propagated
      raise BadDataError()
    if not form.validate_on_submit():
      raise BadDataError()
    username = form.username.data
    public_key = form.public_key.data
    if Account.lookup_from_username(username) != None:
      raise ServerError('This account already exists!', status_code=409)
    with db_safety() as session:
        account_id = Account.create(session, username, public_key)
    return jsonify({'message': 'Account successfully created'})
