from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,SelectField,IntegerField
from wtforms.validators import DataRequired,ValidationError,Email,EqualTo
from wtforms.widgets import TextArea
from app.models import User,Room
from flask import flash

class LoginForm(FlaskForm):
	username = StringField('Username',validators = [DataRequired()])
	password = PasswordField('password',validators = [DataRequired()])
	remember_me = BooleanField('Remember_me')
	submit = SubmitField('Sign-In')

class RegistrationForm(FlaskForm):
	username = StringField('Username',validators = [DataRequired()])
	email = StringField('IIIT-email',validators = [DataRequired(),Email()])
	batch = StringField('Batch',validators = [DataRequired()])
	city = StringField('city',validators=[DataRequired()])
	password = PasswordField('password',validators = [DataRequired()])
	password2 = PasswordField('Re-type the password',validators = [DataRequired(),EqualTo('password')])
	submit = SubmitField('Register')

	def validate_username(self,username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please select a different username')

		def validate_email(self,email):
			user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('This email-id has already been registered')

class Postform(FlaskForm):
	body = StringField('Text',validators=[DataRequired()],widget=TextArea() )
	submit = SubmitField('Post')

class Like(FlaskForm):
	submit = SubmitField('Like')

class RoomForm(FlaskForm):
	# hostel = StringField('Hostel', validators=[DataRequired()])
	# block = StringField('Block', validators=[DataRequired()])
	roomno = IntegerField('Room No', validators=[DataRequired()])
	submit = SubmitField('Submit')

	def check_availabity_room(self, roomno, current_user):
		if ((100 < roomno and roomno < 133) or (200 < roomno and roomno < 233) or (300 < roomno and roomno < 333)):			
			if len(Room.query.filter_by(user_id = current_user.id).all()) > 0:
				flash('Sorry! You already booked a room. You cannot book another room.')
				return False
			if len(Room.query.filter_by(roomno = roomno).all()) > 2:
				flash('This room is already full.Please select other room')
				return False
		else:
			flash('Please enter a valid Room No. between 101 and 132 or 201 and 232 or 301 and 332.')
			return False
		return True