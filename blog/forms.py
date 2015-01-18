from django import forms
from django.forms import ModelForm

from django.contrib.auth.models import User

from blog.models import Note
from blog.models import Comment
from blog.models import UserProfile


from pagedown.widgets import PagedownWidget 



from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Hidden, Fieldset
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class NoteForm(forms.ModelForm):
	class Meta:
		model = Note
		
		fields = ['title', 'text']

	def clean_message(self):
		text = self.cleaned_data['text']
		num_words = len(text.split())
		if num_words < 4:
			raise forms.ValidationError("Text is too small!")
		return text

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['text']

	def clean_message(self):
		text = self.cleaned_data['text']
		num_words = len(text.split())
		if num_words < 4:
			raise forms.ValidationError("Text is too small!")
		return text


class SignupForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password']

	def clean_message(self):
		password = self.cleaned_data['password']
		if len(password) < 5:
			raise forms.ValidationError("Password is way too simple. Make up a new one, please.")
		return password

	def clean_email(self):
		email = self.cleaned_data.get('email')
		username = self.cleaned_data.get('username')
		if email and User.objects.filter(email=email).exclude(username=username).count():
			raise forms.ValidationError(u'This email has already been registered.')
		return email

class EditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email']

class ProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['picture']

class EditFormForSuperuser(forms.ModelForm):
	#newpassword = forms.CharField(required=False, label='New password')
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email', 'password', 'is_active', 'is_staff', 'is_superuser', 'groups']

		widgets = {
            'groups': forms.SelectMultiple(attrs={'class': 'chosen groups'}),
        }

class SigninForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ['username', 'password']

	def __init__(self, *args, **kwargs):
		super(SigninForm, self).__init__(*args, **kwargs)

		for fieldname in ['username', 'password']:
			self.fields[fieldname].help_text = None

class PasswdForm(forms.Form):
	oldpassword = forms.CharField(required=True, label='Current password')
	repeat = forms.CharField(required=True, label='Repeat current password')
	newpassword = forms.CharField(required=True, label='New password')


#	def is_valid(self):
#		valid = super(SigninForm, self).is_valid()
#		if not valid:
#			return valid
#		try:
#			user = User.objects.get(
#				Q(username=self.cleaned_data['username']) | Q(email=self.cleaned_data['username'])
#			)
#		except User.DoesNotExist:
#			self._errors['no_user'] = 'User does not exist'
#			return False
#		if not check_password(self.cleaned_data['password'], user.password):
#			self._errors['invalid_password'] = 'Password is invalid'
#			return False
#		return True