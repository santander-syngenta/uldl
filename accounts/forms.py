from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import ClearableFileInput


class UploadPres(ModelForm):
	class Meta:
		model = Presentation
		fields = '__all__'
		widgets = {
			'pptx': ClearableFileInput(),
			'status': forms.RadioSelect(),
		}
		
		

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username','email','password1','password2']