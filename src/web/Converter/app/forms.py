from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, SubmitField
from wtforms.fields import IntegerField
from wtforms.validators import Required

class CircleNumberForm(FlaskForm):
    openid = IntegerField('Circle`s number', validators = [Required()])
    submit = SubmitField('Justify')