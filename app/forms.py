# Login Class
# Login Class

# Signup Class Form

# Forgotten password form

# Editprofile form

# New Post form

# Edit Post Form

# New message form

# Search bar form

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	firstname = StringField('Firstname', validators=[DataRequired()])
	lastname = StringField('Lastname', validators=[DataRequired()])
	website = StringField('Website') #website validator?
	bio = StringField('Bio')
	
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email address.')

class EditProfile(FlaskForm):
	username = StringField("Username", render_kw={"placeholder": "username"})
	email = StringField('Email')
	firstname = StringField('Firstname')
	lastname = StringField('Lastname')
	website = StringField('Website')
	bio = StringField('Bio')
	submit = SubmitField('Submit')

	def validate_username(self, username):
		if username.data != "":
			user = User.query.filter_by(username=username.data).first()
			if user is not None:
				raise ValidationError('Please use a different username.')

	def validate_email(self, email):
		if email.data != "":
			user = User.query.filter_by(email=email.data).first()
			if user is not None:
				raise ValidationError('Please use a different email address.')

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')