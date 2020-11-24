import os

from django.conf import settings
from django import forms
from django.db.models import Q
from datetime import datetime
from django.db.models import Value as V
from django.db.models.functions import Concat
from dal import autocomplete, forward
from django.forms.widgets import *
from django.core.exceptions import ValidationError

from models import OperationsUser, Region, Branch, Document, Address, Contact, Insurer, BaseTicket, ServiceProvider, Vendor
from models import VendorBankDetail

from employees.models import Employee

class OperationsUserForm(forms.ModelForm):

    password1 = forms.CharField(
        required=False, label="Password (leave empty if not changed)", widget=forms.PasswordInput)
    password2 = forms.CharField(
        required=False, label="Re-enter password", widget=forms.PasswordInput)
    region = forms.ModelChoiceField(required=False,
                                    queryset=Region.objects.all(),
                                    empty_label=None,
                                    widget=autocomplete.ListSelect2(url='region_autocomplete',
                                    attrs={'data-placeholder': "---------"}
                                    ))

    district = forms.ModelChoiceField(required=False,
                                      queryset=Branch.objects.all(),
                                      empty_label=None,
                                      widget=autocomplete.ListSelect2(url='district_autocomplete',
                                      attrs={'data-placeholder': "---------"},
                                      forward=('region',)
                                      ))        
    class Meta:
        model = OperationsUser
        fields = ['first_name','last_name','username','email','phone_number',
                  'region','district','signature','groups','regional_staff',
                  'is_active']       
        widgets = {'groups': forms.CheckboxSelectMultiple()}

    def __init__(self, *args, **kwargs):
        super(OperationsUserForm, self).__init__(*args, **kwargs)
#        self.fields['district'].widget = SelectMultiple()
        self.fields['district'].widget.attrs['class'] = 'multi_select'
        
    def clean_password1(self):
        if not self.cleaned_data.get('password1') and not self.instance.pk:
            raise ValidationError("Please enter a password for this user")
        return self.cleaned_data.get('password1')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise ValidationError("Passwords do not match")

        if not password1 and not self.instance.pk:
            raise ValidationError("Please enter a password for this user")

        return password2

    def save(self, commit=True, *args, **kwargs):
        ops_user = super(OperationsUserForm, self).save(commit=False)

        # if not ops_user.username and ops_user.email:
        #     username = ops_user.email.split('@')[0]
        #     i = 1
        #     while OperationsUser.objects.filter(username=username).exists():
        #         username = "{}{}".format(username, i)
        #     ops_user.username = username

        region = self.instance.region

        if self.cleaned_data.get('password1'):
            ops_user.set_password(self.cleaned_data.get('password1'))

        groups = self.cleaned_data.get('groups', [])
        district = self.cleaned_data.get('district', [])
        
        if commit:
            ops_user.save()
            ops_user.groups = groups

        return ops_user        

class OperationsUserFilterForm(forms.Form):

    name = forms.CharField(required = False)
    active = forms.ChoiceField(required = False, choices = (('', "--- Select User Status ---"), ('active', "Active"), ("inactive", "Inactive")))

    def __init__(self, *args, **kwargs):
        super(OperationsUserFilterForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['placeholder'] = 'User, Name,Email, Phon.... '

    def filter(self, users):
        if self.cleaned_data is not None:
            if self.cleaned_data['active']:
                if self.cleaned_data['active'] == 'active':
                    users = users.filter(is_active=True)
                if self.cleaned_data['active'] == 'inactive':
                    users = users.filter(is_active=False)


            if self.cleaned_data['name']:
                users = users.annotate(fullname=Concat('first_name', V(" "), 'last_name'))
                term = self.cleaned_data['name']
                users = users.filter(Q(first_name__icontains=term) |
                                     Q(last_name__icontains=term) |
                                     Q(fullname__icontains=term) |
                                     Q(email__icontains=term) |
                                     Q(phone_number__icontains=term) |
                                     Q(username__icontains=term))
          
            
        return users

class RegionForm(forms.ModelForm):

    class Meta:
        model = Region
        exclude = ['deleted']

class BranchForm(forms.ModelForm):

    class Meta:
        model = Branch
        exclude = ['deleted']

class DocumentFileForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Document
        fields = ['document', 'description']

class PhotoFileForm(forms.ModelForm):
    
    class Meta:
        model = Document
        fields = ['image', 'description']
        
class IncidentFileForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ['document']

class InsuranceClaimFileForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ['document']

class ServiceMaintanceDocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ['document']

class AddressForm(forms.ModelForm):
    
    class Meta:
        model = Address
        exclude = ['deleted', 'address_type']

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'tel_number', 'cell_number', 'email']

