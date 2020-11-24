from django import forms
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	)
from django.conf import settings
from django import forms
from django.utils.safestring import mark_safe
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, MultiField, ButtonHolder, Submit, HTML
from crispy_forms.bootstrap import TabHolder, Tab, Div
from django.forms.models import modelformset_factory
from django.forms.models import inlineformset_factory
from django.forms.widgets import CheckboxSelectMultiple
from fields import TrustedMultipleChoiceField
from widgets import CheckboxSelectMultipleWithMapButton
from django.contrib.auth.models import Group, Permission
from django.contrib.admin.widgets import FilteredSelectMultiple,AdminDateWidget
from django.conf import settings
from datetime import date
from datetime import datetime
import time
import calendar
from models import *

User = get_user_model()

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		
		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("This user does not exist")
			if not user.check_password(password):
				raise forms.ValidationError("Incorrect password")
			if not user.is_active:
				raise forms.ValidationError("This user is no longer active")
		return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):
	email = forms.EmailField(label='Email Address')	
	password = forms.CharField(max_length=30,min_length=6, required=False, label="Password", widget=forms.PasswordInput)
	password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')	
	class Meta:
		model = User
		fields = [			
			'username',
			'email',			
			'password',			
			'employee',			
			'designation',
			'phone_number',
			'signature',
			'regional_staff',			
			'groups',

		]

	def __init__(self, *args, **kwargs):
		super(UserRegisterForm, self).__init__(*args, **kwargs)
		self.fields['groups'].widget = CheckboxSelectMultiple( choices=[ (x.id, x.name) for x in Group.objects.all().order_by("name")])
		self.helper = FormHelper(self)
		self.helper.layout = Layout(
		    Fieldset(
		        'User Registration',

		        Div(
		        	'username',
		        	'password',
					'password2',
					'email',														
					'phone_number',	
					'signature',			
					Submit('auth_user', 'Register User'),		        
		         	
		            css_class = "col-sm-6"
		            ),
		        Div(
		        	'employee',					
					'designation',	
					'regional_staff',				
		        	'groups',		        	    	
		        	 css_class = "col-sm-6"
		        	)
		        )
		    )

	def save(self, commit=True):
		user = super(UserRegisterForm, self).save(commit=False)
		if self.cleaned_data.get('password'):
		    user.set_password(self.cleaned_data.get('password'))		   
		if commit:			
		    user.save()
		    user.groups = self.cleaned_data.get('groups')
		    user.save()
		return user


	def clean_email(self):
		email = self.cleaned_data.get('email')	
		
		email_qs = User.objects.exclude(pk=self.instance.pk).filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("This email has already been registered")
		return email

	def clean_password2(self):	
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		if password != password2:
			raise forms.ValidationError("Passwords must match")
		return password

class fileUploadForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('signature',)
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': True}),
        }