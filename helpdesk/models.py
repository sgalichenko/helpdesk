from django.db import models
from django.contrib.auth.models import User, Group

import datetime
import os
import random
import time


class Ticket(models.Model):
	title = models.CharField(max_length=200)
	author = models.ForeignKey(User)
	publication_date = models.DateTimeField(blank=False, null=False)
	person = models.CharField(max_length=200, blank=True, null=True)
	email = models.EmailField(max_length=75, blank=True, null=True)
	phone = models.CharField(max_length=15, blank=True, null=True)
	text = models.TextField(max_length=10000)
	group = models.ForeignKey(Group)
	isopen = models.BooleanField(default=True, blank=False, null=False)

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.id:
			self.publication_date = datetime.datetime.now()
		
			#self.id = int(time.time())
			
			timestr = str(int(time.time()))
			self.id = int(timestr[6:]+timestr[4:6]+timestr[:4])

			#modulo = 999983 # prime
			#incrementor = 171803 # relative prime
			#self.id = 100003 # some start value
			#self.id = (self.id + incrementor) % modulo

		return super(Ticket, self).save(*args,**kwargs)

class TicketComment(models.Model):
	ticket = models.ForeignKey(Ticket)
	text = models.TextField(max_length=10000)
	author = models.ForeignKey(User)
	publication_date = models.DateTimeField(blank=False, null=False)

	def __str__(self):
		return self.text

	def save(self, *args, **kwargs):
		if not self.id:
			self.publication_date = datetime.datetime.now()
		return super(TicketComment, self).save(*args,**kwargs)


#class UserGroup(models.Model):
#	name = models.CharField(max_length=100)
#	userlist = models.ForeignKey(User, related_name="users")
#	creation_date = models.DateTimeField(blank=False, null=False)
#	created_by = models.ForeignKey(User, related_name="createdby")
#
#	def __str__(self):
#		return self.name
#
#	def save(self, *args, **kwargs):
#		if not self.id:
#			self.creation_date = datetime.datetime.now()
#		return super(UserGroup, self).save(*args,**kwargs)
