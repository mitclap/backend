from flask_wtf import Form
from wtforms import TextField, DateTimeField
from wtforms.validators import InputRequired, Length, Regexp

class SignupForm(Form):
    username = TextField(validators=[InputRequired(), Length(min=1, max=30), Regexp("^[a-zA-Z0-9]+$")])
    publicKey = TextField(validators=[InputRequired()]) # Add Length and Regexp as required

class AddEventForm(Form):
    name = TextField(validators=[InputRequired(), Length(min=2, max=30), Regexp("^[a-zA-Z0-9][a-zA-Z0-9 ]*[a-zA-Z0-9]+$")])
    start = DateTimeField(format='%Y-%m-%dT%H:%M:%S', validators=[InputRequired()])
    end = DateTimeField(format='%Y-%m-%dT%H:%M:%S', validators=[InputRequired()])
    description = TextField(validators=[InputRequired(), Length(min=0, max=1000)])
