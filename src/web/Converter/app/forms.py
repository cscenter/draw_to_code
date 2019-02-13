from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.fields import IntegerField
from wtforms.validators import Required, InputRequired

class CircleNumberForm(FlaskForm):
    openid = IntegerField('Circle`s number', validators = [InputRequired()])
    #openid = SelectField('Circle`s number', choices=[('0',0), ('1',1), ('2',2), ('3',3), ('4',4), ('5',5), ('6',6), ('7',7)])
    submit = SubmitField('Justify?')
class EditTextForm(FlaskForm):
    tex_code = TextAreaField("tex_code")