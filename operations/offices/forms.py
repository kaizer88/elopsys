from django.conf import settings
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.utils.safestring import mark_safe
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, MultiField, ButtonHolder, Submit, HTML
from crispy_forms.bootstrap import TabHolder, Tab, Div
from .models import *
from django.db.models import Q
from employees.models import *
from offices.models import *
from datetime import datetime
from django.forms.widgets import HiddenInput
from propfac.models import *


class MobileNumberForm(forms.ModelForm):
	class Meta:
		model = MobileNumber
		fields = '__all__'
		widgets = {
            'purchase_date': forms.TextInput(attrs={'class': 'datepicker'}),          
                      
        }
	def __init__(self, *args, **kwargs):        
		user = kwargs.pop('user')
		super(MobileNumberForm, self).__init__(*args, **kwargs)
		
		# self.fields['service_booking_number'].queryset = ServiceBookings.objects.filter(vehicle=instance.vehicle)
		self.helper = FormHelper(self)
		self.helper.layout = Layout(
		    Fieldset(
		        '',
		        Div(
		            'phone_number',                                    
		            'sim_number', 
		            'service_provider',                   
		            'active',                    
		            css_class = "col-sm-4"),
		        Div(
                    HTML(" {% include 'mobilenumbers.html' %} "),
                    css_class = "col-sm-8")
		     
		        )
		    )

class CardAllocationForm(forms.ModelForm):
    class Meta:
        model = CardAllocation
        fields = '__all__'
        widgets = {
            'allocation_date': forms.TextInput(attrs={'class': 'datepicker'}),          
                      
        } 
    
    def __init__(self, *args, **kwargs):        
        user = kwargs.pop('user')
        super(CardAllocationForm, self).__init__(*args, **kwargs)
        if not user.has_perm('fleet.authorize_vehiclemaintenance'):
            self.fields["authorize"].widget = HiddenInput()  
        
        # self.fields['service_booking_number'].queryset = ServiceBookings.objects.filter(vehicle=instance.vehicle)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Card Allocation Details',

                Div(
                	'employee',
                	'allocation_date',
                	'allocation_type',
                    'mobile_number',                                    
                    'parckage', 
                    'fuel_card',                   
                    'fuel_cycle_limit',
                    'accept',
                	'authorize',
                css_class = "col-sm-3"),
               Div(
                    HTML(" {% include 'cardallocations.html' %}"),
                    css_class = "col-sm-9")
             
             
                )
            )




class RegionForm(forms.ModelForm):
	class Meta:
		model = Region
		fields = ['region', 'prefix']
	

	def clean_region(self):
		region = self.cleaned_data.get('region')
		return region

	def clean_prefix(self):
		prefix = self.cleaned_data.get('prefix')
		return prefix


class BranchForm(forms.ModelForm):
	class Meta:
		model = Branch
		fields = '__all__'

	def clean_branch(self):
		branch = self.cleaned_data.get('branch')
		return branch

	def clean_prefix(self):
		prefix = self.cleaned_data.get('prefix')
		return prefix

	def clean_office_type(self):
		office_type = self.cleaned_data.get('office_type')
		return office_type

	def clean_telephone(self):
		address = self.cleaned_data.get('address')
		return address

	def clean_address(self):
		address = self.cleaned_data.get('address')
		return address

	def clean_telephone(self):
		telephone = self.cleaned_data.get('telephone')
		return telephone

	def clean_fax(self):
		fax = self.cleaned_data.get('fax')
		return fax

class DepartmentForm(forms.ModelForm):
	class Meta:
		model = Department
		fields = '__all__'

class SectionForm(forms.ModelForm):
	class Meta:
		model = Section
		fields = '__all__'

class FloorForm(forms.ModelForm):
	class Meta:
		model = Floor
		fields = '__all__'

class fileUploadForm(forms.ModelForm):
    class Meta:
        model = PFDocument
        fields = ('file',)
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': True}),
        }

class CommentsForm(forms.ModelForm):
    class Meta:
        model = PFComment
        fields = ('comments',)
        widgets = {            
            'comments': forms.Textarea(),
        }