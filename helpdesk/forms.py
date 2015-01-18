from django import forms
from django.forms import ModelForm

from django.contrib.auth.models import User, Group

from helpdesk.models import Ticket, TicketComment

from pagedown.widgets import PagedownWidget 

class TicketForm(forms.ModelForm):
	class Meta:
		model = Ticket
		fields = ['email', 'person', 'phone', 'group', 'title', 'text', 'isopen']
		exclude = ['author', 'publication_date']

	def __init__(self, *args, **kwargs):
		super(TicketForm, self).__init__(*args, **kwargs)
		self.fields['isopen'].label = "Open"

	def clean_message(self):
		text = self.cleaned_data['text']
		num_words = len(text.split())
		if num_words < 4:
			raise forms.ValidationError("Text is too small!")
		return text


class CommentForm(forms.ModelForm):
	class Meta:
		model = TicketComment
		fields = ['text']

	def clean_message(self):
		text = self.cleaned_data['text']
		num_words = len(text.split())
		if num_words < 4:
			raise forms.ValidationError("Text is too small!")
		return text



class GroupForm(forms.ModelForm):
	class Meta:
		model = Group
		fields = ['name', 'permissions']