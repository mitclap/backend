from flask_wtf import Form
from wtforms import TextField, DateTimeField
from wtforms.validators import InputRequired, Length, Regexp

class SignupForm(Form):
    username = TextField(validators=[InputRequired(), Length(min=1, max=30), Regexp("^[a-zA-Z0-9]+$")])
    publicKey = TextField(validators=[InputRequired()]) # Add Length and Regexp as required

class AddEventForm(Form):
    name = TextField(validators=[InputRequired(), Length(min=1, max=30), Regexp("^[a-zA-Z0-9]+$")])
    start = DateTimeField(format='%Y-%m-%dT%H:%M:00.000+0000', validators=[InputRequired()])
    end = DateTimeField(format='%Y-%m-%dT%H:%M:00.000+0000', validators=[InputRequired()])
    description = TextField(validators=[InputRequired(), Length(min=0, max=1000)])
