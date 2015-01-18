from django.db import models
from django.contrib.auth.models import User
from django.forms.models import modelform_factory

import datetime
import os

class Note(models.Model):
	title 				= models.CharField(max_length=100)
	author 				= models.ForeignKey(User)
	publication_date 	= models.DateTimeField(blank=False, null=False)
	text 				= models.TextField(max_length=10000)

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.id:
			self.publication_date = datetime.datetime.now()
		return super(Note, self).save(*args,**kwargs)



def extension(self):
	name, extension = os.path.splitext(self)
	return extension

def get_upload_file_name(instance, filename):
	return "blog/media/images/%s_%s%s" % ("profile".replace('.','_'), instance.user.username, extension(filename))
	#return "blog/media/images/%s%s" % (instance.user.username, extension(filename))

def get_deleted_user():
    return User.objects.get_or_create(username='deleted')[0]

class UserProfile(models.Model):
	user 	= models.OneToOneField(User, unique=True)#, on_delete=models.SET(get_deleted_user))
	picture = models.ImageField(upload_to=get_upload_file_name, blank=True, null=True)

	def __unicode__(self):
		return unicode(self.picture.name) 

	def save(self, *args, **kwargs):
		try:
			existing = UserProfile.objects.get(user=self.user)
			self.id = existing.id #force update instead of insert
		except UserProfile.DoesNotExist:
			pass 
		models.Model.save(self, *args, **kwargs)


class Comment(models.Model):
	note 				= models.ForeignKey(Note)
	text 				= models.TextField(max_length=10000)
	author 				= models.ForeignKey(User)
	publication_date 	= models.DateTimeField(blank=False, null=False)
	#parent				= models.ForeignKey('self', blank=True, null=True, related_name='child_set')

	def __str__(self):
		return self.text

	def save(self, *args, **kwargs):
		if not self.id:
			self.publication_date = datetime.datetime.now()
		return super(Comment, self).save(*args,**kwargs)
