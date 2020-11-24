
from django import forms
from .models import SignUp

class SignUpForm(forms.ModelForm):
	class Meta:
		model = SignUp
		fields = ['full_name', 'email']

	def clean_email(self):
		email = self.cleaned_data.get('email')
		email_base, provider = email.split("@")
		domain, extension = provider.split('.')
		if not domain == 'emeraldlife.co':
			raise forms.ValidationError("Please use your valid Emerald Life email")
		if not extension == "za":
			raise forms.ValidationError("Please a valid Emerald Life email address")		
		return email

	def clean_full_name(self):
		full_name = self.cleaned_data.get('full_name')
		return full_name



class ContactForm(forms.Form):
	full_name = forms.CharField()
	email = forms.EmailField()
	message = forms.CharField()