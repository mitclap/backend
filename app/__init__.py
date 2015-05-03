from flask import Flask, jsonify

app = Flask(__name__, static_url_path='/s', instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# USE ONLY ENV VARS FOR config

from .errors import ServerError, NotFoundError
from .models import db

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

from . import views
