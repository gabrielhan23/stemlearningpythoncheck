from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange, Regexp
from wtforms.fields.html5 import IntegerField

from files.setup import *
from files.databases import *

class RegistrationForm(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired(),
                                Length(min=2, max=20), Regexp('^[a-z]+$', message="Username must contain only lower case letters")])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(),
                                        EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AccountForm(FlaskForm):
    oldpassword = PasswordField('Old Password', validators=[DataRequired()])
    newpassword = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(),
                                        EqualTo('newpassword')])
    submit = SubmitField('Change Password')

class AdminPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Change Password')

class QuestionForm(FlaskForm):
    code = TextAreaField('Code', validators=[DataRequired()])
    submit = SubmitField('Submit')