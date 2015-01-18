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

from helpdesk.models import *
from helpdesk.forms import *

from django.contrib.auth.models import User, Group, Permission

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def helpdesk(request):
	tickets = Ticket.objects.all().order_by('-publication_date')

	if request.user.is_authenticated():
		curusertickets = Ticket.objects.filter(author=request.user)
	else:
		curusertickets = None
		return HttpResponseRedirect('/signin/')
	################ PAGINATION ###################

	#request.user.groups.all
	#group_tickets = Ticket.objects

	#ticket_list=Ticket.objects.all().order_by('-publication_date')
	#paginator = Paginator(ticket_list, 10, orphans=0, allow_empty_first_page=True) # Show 10 tickets per page
	#
	#page = request.GET.get('page')
	#try:
	#	tickets = paginator.page(page)
	#except PageNotAnInteger:
	#	# If page is not an integer, deliver first page.
	#	tickets = paginator.page(1)
	#except EmptyPage:
	#	# If page is out of range (e.g. 9999), deliver last page of results.
	#	tickets = paginator.page(paginator.num_pages)

	return render(request, 'helpdesk.html', {'tickets': tickets, 'curusertickets': curusertickets})

def create_ticket(request, template_name='create_ticket.html'):
	if request.user.is_authenticated():
		ticket = Ticket(author=request.user)
		if request.method == 'POST':
			form = TicketForm(request.POST, instance=ticket)
			if form.is_valid():
				ticket = form.save(commit=False)
				ticket.author = request.user
				#ticket.isopen = True
				ticket.save()
				return HttpResponseRedirect('/helpdesk/')
		else:
			form = TicketForm(instance=ticket)
		return render_to_response(template_name, {'form': form}, context_instance=RequestContext(request))
	else:
		return HttpResponse('For authenticated users only!')

def edit_ticket(request, ticket_id=None):
	if ticket_id:
		ticket = get_object_or_404(Ticket, pk=ticket_id)
		if not request.user.is_superuser and not request.user.is_staff and not ticket.author == request.user:
			return HttpResponse("404")
	else:
		return HttpResponse("404")

	if request.user.is_authenticated():
		if request.method == 'POST':
			ticketForm = TicketForm(request.POST, instance=ticket)
			if ticketForm.is_valid():
				ticketForm.save()
				return HttpResponseRedirect('/ticket/%s' % ticket_id)
		else:
			ticketForm = TicketForm(instance=ticket)

	return render(request, 'edit_ticket.html', {'ticketForm': ticketForm})

def delete_ticket(request, ticket_id=None):
	if request.user.is_superuser:
		ticket=Ticket.objects.get(id=ticket_id)
		ticket.delete()
		return HttpResponseRedirect('/helpdesk/')
	else:
		return HttpResponse("You are not allowed to do that!")			

#def edit_group(request, group_id=None, template_name='edit_group.html'):
#	if group_id:
#		group = get_object_or_404(Group, pk=group_id)
#		if not request.user.is_superuser:
#			return HttpResponse("404")
#	else:
#		userlist = User.objects.get(is_superuser=True)
#		group = UserGroup(created_by=request.user, userlist=userlist)
#
#	if request.user.is_authenticated():
#		if request.method == 'POST':
#			form = GroupForm(request.POST, instance=group)
#			if form.is_valid():
#				group = form.save(commit=False)
#				group.created_by = request.user
#				group.save()
#				if group_id:
#					return HttpResponseRedirect('/group/%s/' % group_id)
#				else:
#					return HttpResponseRedirect('/groups/')
#		else:
#			form = GroupForm(instance=group)
#		return render_to_response(template_name, {'form': form}, context_instance=RequestContext(request))
#	else:
#		return HttpResponse('For authenticated users only!')

def edit_group(request, group_id=None):
	if request.user.is_authenticated() and request.user.is_superuser:
		if group_id:
			group = get_object_or_404(Group, pk=group_id)
			if not request.user.is_superuser:
				return HttpResponse("You are not allowed to do that!")	
		else:
			group = Group()

		if request.method == 'POST':
			groupForm = GroupForm(request.POST)

			if groupForm.is_valid():
				if not group_id:
					group = Group.objects.create(name=request.POST['name'])
					superusers=User.objects.filter(is_superuser=True)
					for u in superusers:
						group.user_set.add(u)
				else:
					group.name = request.POST['name']
				group.save()
				return HttpResponseRedirect('/groups/')
			else:
				return HttpResponseRedirect('/groups/')

		else:
			groupForm = GroupForm(instance=group)	
	else:
		return HttpResponse("You are not allowed to do that!")
	return render(request, 'edit_group.html', {'groupForm': groupForm})


def delete_group(request, group_id):
	if request.user.is_superuser:
		group=Group.objects.get(id=group_id)
		group.delete()
		return HttpResponseRedirect('/groups/')
	else:
		return HttpResponse("You are not allowed to do that!")


def groups(request):
	groups=Group.objects.all().order_by('id')
	return render(request, 'groups.html', {'groups': groups})

def ticket(request, ticket_id=None):
	ticket = Ticket.objects.get(id=ticket_id)
	author = ticket.author

	### Comment section ###
	if request.user.is_authenticated():
		if request.method == 'POST':
			commentForm = CommentForm(request.POST)
			if commentForm.is_valid():
				comment = commentForm.save(commit=False)
				comment.ticket = ticket
				comment.author = request.user
				comment.text = request.POST['text']
				comment.save()
				return HttpResponseRedirect('/ticket/%s/' % ticket_id)
		else:
			commentForm = CommentForm()
	else:
		commentForm = CommentForm()
	comments_list=TicketComment.objects.filter(ticket__id=ticket_id)
	#######################

	return render(request, 'ticket.html', {'ticket':ticket, 'author':author, 'commentForm':commentForm, 'comments_list':comments_list})	