class VendorBankDetailForm(forms.ModelForm):

    class Meta:
        model = VendorBankDetail
        fields = ['bank_name', 'branch_code', 'account_holder_name', 'account_number']

class InsurerForm(forms.ModelForm):
    class Meta:
        model = Insurer
        exclude = ['contact_person', 'address', 'created_by', 'modified_by']

    def __init__(self, *args, **kwargs):
        super(InsurerForm, self).__init__(*args, **kwargs)

    def save(self, commit=True, *args, **kwargs):
        insurer = super(InsurerForm, self).save(commit=False)

        if commit:
            insurer.save()

        return insurer


class InsurerFilterForm(forms.Form):
    name = forms.CharField(required = False)

    def __init__(self, *args, **kwargs):
        super(InsurerFilterForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['placeholder'] = 'Search Insurer, Contact, Email, Cell, Tel...'
        
    def filter(self, insurers):
        if self.cleaned_data is not None:
            if self.cleaned_data['name']:
                contacts = Contact.objects.annotate(fullname=Concat('first_name', V(' '), 'last_name')).filter(
                                                    Q(fullname__icontains=self.cleaned_data['name'])|
                                                    Q(first_name__icontains=self.cleaned_data['name'])|
                                                    Q(last_name__icontains=self.cleaned_data['name'])|
                                                    Q(tel_number__icontains=self.cleaned_data['name'])|
                                                    Q(cell_number__icontains=self.cleaned_data['name'])|
                                                    Q(email__icontains=self.cleaned_data['name'])).values_list('id', flat=True)
                                                    
                insurers = insurers.filter(Q(name__icontains=self.cleaned_data['name'])|
                                           Q(contact_person__in=contacts))
        
        return insurers


class DownloadsFilterForm(forms.Form):
    name = forms.CharField(required = False)
    start_date = forms.CharField(required=False, label='Start date')
    end_date = forms.CharField(required=False, label='End date')

    def __init__(self, *args, **kwargs):
        super(DownloadsFilterForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['placeholder'] = 'Search Downloaded By, File Name ,Desc...'
        self.fields['end_date'].widget.attrs['class'] = 'date_field'
        self.fields['start_date'].widget.attrs['class'] = 'date_field'
        self.fields['start_date'].widget.attrs['placeholder'] = 'Start Date'
        self.fields['end_date'].widget.attrs['placeholder'] = 'End Date'
        
    def filter(self, downloads):
        if self.cleaned_data is not None:
            if self.cleaned_data['name']:
                users = OperationsUser.objects.filter(username__icontains=self.cleaned_data['name']).values_list('id', flat=True)
                                                                    
                downloads = downloads.filter(Q(description__icontains=self.cleaned_data['name'])|
                                             Q(document_name__icontains=self.cleaned_data['name'])|
                                             Q(created_by__in=users))

            if self.cleaned_data['start_date']:
                    downloads = downloads.filter(created_at__gte=self.cleaned_data['start_date'])

            if self.cleaned_data['end_date']:
                    downloads = downloads.filter(created_at__lte=self.cleaned_data['end_date'])
        
        return downloads


class TicketFilterForm(forms.Form):
    name = forms.CharField(required = False)
    status = forms.ChoiceField(choices=[('', '--- Select Status ---'), ('', 'All')]+list(BaseTicket.TICKET_STATUS), 
                                       label='Status', required=False)
    category = forms.ChoiceField(choices=[('', '--- Select Category ---'), ('', 'All')]+list(BaseTicket.CATEGORIES), 
                                       label='Status', required=False)
    start_date = forms.CharField(required=False, label='Start date')
    end_date = forms.CharField(required=False, label='End date')

    def __init__(self, *args, **kwargs):
        super(TicketFilterForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['placeholder'] = 'Search Ticket, Created by ...'
        # self.fields['search'].widget.attrs['placeholder'] = 'Search Ticket, Employee, Technician ...'
        self.fields['end_date'].widget.attrs['class'] = 'date_field'
        self.fields['start_date'].widget.attrs['class'] = 'date_field'
        self.fields['start_date'].widget.attrs['placeholder'] = 'Start Date'
        self.fields['end_date'].widget.attrs['placeholder'] = 'End Date'
        
    def filter(self, tickets):
        if self.cleaned_data is not None:
            if self.cleaned_data['name']:
                users = OperationsUser.objects.filter(username__icontains=self.cleaned_data['name']).values_list('id', flat=True)

                tickets = tickets.filter(Q(number__icontains=self.cleaned_data['name'])|
                                         Q(created_by__in=users))

            if self.cleaned_data['status']:
                    tickets = tickets.filter(status=self.cleaned_data['status'])

            if self.cleaned_data['category']:
                    tickets = tickets.filter(category=self.cleaned_data['category'])

            if self.cleaned_data['start_date']:
                    tickets = tickets.filter(created_at__gte=self.cleaned_data['start_date'])

            if self.cleaned_data['end_date']:
                    tickets = tickets.filter(created_at__lte=self.cleaned_data['end_date'])
        
        return tickets

class ServiceProviderForm(forms.ModelForm):
    class Meta:
        model = ServiceProvider
        exclude = ['contact_person', 'address', 'created_by', 'modified_by']

    def __init__(self, *args, **kwargs):
        super(ServiceProviderForm, self).__init__(*args, **kwargs)

    def save(self, commit=True, *args, **kwargs):
        service_provider = super(ServiceProviderForm, self).save(commit=False)

        if commit:
            service_provider.save()

        return service_provider


class ServiceProviderFilterForm(forms.Form):
    name = forms.CharField(required = False)

    def __init__(self, *args, **kwargs):
        super(ServiceProviderFilterForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['placeholder'] = 'Search Service Provider, Contact, Email, Cell, Tel...'
        
    def filter(self, service_providers):
        if self.cleaned_data is not None:
            if self.cleaned_data['name']:
                contacts = Contact.objects.annotate(fullname=Concat('first_name', V(' '), 'last_name')).filter(
                                                    Q(fullname__icontains=self.cleaned_data['name'])|
                                                    Q(first_name__icontains=self.cleaned_data['name'])|
                                                    Q(last_name__icontains=self.cleaned_data['name'])|
                                                    Q(tel_number__icontains=self.cleaned_data['name'])|
                                                    Q(cell_number__icontains=self.cleaned_data['name'])|
                                                    Q(email__icontains=self.cleaned_data['name'])).values_list('id', flat=True)
                                                    
                service_providers = service_providers.filter(Q(name__icontains=self.cleaned_data['name'])|
                                           Q(contact_person__in=contacts))
        
        return service_providers

class VendorForm(forms.ModelForm):
    name = forms.CharField(required = True, label="Service Provider")
    vendor_type = forms.ChoiceField(choices=[('', '--- Select Type ---'), ('', 'All')]+list(Vendor.TYPE_LIST), 
                                    required=True, label="Service Provider Type")
    account_type = forms.ChoiceField(choices=[('', '--- Select Account Type ---')]+list(Vendor.ACCOUNT_TYPE), required=False,
                                    label="Account Type")

    class Meta:
        model = Vendor
        exclude = ['contact_person', 'address', 'created_by', 'modified_by']

    def __init__(self, *args, **kwargs):
        super(VendorForm, self).__init__(*args, **kwargs)

    def save(self, commit=True, *args, **kwargs):
        vendor = super(VendorForm, self).save(commit=False)

        if commit:
            vendor.save()

        return vendor

    def clean_balance(self):
        account_type = self.cleaned_data['account_type']
        balance = self.cleaned_data['balance']
        if account_type=='debit'and not balance:
            raise forms.ValidationError('This field is required if account type is debit')
        if account_type=='credit' and not balance:
            raise forms.ValidationError('This field is required if account type is credit')

        return balance


class VendorFilterForm(forms.Form):

    name = forms.CharField(required = False)
    vendor_type = forms.ChoiceField(choices=[('', '--- Select Type ---'), ('', 'All')]+list(Vendor.TYPE_LIST), 
                                       required=False)
    account_type = forms.ChoiceField(choices=[('', '--- Select Type ---'), ('', 'All')]+list(Vendor.ACCOUNT_TYPE), 
                                       required=False)

    def __init__(self, *args, **kwargs):
        super(VendorFilterForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['placeholder'] = 'Search Service Provider, Contact, Email, Cell, Tel...'
        
    def filter(self, vendors):
        if self.cleaned_data is not None:

            if self.cleaned_data['vendor_type']:
                    vendors = vendors.filter(vendor_type=self.cleaned_data['vendor_type'])

            if self.cleaned_data['account_type']:
                    vendors = vendors.filter(account_type=self.cleaned_data['account_type'])
                    
            if self.cleaned_data['name']:
                contacts = Contact.objects.annotate(fullname=Concat('first_name', V(' '), 'last_name')).filter(
                                                    Q(fullname__icontains=self.cleaned_data['name'])|
                                                    Q(first_name__icontains=self.cleaned_data['name'])|
                                                    Q(last_name__icontains=self.cleaned_data['name'])|
                                                    Q(tel_number__icontains=self.cleaned_data['name'])|
                                                    Q(cell_number__icontains=self.cleaned_data['name'])|
                                                    Q(email__icontains=self.cleaned_data['name'])).values_list('id', flat=True)
                                                    
                vendors = vendors.filter(Q(name__icontains=self.cleaned_data['name'])|
                                         Q(contact_person__in=contacts))
        
        return vendors

class TicketForm(forms.ModelForm):

    # technician = forms.ModelChoiceField(queryset=OperationsUser.objects.all(), required=False, empty_label="--- Select Technician ---")

    # technician = forms.ModelChoiceField(queryset=OperationsUser.objects.all().order_by('username'), 
    #                                  label='Technician',
    #                                  widget=autocomplete.ListSelect2(url='fleetmanagement:technician-autocomplete',
    #                                                                  attrs={'data-placeholder': '--- Select Technician ---'}))
    
    category = forms.ChoiceField([('', '--- Select Category ---')]+list(BaseTicket.CATEGORIES))

    class Meta:
        model = BaseTicket
        exclude = ['created_by', 'deleted', 'technician', 'is_closed', 'possible_fix', 'number', 'employee', 'status']

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)

    def save(self, commit=True, *args, **kwargs):
        ticket = super(TicketForm, self).save(commit=False)

        if commit:
            ticket.save()

        return ticket

class ServiceProviderImportForm(forms.Form):
    service_provider_file = forms.FileField(required=True, label="Service Provider File")

class DistrictImportForm(forms.Form):
    district_file = forms.FileField(required=True, label="District File")

class EditUserForm(forms.ModelForm):

    password1 = forms.CharField(
        required=False, label="Password (leave empty if not changed)", widget=forms.PasswordInput)
    password2 = forms.CharField(
        required=False, label="Re-enter password", widget=forms.PasswordInput)
            
    class Meta:
        model = OperationsUser
        fields = ['first_name','last_name','username','email','phone_number']       
        widgets = {'groups': forms.CheckboxSelectMultiple()}

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        
    def clean_password1(self):
        if not self.cleaned_data.get('password1') and not self.instance.pk:
            raise ValidationError("Please enter a password for this user")
        return self.cleaned_data.get('password1')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise ValidationError("Passwords do not match")

        if not password1 and not self.instance.pk:
            raise ValidationError("Please enter a password for this user")

        return password2

    def save(self, commit=True, *args, **kwargs):
        ops_user = super(EditUserForm, self).save(commit=False)

        if self.cleaned_data.get('password1'):
            ops_user.set_password(self.cleaned_data.get('password1'))
        
        if commit:
            ops_user.save()

        return ops_user 
