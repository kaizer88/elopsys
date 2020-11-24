from django.conf import settings
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.db.models import Q
from django.db.models.functions import Concat
from django.db.models import Value as V

from models import Employee, DrivingLicence
from operations.models import Document
from fleet_management.models import VehicleDriver, Vehicle
from datetime import datetime

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
	fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)

    def save(self, user, commit=True, *args, **kwargs):
        employee = super(EmployeeForm, self).save(commit=False)
        employee.change_at = datetime.now()
        employee.modified_by = user
        employee.created_by = user
        if commit:
            employee.save()

        return employee

class EmployeeFilterForm(forms.Form):

    name = forms.CharField(required = False, label = 'Employee Search')
    assigned = forms.ChoiceField(required = False, label = 'Vehicle Assigned', choices = (('', "--- Select Vehicle Assignment ---"), 
                                                                                          ('', "All Drivers"), 
                                                                                          ('assigned', "Assigned Drivers"),
                                                                                          ("unassigned", "Unassigned Drivers")))
    division = forms.ChoiceField(required = False, label = 'Division', choices = [('', '--- Select Division ---')] + list(Vehicle.DIVISION_TYPES))

    def __init__(self, *args, **kwargs):
        super(EmployeeFilterForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = "Search Name, Email, ID..."
        self.initial['assigned'] = "unassigned"

    def filter(self, employees=None):
        if self.cleaned_data is not None:
            if employees is None:
                employees = Employee.objects.all()

            if self.cleaned_data['assigned']:
                search = self.cleaned_data['assigned']
                                
                if search == 'assigned':
                    employees = Employee.objects.filter(driver_vehicle__start_date__isnull=False,
                                                        driver_vehicle__end_date__isnull=True)
                if search == 'unassigned':
                    employees = Employee.objects.exclude(driver_vehicle__start_date__isnull=False,
                                                         driver_vehicle__end_date__isnull=True)
                                    
            if self.cleaned_data['division']:
                if not self.cleaned_data['division'] == "all":
                    employees = employees.filter(driver_vehicle__vehicle__division=self.cleaned_data['division']) 

            if self.cleaned_data['name']:
                employees = employees.annotate(fullname=Concat('first_name',
                                                               V(" "), 'last_name'))
                term = self.cleaned_data['name']
                employees = employees.filter(Q(first_name__icontains=term) |
                                                 Q(last_name__icontains=term) |
                                                 Q(fullname__icontains=term) |
                                                 Q(email__icontains=term) |
                                                 Q(id_number__icontains=term) |
                                                 Q(employee_no__icontains=term))


                        
        return employees.distinct()
                    
class DrivingLicenceForm(forms.ModelForm):


    licence_image = forms.ImageField()
    
    class Meta:
        model = DrivingLicence
	fields = ['code','licence_number','expiry_date']

    def __init__(self, *args, **kwargs):
        super(DrivingLicenceForm, self).__init__(*args, **kwargs)
        self.fields['expiry_date'].widget.attrs['class'] = 'date_field'
        
    def save(self, commit=True, *args, **kwargs):
        licence = super(DrivingLicenceForm, self).save(commit=False)

        licence_image = self.cleaned_data.get('licence_image', None)
        if licence_image:
            document = Document.objects.create(document_name=licence_image._name,
                                    image=licence_image,
                                    file_type='photo',
                                    description='Employee Driver Licence')
            licence.licence_image = document
            
        if commit:
            licence.save()

        return licence

class DrivingLicenceFilterForm(forms.Form):

    employee = forms.CharField(required = False, label='Driver') 
    licence_number = forms.CharField(required = False)   
    start_date = forms.CharField(required=False, label='Start date')
    end_date = forms.CharField(required=False, label='End date') 
    code = forms.ChoiceField(choices=[('', '--- Select Code ---'), ('', 'All')]+list(DrivingLicence.LICENCE_CODE), 
                                       label='Code', required=False)

    def __init__(self, *args, **kwargs):
        super(DrivingLicenceFilterForm, self).__init__(*args, **kwargs)

        self.fields['end_date'].widget.attrs['class'] = 'date_field'
        self.fields['start_date'].widget.attrs['class'] = 'date_field'
        self.fields['licence_number'].widget.attrs['placeholder'] = 'Licence Number'
        self.fields['start_date'].widget.attrs['placeholder'] = 'Drivers Licence Expiry Start Date'
        self.fields['end_date'].widget.attrs['placeholder'] = 'Drivers Licence Expiry Expiry End Date'
        self.fields['end_date'].widget.attrs['Title']="Search"
        
    def filter(self, driving_licences):
        if self.cleaned_data is not None:

            if self.cleaned_data['employee']:
                    drivers = Employee.objects.annotate(driver_full_name=Concat('first_name', V(' '), 'last_name')).filter(
                                                                Q(driver_full_name__icontains=self.cleaned_data['employee'])|
                                                                Q(first_name__icontains=self.cleaned_data['employee'])|
                                                                Q(last_name__icontains=self.cleaned_data['employee']))
                    
                    driving_licences = driving_licences.filter(Q(employee__in=drivers)|
                                             Q(licence_number__icontains=self.cleaned_data['employee'])
                                            )

            if self.cleaned_data['licence_number']:
                    driving_licences = driving_licences.filter(licence_number__icontains=self.cleaned_data['licence_number'])

            if self.cleaned_data['code']:
                    driving_licences = driving_licences.filter(code=self.cleaned_data['code'])

            if self.cleaned_data['start_date']:
                    driving_licences = driving_licences.filter(expiry_date__gte = self.cleaned_data['start_date'])

            if self.cleaned_data['end_date']:
                    driving_licences = driving_licences.filter(expiry_date__lte = self.cleaned_data['end_date'])
        
        return driving_licences
