from __future__ import unicode_literals
import re
from django.db import models
import bcrypt
import datetime


EMAIL_MATCH = re.compile(r'^^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$')

class UserManager(models.Manager):
	def validate_registration(self, post_data):
		errors = []
		user = None
		
		for key, value in post_data.iteritems():
			if len(value) < 1:
				errors.append("All fields are required")
				break

		if len(post_data['name']) < 3:
			errors.append("Name field must be at least 3 characters")

		if len(post_data['password']) < 8:
			errors.append("Password field must be at least 8 characters")	

		
		if not re.match(EMAIL_MATCH, post_data['email']):
			errors.append("Email not valid")


		if self.filter(email=post_data['email']):
			errors.append("Email in use")


		if post_data['password'] != post_data['password_confirm']:
			errors.append("Passwords do not match")


		if not errors:
			hashed_pw = bcrypt.hashpw(post_data['password'].encode(), bcrypt.gensalt())
			user = self.create(
				name = post_data['name'],
				email = post_data['email'],
				password = hashed_pw,
				birthday = post_data['birthday']
			)
	
		return errors, user

	def validate_login(self, post_data):
		errors = []
		user = None

		if not self.filter(email=post_data['email']):
			errors.append("Invalid email/password")
		else:
			user = self.get(email=post_data['email'])
			if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
				errors.append("Invalid email/password")
		return errors, user

class User(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField(unique=True)
	password = models.CharField(max_length=20)
	birthday = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()

	def __str__(self):
		return "{} {}".format(self.name)

class Appointment(models.Model):
	PENDING = 1
	DONE = 2
	MISSED = 3
	STATUS_CHOICES = (
		(PENDING, 'Pending'),
		(DONE, 'Done'),
		(MISSED, 'Missed'),
	)
	task = models.CharField(max_length=255)
	task_time = models.TimeField()
	task_date = models.DateField()
	task_status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
	task_creator = models.ForeignKey(User, related_name="appointments")
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "Note by User #{}".format(self.task_creator.id)