# coding=utf-8
from __future__ import print_function

from wtforms import Form, BooleanField, DateTimeField, PasswordField, SelectField
from wtforms import StringField, SubmitField, Label, IntegerField
from wtforms import TextAreaField, TextField
from wtforms.validators import Length, required


class RegisteredUsersForm(Form):
	user_id = IntegerField('User ID', [required()])
	login_name = StringField('Login ID', [Length(max=255), required()])
	first_name = StringField('First Name', [Length(max=255), required()])
	last_name = StringField('Last Name', [Length(max=255), required()])
	job_title = StringField('Job Title', [Length(max=255)])
	manager = StringField('Manager', [Length(max=255)])
	account_status = SelectField('Account Status',
	                             choices=[('disabled', 'Disabled'), ('enabled', 'Enabled')], validators=[required()])
	user_password = PasswordField('Password', [Length(max=255), required()])
	created = DateTimeField('Created Date')
	modified = DateTimeField('Last Modified Date')
	memo = TextAreaField('Memo', [Length(max=1024)])


class UserRightsForm(Form):
	# user_id, modified, rights, memo
	user_id = IntegerField('User ID', [required()])
	rights = StringField('Access Rights', [Length(max=1024), required()])
	modified = DateTimeField('Last Modified Date')
	memo = TextAreaField('Memo', [Length(max=1024)])


class FaceFeatureMapForm(Form):
	# user_id, feature_map_[1,2,3], modified, memo
	user_id = IntegerField('User ID', [required()])
	feature_map_1 = StringField('Feature Map #1', [Length(max=255)])
	feature_map_2 = StringField('Feature Map #2', [Length(max=255)])
	feature_map_3 = StringField('Feature Map #3', [Length(max=255)])
	modified = DateTimeField('Last Modified Date')
	memo = TextAreaField('Memo', [Length(max=1024)])


if __name__ == "__main__":
	form = RegisteredUsersForm()
	print("Registered Users Form Demo")
	print(form.user_id.label)
	print(form.user_id)

