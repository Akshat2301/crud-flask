from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import InputRequired, DataRequired, Length, Email, EqualTo, ValidationError
from pythonProject.models import emp_details


class RegistrationForm(FlaskForm):
    firstName = StringField('First name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    lastName = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    phone = StringField('Phone Number',
                        validators=[DataRequired(), Length(min=10, max=11)])
    address = StringField('Address')
    dob = DateField('Date-Of-Birth')
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        emp = emp_details.query.filter_by(email=email.data).first()
        if emp:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    emailID = StringField('EmailID', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8)])