from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.http import Http404
from django.http import HttpResponse

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404

from django.contrib import auth

from django.template import Template, Context
from django.template.loader import get_template

from blog.models import *
from blog.forms import *

from django.contrib.auth.models import User

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.hashers import check_password, make_password

import time

def blog(request, user_id=None):
	if user_id:
		notes_list=list(Note.objects.filter(author__id=user_id))
		if not notes_list:
			return HttpResponse("Selected user doesn't have any notes")
	else:
		notes_list=Note.objects.all().order_by('-id')

	paginator = Paginator(notes_list, 3, orphans=0, allow_empty_first_page=True) # Show 3 notes per page
	
	page = request.GET.get('page')
	try:
		notes = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		notes = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		notes = paginator.page(paginator.num_pages)

		#import os
		#print(os.path.join(os.path.dirname(__file__), 'media').replace('\\','/'))

	return render(request, 'blog.html', {'notes': notes})


def edit_note(request, note_id=None, template_name='edit_note.html'):
	if note_id:
		note = get_object_or_404(Note, pk=note_id)
		if note.author != request.user:
			if not request.user.is_superuser:
				return HttpResponse("404")
	else:
		note = Note(author=request.user)

	if request.user.is_authenticated():
		if request.method == 'POST':
			form = NoteForm(request.POST, instance=note)
			if form.is_valid():
				note = form.save(commit=False)
				note.author = request.user
				note.save()
				if note_id:
					return HttpResponseRedirect('/note/%s/' % note_id)
				else:
					return HttpResponseRedirect('/')
		else:
			form = NoteForm(instance=note)
		return render_to_response(template_name, {'form': form}, context_instance=RequestContext(request))
	else:
		return HttpResponse('For authenticated users only!')


def note(request, note_id=None):
	note = Note.objects.get(id=note_id)
	author = note.author

	### Comment section ###
	if request.user.is_authenticated():
		if request.method == 'POST':
			commentForm = CommentForm(request.POST)
			if commentForm.is_valid():
				comment = commentForm.save(commit=False)
				comment.note = note
				comment.author = request.user
				comment.text = request.POST['text']
				print("COMMENT ADDED! ", comment.text)
				comment.save()
				return HttpResponseRedirect('/note/%s/' % note_id)
		else:
			commentForm = CommentForm()
	else:
		commentForm = CommentForm()
	#else:
	#	return HttpResponse('For authenticated users only!')

	comments_list=Comment.objects.filter(note__id=note_id)
	#######################

	return render(request, 'note.html', {'note':note, 'author':author, 'commentForm':commentForm, 'comments_list':comments_list})	


def delete_note(request, note_id):
	note=Note.objects.get(id=note_id)
	author = note.author
	if request.user.is_superuser or author == request.user:
		note.delete()
		return HttpResponseRedirect('/')
	else:
		return HttpResponse("You are not allowed to do that!")

def delete_comment(request, comment_id):
	comment=Comment.objects.get(id=comment_id)
	note=comment.note
	author = comment.author
	if request.user.is_superuser or author == request.user:
		comment.delete()
		return HttpResponseRedirect('/note/%s/' % note.id)
	else:
		return HttpResponse("You are not allowed to do that!")


def users(request):
	if request.user.is_superuser:
		users=User.objects.all()
		return render(request, 'users.html', {'users': users})
	else:
		return HttpResponse("For superusers only")


def user(request, user_id):
	author=User.objects.get(id=user_id)
	return render(request, 'user.html', {'author': author})


def delete_user(request, user_id):
	user=User.objects.get(id=user_id)
	if request.user.is_superuser or user.id == request.user.id:
		if user.id != request.user.id:
			user.delete()
			return HttpResponseRedirect('/users/')
		else:
			user.delete()
			return HttpResponseRedirect('/')
	else:
		return HttpResponse("You are not allowed to do that!")


def signup(request):
	user = User(id=request.user.id)

	if request.method == 'POST':
		userForm = SignupForm(request.POST, instance=user)

		if userForm.is_valid():
			user = userForm.save(commit=False)
			user.set_password(userForm.cleaned_data['password'])
			#user = User.objects.create_user(
			#	username = request.POST['username'], 
			#	email = request.POST['email'],
			#	password = request.POST['password']
			#)
			user.save()

			return HttpResponseRedirect('/signin/')

	else:
		userForm = SignupForm(instance=user)
	return render(request, 'signup.html', {'userForm': userForm})


def edit_user(request, user_id=None):
	user = get_object_or_404(User, pk=user_id)
	print(user_id != request.user.id)
	print(user_id)
	print(request.user.id)
	if int(user_id) != request.user.id and not request.user.is_superuser:
		return HttpResponse("You are not allowed to do that!")	
	
	if request.method == 'POST':
		if request.user.is_superuser:
			userForm = EditFormForSuperuser(request.POST, instance=user)
		else:
			userForm = EditForm(request.POST, instance=user)

		if userForm.is_valid():
			userForm.save()

			#if request.user.is_superuser:
			#	newpassword = userForm.cleaned_data['newpassword']
			#	passwd = make_password(newpassword)
			#	user.password = passwd
			#	user.save()

			profileForm = ProfileForm(request.POST, request.FILES, instance=user)
			if profileForm.is_valid():
				profile = profileForm.save(commit=False)

				# Superuser can change anyones' picture
				# And users can change only their own pictures
				if request.user.is_superuser:
					profile.user = user
				else:
					profile.user = request.user
				profile.save()
			return HttpResponseRedirect('/user/%s/' % user.id)
	else:
		# Different forms for superusers, users and guests
		if request.user.is_superuser:
			userForm = EditFormForSuperuser(instance=user)
		else:
			userForm = EditForm(instance=user)		
		profileForm = ProfileForm(instance=user)
	return render(request, 'edit_user.html', {'userForm': userForm, 'profileForm': profileForm})


def signin(request):
	if request.user is not None and request.user.is_active:
		return HttpResponseRedirect('helpdesk')
	else:
		if request.method == 'POST':
			form = SigninForm(request.POST)
			#if form.is_valid():
			#username = request.POST.get('username', '')
			#password = request.POST.get('password', '')
			username = request.POST['username']
			password = request.POST['password']
			user = auth.authenticate(username=username, password=password)
			if user is not None and user.is_active:
				auth.login(request, user)
				return HttpResponseRedirect('/helpdesk/')
			else:
				return HttpResponse("ERROR")
		else:
			form = SigninForm()
	return render(request, 'signin.html', {'form': form})


def logout(request):
	auth.logout(request)
	response = HttpResponseRedirect('/')
	response.delete_cookie('sessionid')
	return response


def passwd(request):
	if request.user.is_authenticated and request.user.is_active:
		if request.method == "POST":
			passwdForm = PasswdForm(request.POST)

			if passwdForm.is_valid():
				oldpassword = passwdForm.cleaned_data['oldpassword']
				repeat = passwdForm.cleaned_data['repeat']
				encoded = request.user.password

				if oldpassword == repeat and check_password(oldpassword, encoded):
					newpassword = passwdForm.cleaned_data['newpassword']
					passwd = make_password(newpassword)
					request.user.password = passwd
					request.user.save()

					return HttpResponseRedirect("/user/%s/" % request.user.id)					
				else:
					return HttpResponse("Check your current password!")
		else:
			passwdForm = PasswdForm()

	return render(request, 'passwd.html', {'passwdForm': passwdForm})