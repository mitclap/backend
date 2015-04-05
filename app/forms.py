from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import InputRequired, Length, Regexp

class SignupForm(Form):
    username = TextField(validators=[InputRequired(), Length(min=1, max=30), Regexp("^[a-zA-Z0-9]+$")])
    publicKey = TextField(validators=[InputRequired()]) # Add Length and Regexp as required
