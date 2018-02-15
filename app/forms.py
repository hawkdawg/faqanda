from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(
            label='Username',
            validators=[DataRequired()])
    password = PasswordField(
            label='Password',
            validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField(label='Sign In')
