import os

from django.conf import settings
from django import forms
from django.db.models import Q
from datetime import datetime, timedelta
from django.db.models.functions import Concat
from django.db.models import Value as V
from django.forms.widgets import *
from models import *
from employees.models import Employee
from rest_framework import fields, serializers
from django.core.urlresolvers import reverse
from operations.models import *
from dal import autocomplete, forward
from django.forms.widgets import RadioSelect
from django.utils.translation import ugettext_lazy

class VehicleMakeForm(forms.ModelForm):

    class Meta:
        model = VehicleMake
        fields = ['make_name',]

    def __init__(self, *args, **kwargs):
        super(VehicleMakeForm, self).__init__(*args, **kwargs)

class VehicleMakeFilterForm(forms.Form):

    name = forms.CharField(required = False)

    def __init__(self, *args, **kwargs):
        super(VehicleMakeFilterForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['placeholder'] = 'Search Vehicle Make'

    def filter(self, vehicle_makes):
        if self.cleaned_data is not None:

            if self.cleaned_data['name']:

                vehicle_makes = vehicle_makes.filter(make_name__icontains=self.cleaned_data['name'])

        return vehicle_makes


class VehicleModelForm(forms.ModelForm):

    class Meta:
        model = VehicleModel
        fields = ['make','model_name',]

    def __init__(self, *args, **kwargs):
        super(VehicleModelForm, self).__init__(*args, **kwargs)

class VehicleModelFilterForm(forms.Form):

    name = forms.CharField(required = False)

    def __init__(self, *args, **kwargs):
        super(VehicleModelFilterForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['placeholder'] = 'Search Vehicle Make, Model...'

    def filter(self, vehicle_models):
        if self.cleaned_data is not None:

            if self.cleaned_data['name']:

                vehicle_models = vehicle_models.filter(Q(model_name__icontains=self.cleaned_data['name'])|
                                                       Q(make__make_name__icontains=self.cleaned_data['name']))

        return vehicle_models


class NullBooleanRadioSelect(RadioSelect):
    def __init__(self, *args, **kwargs):
        choices = (
            (None, ugettext_lazy('Unknown')),
            (True, ugettext_lazy('Yes')),
            (False, ugettext_lazy('No'))
        )
        super(NullBooleanRadioSelect, self).__init__(choices=choices, *args, **kwargs)

    _empty_value = None

class VehicleForm(forms.ModelForm):

    registration_number = forms.CharField(required=False, label='Registration Number')
    ownership = forms.ChoiceField(choices=[('', '--- Select Ownership ---')]+list(Vehicle.OWNERSHIP_TYPES), required=False)
    division = forms.ChoiceField(choices=[('', '--- Select Division ---')]+list(Vehicle.DIVISION_TYPES), required=False)
    transmission = forms.ChoiceField(choices=[('', '--- Select Transmission ---')]+list(Vehicle.TRANSMISSION_TYPES), required=False)
    fuel_type = forms.ChoiceField(choices=[('', '--- Select Fuel Type ---')]+list(Vehicle.FUEL_TYPES),label='Fuel Type', required=False)
    status_at_create = forms.ChoiceField(choices=[('', '--- Select Status At Create ---')]+list(Vehicle.STATUS_AT_CREATE_TYPES),
                                         label='Status At Create', required=False)
    vin_number = forms.CharField(required=False, label='VIN Number')
    fleet_administator = forms.CharField(required=False, label='Fleet Administrator')

    class Meta:
        model = Vehicle
        exclude = ['deleted', 'created_by', 'modified_by', 'make', 'model']
        widgets = {'has_aircon': NullBooleanRadioSelect(),
                   'has_radio': NullBooleanRadioSelect(),
                   'has_bluetooth': NullBooleanRadioSelect(),
                   'has_spanner': NullBooleanRadioSelect(),
                   'has_triangle': NullBooleanRadioSelect(),
                   'has_jack': NullBooleanRadioSelect(),
                   'rental_reason': forms.Textarea(attrs={'rows':4, 'cols':15})}

    def __init__(self, *args, **kwargs):
        fleet_admin = kwargs.pop('fleet_admin', None)
        super(VehicleForm, self).__init__(*args, **kwargs)
        self.initial['fleet_administator'] = fleet_admin

        for f in self.fields:
            self.fields[f].widget.attrs['required'] = 'false'
        self.fields['rental_reason'].widget.attrs['rows'] = 5
        self.fields['registration_date'].widget.attrs['class'] = 'date_field'
        self.fields['licence_disk_expiry'].widget.attrs['class'] = 'date_field'
        self.fields['registration_number'].widget.attrs['placeholder'] = 'Registration Number'
        self.fields['ownership'].widget.attrs['onchange'] = 'ownership_selection();'
        self.fields['delivery_date'].widget.attrs['class'] = 'date_time_field'
        self.fields['returned_date'].widget.attrs['class'] = 'date_time_field'
        self.fields['deposit_paid_by'].widget.attrs['onchange'] = 'paidby_selection();'
        self.fields['deposit_paid_date'].widget.attrs['class'] = 'date_field'
        self.fields['updated_date'].widget.attrs['class'] = 'date_field'
        self.fields['fleet_administator'].widget.attrs['readonly'] = True

    def save(self, user, commit=True, *args, **kwargs):
        vehicle = super(VehicleForm, self).save(commit=False)
        vehicle.changed_at = datetime.now()
        vehicle.modified_by = user
        vehicle.created_by = user
        if commit:
            vehicle.save()

        return vehicle

    def clean_vehicle_model(self):
        model = self.cleaned_data['vehicle_model']
        make = self.cleaned_data['vehicle_make']
        if model and make and model.make!=make:
            raise forms.ValidationError('Selected Model does not belong to the Selected Make')

        return model

    def clean_vin_number(self):
        vin = self.cleaned_data['vin_number']
        make = self.cleaned_data['vehicle_make']
        if vin and make:
            if make.id in [1,2] and len(vin)!=17:
                raise forms.ValidationError('VIN Number must have 17 charactors')

        return vin

    def clean(self):
        cleaned_data = super(VehicleForm, self).clean()
        ownership = cleaned_data.get('ownership', None)
        make      = cleaned_data.get('vehicle_make', None)
        model     = cleaned_data.get('vehicle_model', None)
        vin       = cleaned_data.get('vin_number', None)
        engine_num = cleaned_data.get('engine_number', None)
        registration = cleaned_data.get('registration_number', None)
        transmission = cleaned_data.get('transmission', None)
        fuel_type = cleaned_data.get('fuel_type', None)
        rental_company = cleaned_data.get('rental_company', None)
        rental_contact_person = cleaned_data.get('rental_contact_person', None)
        returned_location = cleaned_data.get('returned_location', None)
        vehicle_class = cleaned_data.get('vehicle_class', None)
        rental_reason = cleaned_data.get('rental_reason', None)
        delivery_odometer_mileage = cleaned_data.get('delivery_odometer_mileage', None)
        returned_mileage = cleaned_data.get('returned_mileage', None)
        delivery_date = cleaned_data.get('delivery_date', None)
        returned_date = cleaned_data.get('returned_date', None)
        deposit_paid  = cleaned_data.get('deposit_paid_by', None)
        depositdriver = cleaned_data.get('deposit_driver', None)

        if ownership is None or ownership == '':
            self._errors['ownership'] = ['Please select a valid Ownership Type']
        else:
            if cleaned_data.get('division', None) is None or cleaned_data.get('division', None) == '':
                self._errors['division'] = ['This field is required']
            if ownership == 'emerald' or ownership == 'private':
                if vin is None or vin == '':
                    self._errors['vin_number'] = ['This field is required']
                if engine_num is None or engine_num == '':
                    self._errors['engine_number'] = ['This field is required']
                if make is None or make == '':
                    self._errors['vehicle_make'] = ['This field is required']
                if model is None or model == '':
                    self._errors['vehicle_model'] = ['This field is required']
                if registration is None or registration == '':
                    self._errors['registration_number'] = ['This field is required']
                if transmission is None or transmission == '':
                    self._errors['transmission'] = ['This field is required']
                if fuel_type is None or fuel_type == '':
                    self._errors['fuel_type'] = ['This field is required']
            else:
                if delivery_odometer_mileage is None or delivery_odometer_mileage == '':
                    delivery_odometer_mileage = 0

                if returned_date is not None and returned_date <> '':
                    if returned_mileage is None or returned_mileage == '' or returned_mileage == 0:
                        returned_mileage = 0
                        self._errors['returned_mileage'] = ['This field is required']
                    else:
                        if int(returned_mileage) < int(delivery_odometer_mileage):
                            self._errors['returned_mileage'] = ['Returned mileage not allowed to be less than delivery mileage']
                if returned_mileage is not None and returned_mileage <> ''  and returned_mileage <> 0:
                    if returned_date is None or returned_date == '':
                        self._errors['returned_date'] = ['This field is required']
                    else:
                        if returned_date.date() < delivery_date.date():
                            self._errors['delivery_date'] = ['Returned date not allowed to be earlier than delivery date']
                if deposit_paid is None or deposit_paid == '':
                    deposit_paid = ''
                else:
                    if deposit_paid == 'driver':
                        if depositdriver is None or depositdriver == '':
                            self._errors['deposit_driver'] = ['Valid driver must be selected']

        return cleaned_data

class VehicleTyreForm(forms.ModelForm):

    class Meta:
        model = VehicleTyre
        fields = ['make', 'size', 'serial_number', 'mileage_at_replacement', 'position']

    def __init__(self, *args, **kwargs):
        super(VehicleTyreForm, self).__init__(*args, **kwargs)
        self.fields['position'].widget = forms.HiddenInput()

    def save(self, commit=True, *args, **kwargs):
        vehicle_tyre = super(VehicleTyreForm, self).save(commit=False)
        vehicle_tyre.changed_at = datetime.now()

        if commit:
            vehicle_tyre.save()

        return vehicle_tyre

VehicleTyreFormset = forms.modelformset_factory(VehicleTyre, form=VehicleTyreForm, extra=5, max_num=5)


class PurchaseDetailForm(forms.ModelForm):

    purchase_type = forms.ChoiceField(choices=[('', '--- Select Purchase Type ---')]+list(PurchaseDetail.PURCHASE_TYPES),
                                      label='Purchase Type', required=False)

    vendor = forms.ModelChoiceField(queryset=Vendor.objects.filter(vendor_type='dealer'),
                                     label='Dealer',
                                     widget=autocomplete.ListSelect2(url='fleetmanagement:vendor_purchase_detail-autocomplete',
                                                                     attrs={'data-placeholder': '--- Select Dealer Name ---'}))
    class Meta:
        model = PurchaseDetail
        exclude = ['deleted', 'created_by', 'modified_by', 'vehicle']

    def __init__(self, *args, **kwargs):
        super(PurchaseDetailForm, self).__init__(*args, **kwargs)

        self.fields['purchase_date'].widget.attrs['class'] = 'date_field'

    def save(self, commit=True, *args, **kwargs):
        purchase_detail = super(PurchaseDetailForm, self).save(commit=False)

        if commit:
            purchase_detail.save()

        return purchase_detail


class FinanceDetailForm(forms.ModelForm):

    class Meta:
        model = FinanceDetail
        exclude = ['purchase_detail', 'deleted', 'created_by', 'modified_by', 'contract_number', 'contract_term_months',
                   'deposit', 'installment', 'settlement_amount', 'settlement_amount_date']

    def __init__(self, *args, **kwargs):
        super(FinanceDetailForm, self).__init__(*args, **kwargs)

    def save(self, commit=True, *args, **kwargs):
        finance_detail = super(FinanceDetailForm, self).save(commit=False)

        if commit:
            finance_detail.save()

        return finance_detail


class InsuranceForm(forms.ModelForm):

    vendor = forms.ModelChoiceField(queryset=Vendor.objects.filter(vendor_type='insurance'), required=False, empty_label="--- Select Insurer ---", label='Insurer')
    insurance_type = forms.ChoiceField(choices=[('', '--- Select Insurance Type ---')]+list(Insurance.COVER_TYPES),
                                       label='Insurance Type', required=False)

    class Meta:
        model = Insurance
        exclude = ['deleted', 'created_by', 'modified_by', 'vehicle',
                   'broker_contact_person','broker_address',
                   'insurer_address','insurer_contact_person']

    def __init__(self, *args, **kwargs):
        super(InsuranceForm, self).__init__(*args, **kwargs)

    def save(self, commit=True, *args, **kwargs):
        insurance = super(InsuranceForm, self).save(commit=False)
        if commit:
            insurance.save()

        return insurance

class InsuredVehiclesFilterForm(forms.Form):

    driver = forms.ModelChoiceField(queryset=Employee.objects.all(), required=False, empty_label="--- Select Driver ---")
    vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.all(), required=False, empty_label="--- Select Vehicle ---")
    insurance_type = forms.ChoiceField(choices=[('', '--- Select Insurance Type ---')]+list(Insurance.COVER_TYPES),
                                       label='Insurance Type', required=False)
    broker_name = forms.CharField(required = False)

    def __init__(self, *args, **kwargs):
        super(InsuredVehiclesFilterForm, self).__init__(*args, **kwargs)
        self.fields['vehicle'].widget.attrs['class'] = 'auto_complete_dropdown'

    def filter(self, insured_vehicles):
        if self.cleaned_data is not None:
            if self.cleaned_data['vehicle']:
                insured_vehicles = insured_vehicles.filter(vehicle=self.cleaned_data['vehicle'])
            if self.cleaned_data['broker_name']:
                insured_vehicles = insured_vehicles.filter(broker_name__icontains=self.cleaned_data['broker_name'])
            if self.cleaned_data['insurance_type']:
                insured_vehicles = insured_vehicles.filter(insurance_type=self.cleaned_data['insurance_type'])

        return insured_vehicles


class VehicleMaintenanceForm(forms.ModelForm):


    class Meta:
        model = VehicleMaintenance
        exclude = ['deleted', 'created_by', 'modified_by', 'vehicle']

    def __init__(self, *args, **kwargs):
        super(VehicleMaintenanceForm, self).__init__(*args, **kwargs)
        self.fields['end_date'].widget.attrs['class'] = 'date_field'

    def save(self, commit=True, *args, **kwargs):
        vehicle_maintenance = super(VehicleMaintenanceForm, self).save(commit=False)

        if commit:
            vehicle_maintenance.save()

        return vehicle_maintenance

class AddVehicleMaintenanceForm(forms.ModelForm):

    vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.all().order_by('registration_number'),
                                     label='Registration Number',
                                     widget=autocomplete.ListSelect2(url='fleetmanagement:vehicle-autocomplete',
                                                                     attrs={'data-placeholder': '--- Select Registration Number ---'}))

    class Meta:
        model = VehicleMaintenance
        exclude = ['deleted', 'created_by', 'modified_by']

    def __init__(self, *args, **kwargs):
        super(AddVehicleMaintenanceForm, self).__init__(*args, **kwargs)
        self.fields['end_date'].widget.attrs['class'] = 'date_field'

    def save(self, commit=True, *args, **kwargs):
        vehicle_maintenance = super(AddVehicleMaintenanceForm, self).save(commit=False)

        if commit:
            vehicle_maintenance.save()

        return vehicle_maintenance

class FuelCardUsageForm(forms.ModelForm):

    driver = forms.ModelChoiceField(queryset=Employee.objects.all().order_by('first_name','last_name'),
                                    required=False,
                                    widget=autocomplete.ModelSelect2(url='fleetmanagement:driver-autocomplete',
                                                                    attrs={'data-placeholder': '--- Select Driver ---'}))

    vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.all().order_by('registration_number'),
                                     label='Registration Number',
                                     required=False,
                                     widget=autocomplete.ModelSelect2(url='fleetmanagement:vehicle-autocomplete',
                                                                     attrs={'data-placeholder': '--- Select Registration Number ---'}))

    class Meta:
        model = FuelCardUsage
        exclude = ['deleted', 'created_by', 'modified_by', 'fuel_card']

    def __init__(self, *args, **kwargs):
        super(FuelCardUsageForm, self).__init__(*args, **kwargs)
        self.fields['transaction_date'].widget.attrs['class'] = 'date_time_field'
        self.fields['fuel_card'].widget.attrs['class'] = 'select2'

        if self.instance.pk:
            fc = FuelCard.objects.filter(id=self.instance.fuel_card_id)
            self.initial['fuel_card'] = self.instance.fuel_card_id
            self.fields['fuel_card'].widget.attrs['readonly'] = True
            self.fields['fuel_card'].widget.attrs['disabled'] = True
            self.fields['vehicle'].widget.attrs['readonly'] = True
            self.fields['vehicle'].widget.attrs['disabled'] = True

    def save(self, commit=True, *args, **kwargs):
        fuel_card_usage = super(FuelCardUsageForm, self).save(commit=False)
        if commit:
            fuel_card_usage.save()

        return fuel_card_usage

class EditFuelCardUsageForm(forms.ModelForm):

    driver = forms.ModelChoiceField(queryset=Employee.objects.all().order_by('first_name','last_name'),
                                    required=False,
                                    widget=autocomplete.ListSelect2(url='fleetmanagement:driver-autocomplete',
                                                                    attrs={'data-placeholder': '--- Select Driver ---'}))

    vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.all().order_by('registration_number'),
                                     label='Registration Number',
                                     widget=autocomplete.ListSelect2(url='fleetmanagement:vehicle-autocomplete',
                                                                     attrs={'data-placeholder': '--- Select Registration Number ---'}))
    transaction_date = forms.DateTimeField(required=True, label="Transaction Date")
    quantity  = forms.DecimalField(required=False, max_digits=10, decimal_places=2)
    class Meta:
        model = FuelCardUsage
        exclude = ['deleted', 'created_by', 'modified_by', 'fuel_card', 'usage_type']
        widgets = {'comment':forms.Textarea(attrs={'rows':4, 'cols':15})}

    def __init__(self, *args, **kwargs):
        super(EditFuelCardUsageForm, self).__init__(*args, **kwargs)
        self.fields['transaction_date'].widget.attrs['class'] = 'date_time_field'
        self.fields['vehicle'].widget.attrs['class'] = 'auto_select'
        self.fields['comment'].widget.attrs['rows'] = 5
        self.fields['transaction_type'].widget = SelectMultiple()
        self.fields['transaction_type'].widget.attrs['class'] = 'multi_select'
        self.fields['transaction_type'].queryset = FuelCardUsageTransactionType.objects.filter(description__in=['FUEL', 'OIL', 'TOLL-GATE'])




    def save(self, commit=True, *args, **kwargs):
        fuel_card_usage = super(EditFuelCardUsageForm, self).save(commit=False)
        if commit:
            fuel_card_usage.save()

        return fuel_card_usage

class FuelCardUsageDocumentForm(forms.ModelForm):

    class Meta:
        model = FuelCardUsageDocument
        fields = ['document_type']

    def __init__(self, *args, **kwargs):
        super(FuelCardUsageDocumentForm, self).__init__(*args, **kwargs)
        self.fields['document_type'].widget = SelectMultiple()
        self.fields['document_type'].widget.attrs['class'] = 'multi_select'
        self.fields['document_type'].queryset = FuelCardUsageDocumentUploads.objects.all().exclude(description='Card Limit Change')


class FuelCardUsageFileForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ['document']

class FuelCardDocumentForm(forms.ModelForm):

    class Meta:
        model = FuelCardDocument
        fields = ['document_type']

    def __init__(self, *args, **kwargs):
        super(FuelCardDocumentForm, self).__init__(*args, **kwargs)
        self.fields['document_type'].widget = SelectMultiple()
        self.fields['document_type'].widget.attrs['class'] = 'multi_select'
        self.fields['document_type'].queryset = FuelCardDocumentUploads.objects.all()


class FuelCardFileForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ['document']

class TrackerForm(forms.ModelForm):

    SOURCE_TYPES = (('tracker','Tracker'),
                    ('geotab','Geotab'),
                    ('none','None')
        )
    tracking_source = forms.ChoiceField(required=True, choices=SOURCE_TYPES)
    installation_type = forms.ChoiceField([('', '--- Select Installation Type ---')]+list(Tracker.INSTALLATION_TYPES), label='Installation Type',required=False)
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.filter(vendor_type='tracker'),required=False,
                                     label='Dealer',
                                     widget=autocomplete.ListSelect2(url='fleetmanagement:vendor_tracker-autocomplete',
                                                                     attrs={'data-placeholder': '--- Select Dealer Name ---'}))

    class Meta:
        model = Tracker
        exclude = ['deleted', 'vehicle', 'address', 'contact_person', 'active']

    def __init__(self, *args, **kwargs):
        super(TrackerForm, self).__init__(*args, **kwargs)
        self.fields['installation_date'].widget.attrs['class'] = 'date_field'
        self.fields['settlement_amount_date'].widget.attrs['class'] = 'date_field'

    def save(self, commit=True, *args, **kwargs):
        tracker = super(TrackerForm, self).save(commit=False)

        if commit:
            tracker.save()

        return tracker

class BrandingForm(forms.ModelForm):

    supplier = forms.ModelChoiceField(queryset=Vendor.objects.filter(vendor_type='branding'), required=False, empty_label="--- Select Supplier ---", label='Supplier')
    installer = forms.ModelChoiceField(queryset=Vendor.objects.filter(vendor_type='installer'), required=False, empty_label="--- Select Installer ---", label='Installer')

    class Meta:
        model = Branding
        exclude = ['deleted', 'created_by', 'modified_by', 'vehicle', 'supplier_address',
                   'supplier_contact_person', 'installer_address',
                   'installer_contact_person']

    def __init__(self, *args, **kwargs):
        super(BrandingForm, self).__init__(*args, **kwargs)
        self.fields['installation_date'].widget.attrs['class'] = 'date_field'

    def save(self, commit=True, *args, **kwargs):
        branding = super(BrandingForm, self).save(commit=False)

        if commit:
            branding.save()
        return branding

class VehicleDocumentForm(forms.ModelForm):

    document_type = forms.ChoiceField([('', '--- Select Document Type ---')]+list(VehicleDocument.DOCUMENT_TYPES), label='Document Type')

    class Meta:
        model = VehicleDocument
        exclude = ['deleted', 'created_by', 'modified_by']
        widgets = {
          'description': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }

    def __init__(self, *args, **kwargs):
        super(VehicleDocumentForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['rows'] = 5


    def save(self, user, commit=True, *args, **kwargs):
        vehicle_document = super(VehicleDocumentForm, self).save(commit=False)

        if commit:
            vehicle_document.save()

class VehicleDriverForm(forms.ModelForm):

    UNASSIGN_REASONS = (('none','None'),
                        ('adsconded', 'Absconded'),
                        ('discretionary change','Discretionary Vehicle Change'),
                        ('dismissed','Dismissal'),
                        ('long term repair','Long-term Maintenance/Repairs'),
                        ('relocation','Relocation'),
                        ('resignation','Resignation'),
                        ('suspend','Suspension'),
                        ('temp vehicle','Temp Vehicle'),
                        ('insurance pending','Insurance Claim - Pending'),
                        ('insurance repairs','Insurance Claim - Repairs'),
                        ('writeoff','Write-off'))
    
    driver = forms.ModelChoiceField(queryset=Employee.objects.all().order_by('first_name','last_name'),
                                    widget=autocomplete.ListSelect2(url='fleetmanagement:driver-autocomplete',
                                                                    attrs={'data-placeholder': '--- Select Driver ---'}))

    reason = forms.ChoiceField(required = True,
                               choices = [('', '--- Select Reason ---')] + list(VehicleDriver.REASONS))
#    unassign_reason = forms.ChoiceField(required = False, choices=UNASSIGN_REASONS)

    class Meta:
        model = VehicleDriver
        exclude = ['deleted', 'created_by', 'modified_by', 'vehicle', 'status', 'end_date','unassign_reason']

    def __init__(self, *args, **kwargs):
        self.car = kwargs.pop('car')
        self.driver = kwargs.pop('driver')
        super(VehicleDriverForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs['class'] = 'date_time_field'
#        self.fields['end_date'].widget.attrs['class'] = 'date_time_field'
        
        self.initial['driver'] = self.car.driver
#        if self.initial['driver']:
#            self.fields['start_date'].widget = forms.HiddenInput()
#            self.fields['reason'].widget = forms.HiddenInput()
#        else:
#            self.fields['end_date'].widget = forms.HiddenInput()
#            self.fields['unassign_reason'].widget = forms.HiddenInput()
            


    def save(self, user, vehicle, status, commit=True, *args, **kwargs):
        vehicle_driver = super(VehicleDriverForm, self).save(commit=False)
        vehicle_driver.modified_by = user
        vehicle_driver.vehicle = vehicle
        vehicle_driver.status = status

        if not vehicle_driver.created_by_id:
            vehicle_driver.created_by_id = user.id
        if commit:
            vehicle_driver.save()
        return vehicle_driver

    def clean_driver(self):
        driver = self.cleaned_data['driver']
        current_driver = VehicleDriver.objects.filter(end_date__isnull=True).values_list('driver_id', flat=True)
        if driver == self.car.driver and not self.cleaned_data['end_date']:            
            raise forms.ValidationError('Cannot assign vehicle to its current driver. Please select another driver')
        elif driver.id in current_driver:
           raise forms.ValidationError('Cannot assign driver twice. Driver already assigned, please select another driver')
        return driver

class VehicleFuelCardForm(forms.ModelForm):
    vehicle_id = forms.CharField(required = False)

    class Meta:
        model = FuelCard
        exclude = ['deleted', 'created_by', 'modified_by', 'vehicle_assigned', 'vendor', 'card_type', 'cancelled_date']

    def __init__(self, *args, **kwargs):
        vehicle = kwargs.pop('vehicle', None)
        vehicle_id = vehicle.id
        super(VehicleFuelCardForm, self).__init__(*args, **kwargs)
        self.fields['vehicle_id'].initial=vehicle_id
        self.fields['start_date'].widget.attrs['class'] = 'date_time_field'
        self.fields['card_number'].queryset = FuelCard.objects.filter(vehicle_assigned__id=vehicle_id).order_by('card_number')
        self.fields['card_number'].widget = autocomplete.ListSelect2(url='fleetmanagement:fuel_card-autocomplete',
                                                                     attrs={'data-placeholder': '--- Select Fuel Card ---'},
                                                                     forward=(forward.Const(vehicle_id, 'vehicle_id'),))

    def save(self, user, vehicle, commit=True, *args, **kwargs):
        vehicle_fuel_card = super(VehicleFuelCardForm, self).save(commit=False)
        vehicle_fuel_card.modified_by = user
        vehicle_fuel_card.vehicle = vehicle

        if not vehicle_fuel_card.created_by_id:
            vehicle_fuel_card.created_by_id = user.id
        if commit:
            vehicle_fuel_card.save()
        return vehicle_fuel_card

    def clean(self):
        has_changed = super(VehicleFuelCardForm, self).has_changed()
        cleaned_data = super(VehicleFuelCardForm, self).clean()
        card_number = cleaned_data.get('card_number')
        start_date = cleaned_data.get('start_date')
        if has_changed:
            if card_number == None or card_number== "":
                self._errors['card_number'] = ['This field is required']
            if start_date == None or start_date == "":
                self._errors['start_date'] = ['This field is required']

        return cleaned_data

class VehicleFilterForm(forms.Form):

    vehicle_registration = forms.CharField(required = False)
    driver = forms.CharField(required = False)
    make = forms.CharField(required = False)
    year_model = forms.CharField(required = False)
    purchase_type = forms.ChoiceField(required = False, label = 'Purchase Type',
                                      choices = [('', '--- Select Purchase Type ---')] + list(PurchaseDetail.PURCHASE_TYPES))

    ownership = forms.ChoiceField(required = False, label = 'Vehicle Ownership',
                                  choices = [('', '--- Select Vehicle Ownership ---')] + list(Vehicle.OWNERSHIP_TYPES))

    division = forms.ChoiceField(required = False, label = 'Division',
                                 choices = [('', '--- Select Division ---')] + list(Vehicle.DIVISION_TYPES))

    available = forms.ChoiceField(required = False, label = 'Vehicle Availability',
                                  choices = (('', '--- Select Vehicle Availability ---'),
                                             ('assigned','Assigned'),
                                             ('unassigned','Unassigned')))

    region = forms.ChoiceField(required = False, label='Region',
                               choices=[('','--- Select Region ---')]+list(Region.objects.all().annotate(region_name=Concat('code', V(' - '), 'name')).values_list('id','region_name')))

    district = forms.ChoiceField(required = False, label='District',
                                 choices=[('','--- Select District ---')]+list(Branch.objects.all().annotate(branch_name=Concat('code', V(' - '), 'description')).values_list('id','branch_name')))

    status = forms.ChoiceField(required = False, label='Status')

    def __init__(self, *args, **kwargs):
        super(VehicleFilterForm, self).__init__(*args, **kwargs)

        self.fields['year_model'].widget.attrs['class'] = 'year_field'
        self.fields['vehicle_registration'].widget.attrs['placeholder'] = 'Registration Number'
        self.fields['year_model'].widget.attrs['placeholder'] = 'Year Model'
        self.fields['district'].widget.attrs['class'] = 'cascade'
        self.fields['status'].choices = [('','--- Select Vehicle Status ---')]+list(VehicleStatusType.objects.all().values_list('id','description'))

    def filter(self, vehicles):
        if self.cleaned_data is not None:
            if self.cleaned_data['make']:
                vehicles = vehicles.filter(make__icontains=self.cleaned_data['make'])
            if self.cleaned_data['year_model']:
                vehicles = vehicles.filter(year_model=self.cleaned_data['year_model'])
            if self.cleaned_data['driver']:
                drivers =  Employee.objects.annotate(driver_full_name=Concat('first_name', V(' '), 'last_name')).filter(
                                                   Q(driver_full_name__icontains=self.cleaned_data['driver'])|
                                                   Q(first_name__icontains=self.cleaned_data['driver'])|
                                                   Q(last_name__icontains=self.cleaned_data['driver'])).values_list('id', flat=True)
                vehicles = vehicles.filter(vehicle_driver__driver__in=drivers, vehicle_driver__end_date__isnull=True)
            if self.cleaned_data['vehicle_registration']:
                vehicles = vehicles.filter(registration_number__icontains=self.cleaned_data['vehicle_registration'])
            if self.cleaned_data['available']:
                assignments = VehicleDriver.objects.filter(end_date__isnull=True).values_list('vehicle_id', flat=True)
                if self.cleaned_data['available'] == 'unassigned':
                    vehicles = vehicles.exclude(id__in=assignments)

                if self.cleaned_data['available'] == 'assigned':
                    vehicles = vehicles.filter(id__in=assignments)
            if self.cleaned_data['status']:
                vehicles = vehicles.filter(status=self.cleaned_data['status'])
            if self.cleaned_data['ownership']:
                vehicles = vehicles.filter(ownership=self.cleaned_data['ownership'])
            if self.cleaned_data['division']:
                if not self.cleaned_data['division'] == "all":
                    vehicles = vehicles.filter(division=self.cleaned_data['division'])
            if self.cleaned_data['purchase_type']:
                vehicles = vehicles.filter(purchase_detail__purchase_type=self.cleaned_data['purchase_type'])
            if self.cleaned_data['region']:
                vehicles = vehicles.filter(region__id=self.cleaned_data['region'])
            if self.cleaned_data['district']:
                vehicles = vehicles.filter(district__id=self.cleaned_data['district'])
        return vehicles

class VehicleImportForm(forms.Form):
    vehicles_file = forms.FileField(required=True)

class FuelCardUsageFilterForm(forms.Form):
    date_type = forms.ChoiceField(required = False, label = 'Date Type',
                                  choices = (('transacted','Transaction Date'),
                                             ('imported','Imported Date')))
    date_from = forms.DateTimeField(required=False,label='From Date')
    date_to   = forms.DateTimeField(required=False,label='To Date')
    card_number = forms.CharField(required = False, label="Fuel Card Number")
    vehicle = forms.CharField(required = False, label='Registration Number')
    driver = forms.CharField(required = False)

    def __init__(self, *args, **kwargs):
        super(FuelCardUsageFilterForm, self).__init__(*args, **kwargs)
        self.fields['date_from'].widget.attrs['class'] = 'date_time_field'
        self.fields['date_to'].widget.attrs['class'] = 'date_time_field'

    def filter(self, fuel_card_usage):
        if self.cleaned_data is not None:

            if self.cleaned_data['card_number']:
                fuel_card_usage = fuel_card_usage.filter(Q(fuel_card__card_number__icontains=self.cleaned_data['card_number']))

            if self.cleaned_data['vehicle']:
                fuel_card_usage = fuel_card_usage.filter(Q(vehicle__registration_number__icontains=self.cleaned_data['vehicle']))

            if self.cleaned_data['driver']:
                drivers =  Employee.objects.annotate(driver_full_name=Concat('first_name', V(' '), 'last_name')).filter(
                                                       Q(driver_full_name__icontains=self.cleaned_data['driver'])|
                                                       Q(first_name__icontains=self.cleaned_data['driver'])|
                                                       Q(last_name__icontains=self.cleaned_data['driver'])).values_list('id', flat=True)
                fuel_card_usage = fuel_card_usage.filter(driver__id__in=drivers)

            if self.cleaned_data['date_type'] == "transacted":
                if self.cleaned_data['date_to']:
                    fuel_card_usage = fuel_card_usage.filter(transaction_date__lte=self.cleaned_data['date_to'])

                if self.cleaned_data['date_from']:
                    fuel_card_usage = fuel_card_usage.filter(transaction_date__gte=self.cleaned_data['date_from'])
            else:
                if self.cleaned_data['date_to']:
                    fuel_card_usage = fuel_card_usage.filter(created_at__lte=self.cleaned_data['date_to'])

                if self.cleaned_data['date_from']:
                    fuel_card_usage = fuel_card_usage.filter(created_at__gte=self.cleaned_data['date_from'])


        return fuel_card_usage.order_by('-transaction_date')

class FuelUsageFilterForm(forms.Form):
    date_type = forms.ChoiceField(required = False, label = 'Date Type',
                                  choices = (('transacted','Transaction Date'),
                                             ('imported','Imported Date')))
    date_from = forms.DateTimeField(required=False,label='From Date')
    date_to   = forms.DateTimeField(required=False,label='To Date')
    card_number = forms.CharField(required = False, label="Fuel Card Number")
    vehicle = forms.CharField(required = False, label='Registration Number')
    driver = forms.CharField(required = False)

    def __init__(self, *args, **kwargs):
        super(FuelUsageFilterForm, self).__init__(*args, **kwargs)
        dt = datetime.today()
        df = dt.replace(day=1)
        self.fields['date_from'].widget.attrs['class'] = 'date_time_field'
        self.initial['date_from'] = df
        self.fields['date_to'].widget.attrs['class'] = 'date_time_field'
        self.initial['date_to'] = dt

    def filter(self, fuel_card_usage):
        if self.cleaned_data is not None:

            if self.cleaned_data['card_number']:
                fuel_card_usage = fuel_card_usage.filter(Q(fuel_card__card_number__icontains=self.cleaned_data['card_number']))

            if self.cleaned_data['vehicle']:
                fuel_card_usage = fuel_card_usage.filter(Q(vehicle__registration_number__icontains=self.cleaned_data['vehicle']))

            if self.cleaned_data['driver']:
                drivers =  Employee.objects.annotate(driver_full_name=Concat('first_name', V(' '), 'last_name')).filter(
                                                       Q(driver_full_name__icontains=self.cleaned_data['driver'])|
                                                       Q(first_name__icontains=self.cleaned_data['driver'])|
                                                       Q(last_name__icontains=self.cleaned_data['driver'])).values_list('id', flat=True)
                fuel_card_usage = fuel_card_usage.filter(driver__id__in=drivers)

            if not self.cleaned_data['date_to'] or self.cleaned_data['date_to'] is None:
                if not self.cleaned_data['date_from'] or self.cleaned_data['date_from'] is None:
                    date_to = datetime.today()
                    date_from = date_to.replace(day=1)
                else:
                    date_from = (self.cleaned_data['date_from']).date()
                    if date_from.month == 12:
                        last_of_month = date_from.replace(day=31)
                    else:
                        last_of_month = date_from.replace(month=date_from.month+1, day=1) - timedelta(days=1)
                    date_to   = last_of_month
            else:
                if not self.cleaned_data['date_from'] or self.cleaned_data['date_from'] is None:
                    date_from = date_to.replace(day=1)
                else:
                    date_from = (self.cleaned_data['date_from']).date()
                    date_to = (self.cleaned_data['date_to']).date()
            if self.cleaned_data['date_type'] == "transacted":
                fuel_card_usage = fuel_card_usage.filter(transaction_date__range=(date_from,date_to))
            else:
                fuel_card_usage = fuel_card_usage.filter(created_at__range=(date_from,date_to))


        return fuel_card_usage.order_by('-transaction_date')

class FuelCardUsageListForm(forms.Form):

    class Meta:
        model = FuelCardUsage
        exclude = ['deleted', 'created_by', 'modified_by']

    def __init__(self, *args, **kwargs):
        super(FuelCardUsageListForm, self).__init__(*args, **kwargs)

class FuelCardImportForm(forms.Form):
    fuel_card_file = forms.FileField(required=True)

class VehicleAssignForm(forms.ModelForm):
    class Meta:
        model = VehicleDriver
        exclude = ['vehicle', 'start_date', 'end_date', 'created_by', 'modified_by']

    def __init__(self, *args, **kwargs):
        vehicle = kwargs.pop('vehicle', None)
        super(VehicleAssignForm, self).__init__(*args, **kwargs)
        drivers = Employee.objects.all()
        if vehicle.driver:
            drivers = Employee.objects.exclude(pk=vehicle.driver.pk)
        self.fields['driver'].queryset = drivers

class IncidentForm(forms.ModelForm):

    class Meta:
        model = Incident
        exclude = ['deleted', 'created_by']

    def __init__(self, *args, **kwargs):
        super(IncidentForm, self).__init__(*args, **kwargs)
        self.fields['incident_date'].widget.attrs['class'] = 'date_field'

class DocumentFileForm(forms.ModelForm):

    document_type = forms.ChoiceField(required = False, label='Document Type',
                                      choices=[('','--- Select Document Type ---')]+list(VehicleDocument.DOCUMENT_TYPES))

    class Meta:
        model = Document
        fields = ['document', 'description']


    def __init__(self, *args, **kwargs):
        super(DocumentFileForm, self).__init__(*args, **kwargs)
        self.fields['document'].required = True
        self.fields['description'].widget.attrs['rows'] = 5

    def save(self, commit=True, *args, **kwargs):
        document = super(DocumentFileForm, self).save(commit=False)
        if commit:
            document.save()

        return document

class PhotoFileForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ['image', 'description']

class TrafficFineForm(forms.ModelForm):

    driver = forms.ModelChoiceField(queryset=Employee.objects.all().order_by('first_name','last_name'),
                                    required=False,
                                    widget=autocomplete.ListSelect2(url='fleetmanagement:driver-autocomplete',
                                                                    attrs={'data-placeholder': '--- Select Driver ---'}))

    vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.all().order_by('registration_number'),
                                     label='Registration Number',
                                     widget=autocomplete.ListSelect2(url='fleetmanagement:vehicle-autocomplete',
                                                                     attrs={'data-placeholder': '--- Select Registration Number ---'}))

    description = forms.CharField(required=True, widget=forms.Textarea)

    cost = forms.DecimalField(required=False, max_digits=10, decimal_places=2, label="Fine Amount")
    class Meta:
        model = Incident

        exclude = ['deleted', 'incident_type', 'created_by', 'vehicle_driver', 'status','driver_co_payment','invoice_amount']

    def __init__(self, *args, **kwargs):
        super(TrafficFineForm, self).__init__(*args, **kwargs)
        self.fields['incident_date'].widget.attrs['class'] = 'date_time_field'
        self.fields['incident_date'].widget.attrs['placeholder'] = 'Incident Date'
        self.fields['date_recieved_by_fleet'].widget.attrs['class'] = 'date_time_field'
        self.fields['date_sent_to_finance'].widget.attrs['class'] = 'date_time_field'
        self.fields['cost'].widget.attrs['label'] = 'Fine Amount'
        self.fields['driver'].queryset = Employee.objects.all()
        self.fields['driver'].required = False
        self.fields['driver'].widget.attrs['class'] = 'auto_select'
        self.fields['description'].widget.attrs['rows'] = 8

class TrafficFineDocumentForm(forms.ModelForm):

    class Meta:
        model = IncidentDocument
        fields = ['document_type']

    def __init__(self, *args, **kwargs):
        super(TrafficFineDocumentForm, self).__init__(*args, **kwargs)
        self.fields['document_type'].widget = SelectMultiple()
        self.fields['document_type'].widget.attrs['class'] = 'multi_select'
        self.fields['document_type'].queryset = IncidentDocumentUploads.objects.exclude(incident_type='Incident')


class AddIncidentForm(forms.ModelForm):

    driver = forms.ModelChoiceField(queryset=Employee.objects.all().order_by('first_name','last_name'),
                                    required=True,
                                    widget=autocomplete.ListSelect2(url='fleetmanagement:driver-autocomplete',
                                                                    attrs={'data-placeholder': '--- Select Driver ---'}))
    incident_type = forms.ChoiceField(choices=[('', '--- Select Incident Type ---')]+list(Incident.INCIDENT_TYPES), label='Incident Type',)
    description = forms.CharField(widget=forms.Textarea)
    vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.all().order_by('registration_number'),
                                     label='Registration Number',
                                     widget=autocomplete.ListSelect2(url='fleetmanagement:vehicle-autocomplete',
                                                                     attrs={'data-placeholder': '--- Select Registration Number ---'}))
    cost = forms.CharField(required = False, label="Quote Amount")
    driver_co_payment =  forms.ChoiceField(required = False,
                                           choices=[('', '--- Select Type ---')]+list(Incident.CO_PAYMENTS))
    drivers_licence = forms.CharField(required=False, label = 'Drivers Licence')
    expiry_date = forms.CharField(required=False, label = 'Expiry Date')

    class Meta:
        model = Incident
        exclude = ['deleted', 'created_by', 'vehicle_driver']

    def __init__(self, *args, **kwargs):
        super(AddIncidentForm, self).__init__(*args, **kwargs)
        self.fields['incident_date'].widget.attrs['class'] = 'date_time_field'
        self.fields['incident_date'].widget.attrs['placeholder'] = 'Incident Date'
        self.fields['driver'].queryset = Employee.objects.all()
        self.fields['driver'].required = False
        self.fields['driver'].widget.attrs['class'] = 'auto_select'
        self.fields['percentage'].widget.attrs['type'] = "number"
        self.fields['description'].widget.attrs['rows'] = 5

    def clean(self):
        cleaned_data = super(AddIncidentForm, self).clean()
        driver_co_payment = self.cleaned_data.get("driver_co_payment")
        percentage = self.cleaned_data.get("percentage")
        if driver_co_payment == "yes" and not percentage:
            self._errors['percentage'] = ['This field is required when Driver Co Payment is Yes']
        return cleaned_data


class IncidentFileForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ['document']

class InsuranceClaimFileForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ['document']

class IncidentFilterForm(forms.Form):


    vehicle = forms.CharField(required = False, label = 'Registration Number')
    driver = forms.CharField(required = False, label = 'Driver')
    start_date = forms.CharField(required=False, label='Start date')
    end_date = forms.CharField(required=False, label='End date')
    incident_type = forms.ChoiceField(required = False, choices=[('','--- Select Incident Type ---')]+list(Incident.INCIDENT_TYPES))
    division = forms.ChoiceField(required = False, label = 'Division', choices = [('', '--- Select Division ---')] + list(Vehicle.DIVISION_TYPES))

    def __init__(self, *args, **kwargs):
        super(IncidentFilterForm, self).__init__(*args, **kwargs)

        self.fields['end_date'].widget.attrs['class'] = 'date_time_field'
        self.fields['start_date'].widget.attrs['class'] = 'date_time_field'
        self.fields['start_date'].widget.attrs['placeholder'] = 'Start Date'
        self.fields['end_date'].widget.attrs['placeholder'] = 'End Date'

    def filter(self, incidents, vehicles=None):

        if self.cleaned_data is not None:

            if self.cleaned_data['vehicle']:
                incidents = incidents.filter(vehicle__registration_number__icontains=self.cleaned_data['vehicle'])

            if self.cleaned_data['driver']:
                 drivers =  Employee.objects.annotate(driver_full_name=Concat('first_name', V(' '), 'last_name')).filter(
                                                       Q(driver_full_name__icontains=self.cleaned_data['driver'])|
                                                       Q(first_name__icontains=self.cleaned_data['driver'])|
                                                       Q(last_name__icontains=self.cleaned_data['driver'])).values_list('id', flat=True)
                 incidents = incidents.filter(driver__id__in=drivers)

            if self.cleaned_data['incident_type']:
                incidents = incidents.filter(incident_type__icontains=self.cleaned_data['incident_type'])


            if self.cleaned_data['start_date']:
                    incidents = incidents.filter(incident_date__gte = self.cleaned_data['start_date'])

            if self.cleaned_data['end_date']:
                    incidents = incidents.filter(incident_date__lte = self.cleaned_data['end_date'])

            if self.cleaned_data['division']:
                if not self.cleaned_data['division'] == "all":
                    incidents = incidents.filter(vehicle__division=self.cleaned_data['division'])

        return incidents


class TrafficFineFilterForm(forms.Form):


    vehicle = forms.CharField(required = False, label = 'Registration Number')
    driver = forms.CharField(required = False, label = 'Driver')
    start_date = forms.CharField(required=False, label='Start date')
    end_date = forms.CharField(required=False, label='End date')
    status = forms.ChoiceField(required = False, choices=[('','--- Select Status ---'), ('all','All'),
                                                          ('resolve','Resolve'),
                                                          ('resolved','Resolved')])
    division = forms.ChoiceField(required = False, label = 'Division', choices = [('', '--- Division ---')] + list(Vehicle.DIVISION_TYPES))

    def __init__(self, *args, **kwargs):
        super(TrafficFineFilterForm, self).__init__(*args, **kwargs)

        self.fields['end_date'].widget.attrs['class'] = 'date_field'
        self.fields['start_date'].widget.attrs['class'] = 'date_field'
        self.fields['start_date'].widget.attrs['placeholder'] = 'Start Date'
        self.fields['end_date'].widget.attrs['placeholder'] = 'End Date'

    def filter(self, incidents=None, vehicles=None):

        if self.cleaned_data is not None:

            if self.cleaned_data['vehicle']:
                incidents = incidents.filter(vehicle__registration_number__icontains=self.cleaned_data['vehicle'])

            if self.cleaned_data['driver']:
                 drivers =  Employee.objects.annotate(driver_full_name=Concat('first_name', V(' '), 'last_name')).filter(
                                                       Q(driver_full_name__icontains=self.cleaned_data['driver'])|
                                                       Q(first_name__icontains=self.cleaned_data['driver'])|
                                                       Q(last_name__icontains=self.cleaned_data['driver'])).values_list('id', flat=True)
                 incidents = incidents.filter(driver__id__in=drivers)

            if self.cleaned_data['status']:
                if not self.cleaned_data['status'] == "all":
                    if self.cleaned_data['status'] == 'resolved':
                        incidents = incidents.filter(resolved=True)
                    if self.cleaned_data['status'] == 'resolve':
                        incidents = incidents.filter(resolved=False)

            if self.cleaned_data['start_date']:
                incidents = incidents.filter(incident_date__gte = self.cleaned_data['start_date'])

            if self.cleaned_data['end_date']:
                    incidents = incidents.filter(incident_date__lte = self.cleaned_data['end_date'])

            if self.cleaned_data['division']:
                if not self.cleaned_data['division'] == "all":
                    incidents = incidents.filter(vehicle__division=self.cleaned_data['division'])

        return incidents


class IncidentDocumentForm(forms.ModelForm):

    class Meta:
        model = IncidentDocument
        fields = ['document_type']

    def __init__(self, *args, **kwargs):
        super(IncidentDocumentForm, self).__init__(*args, **kwargs)
        self.fields['document_type'].widget = SelectMultiple()
        self.fields['document_type'].widget.attrs['class'] = 'multi_select'
        self.fields['document_type'].queryset = IncidentDocumentUploads.objects.exclude(incident_type='Traffic Fine')



class VehicleMaintenanceFilterForm(forms.Form):

    search = forms.CharField(required = False, label = 'Search')
    start_date = forms.CharField(required=False, label='Start date')
    end_date = forms.CharField(required=False, label='End date')
    division = forms.ChoiceField(required = False, label = 'Division', choices = [('', '--- Select Division ---')] + list(Vehicle.DIVISION_TYPES))


    def __init__(self, *args, **kwargs):
        super(VehicleMaintenanceFilterForm, self).__init__(*args, **kwargs)

        self.fields['end_date'].widget.attrs['class'] = 'date_field'
        self.fields['start_date'].widget.attrs['class'] = 'date_field'
        self.fields['start_date'].widget.attrs['placeholder'] = 'Start Date'
        self.fields['end_date'].widget.attrs['placeholder'] = 'End Date'
        self.fields['search'].widget.attrs['placeholder'] = 'Search Registration Number, Driver....'

    def filter(self, vehicle_maintenances):

        if self.cleaned_data is not None:

            if self.cleaned_data['start_date']:
                    vehicle_maintenances = vehicle_maintenances.filter(end_date__gte = self.cleaned_data['start_date'])

            if self.cleaned_data['end_date']:
                    vehicle_maintenances = vehicle_maintenances.filter(end_date__lte = self.cleaned_data['end_date'])

            if self.cleaned_data['division']:
                if not self.cleaned_data['division'] == "all":
                    vehicle_maintenances = vehicle_maintenances.filter(vehicle__division=self.cleaned_data['division'])

            if self.cleaned_data['search']:

                drivers =  Employee.objects.annotate(driver_full_name=Concat('first_name', V(' '), 'last_name')).filter(
                                                   Q(driver_full_name__icontains=self.cleaned_data['search'])|
                                                   Q(first_name__icontains=self.cleaned_data['search'])|
                                                   Q(last_name__icontains=self.cleaned_data['search'])).values_list('id', flat=True)

                if not self.cleaned_data['search'] == 'Unassigned':
                    vehicle_maintenances = vehicle_maintenances.filter(Q(vehicle__vehicle_driver__driver__in=drivers)|
                                                                       Q(vehicle__registration_number__icontains=self.cleaned_data['search']))
                else:
                    vehicle_maintenances = vehicle_maintenances.filter(Q(vehicle__vehicle_driver__driver__isnull=True))

        return vehicle_maintenances

class ServiceBookingForm(forms.ModelForm):

    vendor = forms.ModelChoiceField(queryset=Vendor.objects.filter(vendor_type='service provider'),
                                     label='Service Provider',
                                     widget=autocomplete.ListSelect2(url='fleetmanagement:vendor_service_provider-autocomplete',
                                                                     attrs={'data-placeholder': '--- Select Service Provider ---'}))
    service_date = forms.DateTimeField(required=True, label='Service/Maintenance Date')
    booking_date = forms.DateTimeField(required=True)
    document_date = forms.DateTimeField(required=True)

    class Meta:
        model = ServiceBooking
        exclude = ['deleted', 'modified_by', 'created_by', 'vehicle']

    def __init__(self, *args, **kwargs):
        super(ServiceBookingForm, self).__init__(*args, **kwargs)
        self.fields['booking_date'].widget.attrs['class'] = 'date_time_field'
        self.fields['service_date'].widget.attrs['class'] = 'date_time_field'
        self.fields['document_date'].widget.attrs['class'] = 'date_field'

    def save(self, commit=True, *args, **kwargs):
        service_booking = super(ServiceBookingForm, self).save(commit=False)

        if commit:
            service_booking.save()

        return service_booking

class AddServiceBookingForm(forms.ModelForm):

    SERVICES_INTERVALS = (('5000', '5 000km'),('10000', '10 000km'),('15000', '15 000km'),('20000', '20 000km'),('25000', '25 000km'),
                        ('30000', '30 000km'),('35000', '35 000km'),('40000', '40 000km'),('45000', '45 000km'),('50000', '50 000km'),
                        ('55000', '55 000km'),('60000', '60 000km'),('65000', '65 000km'),('70000', '70 000km'),('75000', '75 000km'),
                        ('80000', '80 000km'),('85000', '85 000km'),('90000', '90 000km'),('95000', '95 000km'),('100000', '100 000km'),
                        ('105000', '105 000km'),('110000', '110 000km'),('115000', '115 000km'),('120000', '120 000km'),('125000', '125 000km'),
                        ('130000', '130 000km'),('135000', '135 000km'),('140000', '140 000km'),('145000', '145 000km'),('150000', '150 000km'),
                        ('155000', '155 000km'),('160000', '160 000km'),('165000', '165 000km'),('170000', '170 000km'),('175000', '175 000km'),
                        ('180000', '180 000km'),('185000', '185 000km'),('190000', '190 000km'),('195000', '195 000km'),('200000', '200 000km'),
                        ('205000', '205 000km'),('210000', '210 000km'),('215000', '215 000km'),('220000', '220 000km'),('225000', '225 000km'),
                        ('230000', '230 000km'),('235000', '235 000km'),('240000', '240 000km'),('245000', '245 000km'),('250000', '250 000km'),
                        ('255000', '255 000km'),('260000', '260 000km'),('265000', '265 000km'),('270000', '270 000km'),('275000', '275 000km'),
                        ('280000', '280 000km'),('285000', '285 000km'),('290000', '290 000km'),('295000', '295 000km'),('300000', '300 000km'),
                        ('305000', '305 000km'),('310000', '310 000km'),('315000', '315 000km'),('320000', '320 000km'),('325000', '325 000km'),
                        ('330000', '330 000km'),('335000', '335 000km'),('340000', '340 000km'),('345000', '345 000km'),('350000', '350 000km'),
                        ('355000', '355 000km'),('360000', '360 000km'),('365000', '365 000km'),('370000', '370 000km'),('375000', '375 000km'),
                        ('380000', '380 000km'),('385000', '385 000km'),('390000', '390 000km'),('395000', '395 000km'),('400000', '400 000km'),
                        )
    DOCUMENT_TYPES = (('','--- Select Answer ---'),('Invoice', 'Invoice'), ('Proof of Payment','Proof of Payment'), ('Quote', 'Quote'))

    SERVICEBOOKING_STATUSES = (('booked','Booked'),('escalated', 'Escalated'),('awaiting authorisation', 'Awaiting Authorisation'),
                            ('authorised', 'Authorised'),('declined', 'Declined'))

    vendor = forms.ModelChoiceField(queryset=Vendor.objects.filter(vendor_type='service provider'),
                                     label='Service Provider',
                                     widget=autocomplete.ListSelect2(url='fleetmanagement:vendor_service_provider-autocomplete',
                                                                     attrs={'data-placeholder': '--- Select Service Provider ---'}))
    vehicle = forms.ModelChoiceField(required=True, queryset=Vehicle.objects.all().order_by('registration_number'),
                                     label='Registration Number',
                                     widget=autocomplete.ListSelect2(url='fleetmanagement:vehicle-autocomplete',
                                                                     attrs={'data-placeholder': '--- Select Registration Number ---'}))

    service_date = forms.DateTimeField(required = False, label = 'Service/Maintenance Date')
    follow_up_date = forms.DateTimeField(required = False)
    service_interval = forms.ChoiceField(required = False, label="Service Interval", choices = [('', '--- Select Service Interval ---')] + list(SERVICES_INTERVALS))
    balances = forms.CharField(required=False, label = 'Balances')
    drivers  = forms.CharField(required=False, label = 'Driver')
    document_received = forms.ChoiceField(required = False, label="Document Type", choices = [('', '--- Select Document Type ---')] + list(DOCUMENT_TYPES))
    status = forms.ChoiceField(required = False, choices = [('', '--- Select Status ---')] + list(SERVICEBOOKING_STATUSES))

    class Meta:
        model = ServiceBooking
        exclude = ['deleted', 'created_by', 'modified_by']

    def __init__(self, *args, **kwargs):
        super(AddServiceBookingForm, self).__init__(*args, **kwargs)
        self.fields['booking_date'].widget.attrs['class'] = 'date_time_field'
        self.fields['service_date'].widget.attrs['class'] = 'date_time_field'
        self.fields['document_date'].widget.attrs['class'] = 'date_field'
        self.fields['follow_up_date'].widget.attrs['class'] = 'date_field'
        self.fields['drivers'].widget.attrs['class'] = 'auto_select'


    def save(self, commit=True, *args, **kwargs):
        service_booking = super(AddServiceBookingForm, self).save(commit=False)

        if commit:
            service_booking.save()

        return service_booking

    def clean_follow_up_date(self):
        follow_up_date = self.cleaned_data['follow_up_date']
        long_term_repairs = self.cleaned_data['long_term_repairs']
        if long_term_repairs is True and not follow_up_date:
            raise forms.ValidationError('This field is required')
        return follow_up_date

    def clean_driver(self):
        driver = self.cleaned_data['driver']
        current_driver = VehicleDriver.objects.filter(end_date__isnull=True).values_list('driver_id', flat=True)
        if driver == self.car.driver:
            raise forms.ValidationError('Cannot assign vehicle to its current driver. Please select another driver')
        elif driver.id in current_driver:
           raise forms.ValidationError('Cannot assign driver twice. Driver already assigned, please select another driver')
        return driver

class ServiceBookingInvoiceForm(forms.ModelForm):

    SERVICES_INTERVALS = (('5000', '5 000km'),('10000', '10 000km'),('15000', '15 000km'),('20000', '20 000km'),('25000', '25 000km'),
                        ('30000', '30 000km'),('35000', '35 000km'),('40000', '40 000km'),('45000', '45 000km'),('50000', '50 000km'),
                        ('55000', '55 000km'),('60000', '60 000km'),('65000', '65 000km'),('70000', '70 000km'),('75000', '75 000km'),
                        ('80000', '80 000km'),('85000', '85 000km'),('90000', '90 000km'),('95000', '95 000km'),('100000', '100 000km'),
                        ('105000', '105 000km'),('110000', '110 000km'),('115000', '115 000km'),('120000', '120 000km'),('125000', '125 000km'),
                        ('130000', '130 000km'),('135000', '135 000km'),('140000', '140 000km'),('145000', '145 000km'),('150000', '150 000km'),
                        ('155000', '155 000km'),('160000', '160 000km'),('165000', '165 000km'),('170000', '170 000km'),('175000', '175 000km'),
                        ('180000', '180 000km'),('185000', '185 000km'),('190000', '190 000km'),('195000', '195 000km'),('200000', '200 000km'),
                        ('205000', '205 000km'),('210000', '210 000km'),('215000', '215 000km'),('220000', '220 000km'),('225000', '225 000km'),
                        ('230000', '230 000km'),('235000', '235 000km'),('240000', '240 000km'),('245000', '245 000km'),('250000', '250 000km'),
                        ('255000', '255 000km'),('260000', '260 000km'),('265000', '265 000km'),('270000', '270 000km'),('275000', '275 000km'),
                        ('280000', '280 000km'),('285000', '285 000km'),('290000', '290 000km'),('295000', '295 000km'),('300000', '300 000km'),
                        ('305000', '305 000km'),('310000', '310 000km'),('315000', '315 000km'),('320000', '320 000km'),('325000', '325 000km'),
                        ('330000', '330 000km'),('335000', '335 000km'),('340000', '340 000km'),('345000', '345 000km'),('350000', '350 000km'),
                        ('355000', '355 000km'),('360000', '360 000km'),('365000', '365 000km'),('370000', '370 000km'),('375000', '375 000km'),
                        ('380000', '380 000km'),('385000', '385 000km'),('390000', '390 000km'),('395000', '395 000km'),('400000', '400 000km'),
                        )
    DOCUMENT_TYPES = (('','--- Select Answer ---'),('Invoice', 'Invoice'), ('Proof of Payment','Proof of Payment'), ('Quote', 'Quote'))

    SERVICEBOOKING_STATUSES = (('captured','Captured'),('resolved', 'Resolved'))

    vendor = forms.ModelChoiceField(queryset=Vendor.objects.filter(vendor_type='service provider'),
                                     label='Service Provider',
                                     widget=autocomplete.ListSelect2(url='fleetmanagement:vendor_service_provider-autocomplete',
                                                                     attrs={'data-placeholder': '--- Select Service Provider ---'}))
    vehicle = forms.ModelChoiceField(required=True, queryset=Vehicle.objects.all().order_by('registration_number'),
                                     label='Registration Number',
                                     widget=autocomplete.ListSelect2(url='fleetmanagement:vehicle-autocomplete',
                                                                     attrs={'data-placeholder': '--- Select Registration Number ---'}))

    service_date = forms.DateTimeField(required = False, label = 'Service/Maintenance Date')
    follow_up_date = forms.DateTimeField(required = False)
    service_interval = forms.ChoiceField(required = False, label="Service Interval", choices = [('', '--- Select Service Interval ---')] + list(SERVICES_INTERVALS))
    balances = forms.CharField(required=False, label = 'Balances')
    drivers  = forms.CharField(required=False, label = 'Driver')
    document_received = forms.ChoiceField(required = False, label="Document Type", choices = [('', '--- Select Document Type ---')] + list(DOCUMENT_TYPES))

    class Meta:
        model = ServiceBooking
        exclude = ['deleted', 'created_by', 'modified_by']

    def __init__(self, *args, **kwargs):
        super(ServiceBookingInvoiceForm, self).__init__(*args, **kwargs)
        self.fields['booking_date'].widget.attrs['class'] = 'date_time_field'
        self.fields['service_date'].widget.attrs['class'] = 'date_time_field'
        self.fields['document_date'].widget.attrs['class'] = 'date_field'
        self.fields['follow_up_date'].widget.attrs['class'] = 'date_field'
        self.fields['drivers'].widget.attrs['class'] = 'auto_select'
        self.fields['status'].widget.attrs['readonly'] = True


    def save(self, commit=True, *args, **kwargs):
        service_booking = super(ServiceBookingInvoiceForm, self).save(commit=False)

        if commit:
            service_booking.save()

        return service_booking

    def clean_follow_up_date(self):
        follow_up_date = self.cleaned_data['follow_up_date']
        long_term_repairs = self.cleaned_data['long_term_repairs']
        if long_term_repairs is True and not follow_up_date:
            raise forms.ValidationError('This field is required')
        return follow_up_date

    # def clean_driver(self):
    #     driver = self.cleaned_data['driver']
    #     current_driver = VehicleDriver.objects.filter(end_date__isnull=True).values_list('driver_id', flat=True)
    #     if driver == self.car.driver:
    #         raise forms.ValidationError('Cannot assign vehicle to its current driver. Please select another driver')
    #     elif driver.id in current_driver:
    #        raise forms.ValidationError('Cannot assign driver twice. Driver already assigned, please select another driver')
    #     return driver

class ServiceBookingFilterForm(forms.Form):

    SERVICES_INTERVALS = (('5000', '5 000km'),('10000', '10 000km'),('15000', '15 000km'),('20000', '20 000km'),('25000', '25 000km'),
                        ('30000', '30 000km'),('35000', '35 000km'),('40000', '40 000km'),('45000', '45 000km'),('50000', '50 000km'),
                        ('55000', '55 000km'),('60000', '60 000km'),('65000', '65 000km'),('70000', '70 000km'),('75000', '75 000km'),
                        ('80000', '80 000km'),('85000', '85 000km'),('90000', '90 000km'),('95000', '95 000km'),('100000', '100 000km'),
                        ('105000', '105 000km'),('110000', '110 000km'),('115000', '115 000km'),('120000', '120 000km'),('125000', '125 000km'),
                        ('130000', '130 000km'),('135000', '135 000km'),('140000', '140 000km'),('145000', '145 000km'),('150000', '150 000km'),
                        ('155000', '155 000km'),('160000', '160 000km'),('165000', '165 000km'),('170000', '170 000km'),('175000', '175 000km'),
                        ('180000', '180 000km'),('185000', '185 000km'),('190000', '190 000km'),('195000', '195 000km'),('200000', '200 000km'), 
                        ('205000', '205 000km'),('210000', '210 000km'),('215000', '215 000km'),('220000', '220 000km'),('225000', '225 000km'),
                        ('230000', '230 000km'),('235000', '235 000km'),('240000', '240 000km'),('245000', '245 000km'),('250000', '250 000km'),
                        ('255000', '255 000km'),('260000', '260 000km'),('265000', '265 000km'),('270000', '270 000km'),('275000', '275 000km'),
                        ('280000', '280 000km'),('285000', '285 000km'),('290000', '290 000km'),('295000', '295 000km'),('300000', '300 000km'),
                        ('305000', '305 000km'),('310000', '310 000km'),('315000', '315 000km'),('320000', '320 000km'),('325000', '325 000km'),
                        ('330000', '330 000km'),('335000', '335 000km'),('340000', '340 000km'),('345000', '345 000km'),('350000', '350 000km'),
                        ('355000', '355 000km'),('360000', '360 000km'),('365000', '365 000km'),('370000', '370 000km'),('375000', '375 000km'),
                        ('380000', '380 000km'),('385000', '385 000km'),('390000', '390 000km'),('395000', '395 000km'),('400000', '400 000km'),
                        )

    vehicle_registration = forms.CharField(required = False, label = 'Search')
    search = forms.CharField(required = False, label = 'Search')
    division = forms.ChoiceField(required = False, label = 'Division', choices = [('', '--- Select Division ---')] + list(Vehicle.DIVISION_TYPES))
    service_interval = forms.ChoiceField(required = False, choices = [('', '--- Select Service Interval ---')] + list(SERVICES_INTERVALS))
    start_date = forms.DateTimeField(required=False, label='Start date')
    end_date = forms.DateTimeField(required=False, label='End date')

    def __init__(self, *args, **kwargs):
        super(ServiceBookingFilterForm, self).__init__(*args, **kwargs)

        self.fields['end_date'].widget.attrs['class'] = 'date_field'
        self.fields['start_date'].widget.attrs['class'] = 'date_field'
        self.fields['start_date'].widget.attrs['placeholder'] = 'Start Date'
        self.fields['end_date'].widget.attrs['placeholder'] = 'End Date'
        self.fields['search'].widget.attrs['placeholder'] = 'Search Driver....'
        self.fields['vehicle_registration'].widget.attrs['placeholder'] = 'Search Registration Number....'

    def filter(self, service_bookings):

        if self.cleaned_data is not None:

            if self.cleaned_data['division']:
                if not self.cleaned_data['division'] == "all":
                    service_bookings = service_bookings.filter(vehicle__division=self.cleaned_data['division'])

            if self.cleaned_data['service_interval']:
                    service_bookings = service_bookings.filter(service_interval__icontains = self.cleaned_data['service_interval'])

            if self.cleaned_data['start_date']:
                    service_bookings = service_bookings.filter(follow_up_date__gte = self.cleaned_data['start_date'])

            if self.cleaned_data['end_date']:
                    service_bookings = service_bookings.filter(follow_up_date__lte = self.cleaned_data['end_date'])

            if self.cleaned_data['vehicle_registration']:
                    service_bookings = service_bookings.filter(vehicle__registration_number__icontains = self.cleaned_data['vehicle_registration'])

            if self.cleaned_data['search']:

                drivers =  Employee.objects.annotate(driver_full_name=Concat('first_name', V(' '), 'last_name')).filter(
                                                   Q(driver_full_name__icontains=self.cleaned_data['search'])|
                                                   Q(first_name__icontains=self.cleaned_data['search'])|
                                                   Q(last_name__icontains=self.cleaned_data['search'])).values_list('id', flat=True)

                if not self.cleaned_data['search'] == 'Unassigned':
                    service_bookings = service_bookings.filter(Q(vehicle__vehicle_driver__driver__in=drivers, vehicle__vehicle_driver__end_date__isnull=True))
                else:
                    service_bookings = service_bookings.filter(Q(vehicle__vehicle_driver__driver__isnull=True))

        return service_bookings

class AssignDriverAuthorizationForm(forms.ModelForm):

    reason = forms.ChoiceField(required = False,
                                      choices = [('', '--- Select Reason ---')] +
                                                list(VehicleDriver.REASONS))

    class Meta:
        model = VehicleDriver
        exclude = ['deleted',
                   'created_by',
                   'modified_by',
                   'end_date']

    def __init__(self, *args, **kwargs):
        super(AssignDriverAuthorizationForm, self).__init__(*args, **kwargs)
        self.fields['vehicle'].widget.attrs['disabled'] = True
        self.fields['driver'].widget.attrs['disabled'] = True
        self.fields['start_date'].widget.attrs['disabled'] = True
        self.fields['reason'].widget.attrs['disabled'] = True

class AddVehicleDriverForm(forms.ModelForm):

    UNASSIGN_REASONS = (('none','None'),
                        ('adsconded', 'Absconded'),
                        ('discretionary change','Discretionary Vehicle Change'),
                        ('dismissed','Dismissal'),
                        ('long term repair','Long-term Maintenance/Repairs'),
                        ('relocation','Relocation'),
                        ('resignation','Resignation'),
                        ('suspend','Suspension'),
                        ('temp vehicle','Temp Vehicle'),
                        ('insurance pending','Insurance Claim - Pending'),
                        ('insurance repairs','Insurance Claim - Repairs'),
                        ('writeoff','Write-off'))
    
    unassign_reason = forms.ChoiceField(required = False,
                                      choices = [('', '--- Select Reason ---')] +
                                                list(UNASSIGN_REASONS))

    class Meta:
        model = VehicleDriver
        exclude = ['deleted',
                   'created_by',
                   'modified_by',
                   'vehicle',
                   'start_date',
                   'reason',
                   'driver']

    def __init__(self, *args, **kwargs):
        super(AddVehicleDriverForm, self).__init__(*args, **kwargs)
        self.fields['end_date'].widget.attrs['class'] = 'date_time_field'

class AddFuelCardForm(forms.ModelForm):

    vehicle_assigned = forms.ModelChoiceField(queryset=Vehicle.objects.all().order_by('registration_number'),
                                     label='Registration Number',
                                     widget=autocomplete.ListSelect2(url='fleetmanagement:vehicle-autocomplete',
                                                                     attrs={'data-placeholder': '--- Select Registration Number ---'}))

    card_type = forms.ChoiceField([('', '--- Select Card Type ---')]+list(FuelCard.CARD_TYPES), label='Card Type')

    vendor = forms.ModelChoiceField(queryset=Vendor.objects.filter(vendor_type='fuel card supplier'),
                                     label='Supplier',
                                     widget=autocomplete.ListSelect2(url='fleetmanagement:vendor_fuel_card_supplier-autocomplete',
                                                                     attrs={'data-placeholder': '--- Select Supplier Name ---'}))

    status = forms.ChoiceField([('', '--- Select Status ---')]+list(FuelCard.FUEL_CARD_STATUSES), label='Status')
    class Meta:
        model = FuelCard
        exclude = ['deleted', 'modified_by', 'created_by']
        widgets = {'comment':forms.Textarea(attrs={'rows':4, 'cols':15})}

    def __init__(self, *args, **kwargs):
        super(AddFuelCardForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs['class'] = 'date_time_field'
        self.fields['cancelled_date'].widget.attrs['class'] = 'date_time_field'
        self.fields['date_ordered'].widget.attrs['class'] = 'date_field'
        self.fields['comment'].widget.attrs['rows'] = 5

    def save(self, commit=True, *args, **kwargs):
        fuel_card = super(AddFuelCardForm, self).save(commit=False)

        if commit:
            fuel_card.save(user)

        return fuel_card

    def clean_cancelled_date(self):
        cancelled_date = self.cleaned_data['cancelled_date']
        status = self.cleaned_data['status']
        if status=='cancelled' and not cancelled_date:
            raise forms.ValidationError('This field is required')
        return cancelled_date

    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        status = self.cleaned_data['status']
        if status=='active' and not start_date:
            raise forms.ValidationError('This field is required')
        return start_date


class FuelCardFilterForm(forms.Form):
    card_number = forms.CharField(required = False, label = 'Card Number')
    card_type = forms.ChoiceField([('', '--- Select Card Type ---')]+list(FuelCard.CARD_TYPES),required = False, label='Card Type')
    status = forms.ChoiceField([('', '--- Select Status ---')]+list(FuelCard.FUEL_CARD_STATUSES),required = False, label='Status')
    supplier = forms.CharField(required = False, label = 'Supplier')
    vehicle = forms.CharField(required = False, label = 'Registration Number')
    driver = forms.CharField(required = False, label = 'Driver')
    date_from = forms.DateTimeField(required=False,label='From Date')
    date_to   = forms.DateTimeField(required=False,label='To Date')


    def __init__(self, *args, **kwargs):
        super(FuelCardFilterForm, self).__init__(*args, **kwargs)
        self.fields['date_from'].widget.attrs['class'] = 'date_field'
        self.fields['date_to'].widget.attrs['class'] = 'date_field'


    def filter(self, fuel_cards):

        if self.cleaned_data is not None:

            if self.cleaned_data['card_number']:
                fuel_cards = fuel_cards.filter(card_number__icontains=self.cleaned_data['card_number'])

            if self.cleaned_data['card_type']:
                fuel_cards = fuel_cards.filter(card_type=self.cleaned_data['card_type'])

            if self.cleaned_data['status']:
                fuel_cards = fuel_cards.filter(status=self.cleaned_data['status'])

            if self.cleaned_data['supplier']:
                fuel_cards = fuel_cards.filter(vendor__name__icontains=self.cleaned_data['supplier'])

            if self.cleaned_data['vehicle']:
                fuel_cards = fuel_cards.filter(vehicle_assigned__registration_number__icontains=self.cleaned_data['vehicle'])

            if self.cleaned_data['driver']:
                drivers =  Employee.objects.annotate(driver_full_name=Concat('first_name', V(' '), 'last_name')).filter(
                                                       Q(driver_full_name__icontains=self.cleaned_data['driver'])|
                                                       Q(first_name__icontains=self.cleaned_data['driver'])|
                                                       Q(last_name__icontains=self.cleaned_data['driver'])).values_list('id', flat=True)

                fuel_cards = fuel_cards.filter(vehicle_assigned__vehicle_driver__driver__id__in=drivers,
                                               vehicle_assigned__vehicle_driver__end_date__isnull=True)

            if self.cleaned_data['date_from']:
                fuel_cards = fuel_cards.filter(cancelled_date__gte=self.cleaned_data['date_from'])

            if self.cleaned_data['date_to']:
                fuel_cards = fuel_cards.filter(cancelled_date__lte=self.cleaned_data['date_to'])

        return fuel_cards


class InsuranceClaimForm(forms.ModelForm):

    vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.all().order_by('registration_number'),
                                     label='Registration Number',
                                     widget=autocomplete.ListSelect2(url='fleetmanagement:vehicle-autocomplete',
                                                                     attrs={'data-placeholder': '--- Select Registration Number ---'}))
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.filter(vendor_type='insurance'),
                                     label='Insurance',
                                     widget=autocomplete.ListSelect2(url='fleetmanagement:vendor_insurance-autocomplete',
                                                                     attrs={'data-placeholder': '--- Select Insurance Name ---'}))
    drivers_licence = forms.CharField(required=False, label = 'Drivers Licence')
    expiry_date = forms.CharField(required=False, label = 'Expiry Date')
    division   = forms.CharField(required=False, label = 'Division')
    region  = forms.CharField(required=False, label = 'Region')
    district  = forms.CharField(required=False, label = 'District')
    ownership   = forms.CharField(required=False, label = 'Ownership')
    vin_number = forms.CharField(required=False, label = 'VIN Number')
    engine_number = forms.CharField(required=False, label = 'Engine Number')
    colour = forms.CharField(required=False, label = 'Colour')
    make  = forms.CharField(required=False, label = 'Make')
    model   = forms.CharField(required=False, label = 'Model')
    year_model  = forms.CharField(required=False, label = 'Year Model')

    class Meta:
        model = InsuranceClaim
        exclude = ['deleted', 'created_by', 'modified_by']

    def __init__(self, *args, **kwargs):
        super(InsuranceClaimForm, self).__init__(*args, **kwargs)

        self.fields['submission_date'].widget.attrs['class'] = 'date_field'
        self.fields['insurance_date_recieved'].widget.attrs['class'] = 'date_field'
        self.fields['claim_date_recieved'].widget.attrs['class'] = 'date_field'
        self.fields['incident_date'].widget.attrs['class'] = 'date_time_field'
        self.fields['incident_date'].widget.attrs['placeholder'] = 'Incident Date'
        self.fields['driver'].queryset = Employee.objects.all()
        self.fields['driver'].required = False
        self.fields['driver'].widget.attrs['class'] = 'auto_select'
        self.fields['percentage'].widget.attrs['type'] = "number"
        self.fields['damage_description'].widget.attrs['rows'] = 5
        self.fields['incident_description'].widget.attrs['rows'] = 5

    def clean(self):
        cleaned_data = super(InsuranceClaimForm, self).clean()
        driver_co_payment = self.cleaned_data.get("driver_co_payment")
        percentage = self.cleaned_data.get("percentage")
        if driver_co_payment == "yes" and not percentage:
            self._errors['percentage'] = ['This field is required when Driver Co Payment is Yes']
        return cleaned_data


class InsuranceClaimDocumentForm(forms.ModelForm):

    class Meta:
        model = InsuranceClaimDocument
        fields = ['document_type']

    def __init__(self, *args, **kwargs):
        super(InsuranceClaimDocumentForm, self).__init__(*args, **kwargs)
        self.fields['document_type'].widget = SelectMultiple()
        self.fields['document_type'].widget.attrs['class'] = 'multi_select'
        self.fields['document_type'].queryset = InsuranceClaimDocumentTypes.objects.all()


class InsuranceClaimFilterForm(forms.Form):

    claim_number = forms.CharField(required = False, label="Claim Reference Number")
    claim_type = forms.ChoiceField(choices=[('', '--- Select Type ---'), ('', 'All')]+list(InsuranceClaim.CLAIMTYPES),
                                   required=False)
    start_date = forms.CharField(required=False, label='Start date')
    end_date = forms.CharField(required=False, label='End date')
    quote_number = forms.CharField(required = False, label="Quote Reference Number")
    vehicle = forms.CharField(required = False, label="Registration Number")
    division = forms.ChoiceField(required = False, label = 'Division', choices = [('', '--- Division ---')] + list(Vehicle.DIVISION_TYPES))


    def __init__(self, *args, **kwargs):
        super(InsuranceClaimFilterForm, self).__init__(*args, **kwargs)

        self.fields['start_date'].widget.attrs['class'] = 'date_field'
        self.fields['end_date'].widget.attrs['class'] = 'date_field'

    def filter(self, insurance_claims):
        if self.cleaned_data is not None:

            if self.cleaned_data['claim_type']:
                    insurance_claims = insurance_claims.filter(claim_type=self.cleaned_data['claim_type'])

            if self.cleaned_data['start_date']:
                    insurance_claims = insurance_claims.filter(incident_date__gte = self.cleaned_data['start_date'])

            if self.cleaned_data['end_date']:
                    insurance_claims = insurance_claims.filter(incident_date__lte = self.cleaned_data['end_date'])

            if self.cleaned_data['division']:
                if not self.cleaned_data['division'] == "all":
                    insurance_claims = insurance_claims.filter(vehicle__division=self.cleaned_data['division'])

            if self.cleaned_data['vehicle']:
                insurance_claims = insurance_claims.filter(vehicle__registration_number__icontains=self.cleaned_data['vehicle'])

            if self.cleaned_data['quote_number']:
                insurance_claims = insurance_claims.filter(quote_reference_number__icontains=self.cleaned_data['quote_number'])

            if self.cleaned_data['claim_number']:
                insurance_claims = insurance_claims.filter(insurance_reference_number__icontains=self.cleaned_data['claim_number'])

        return insurance_claims


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs['rows'] = 5

    def save(self, commit=True, *args, **kwargs):
        comment = super(CommentForm, self).save(commit=False)
        if commit:
            comment.save()

        return comment

class ServiceMaintanceDocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ['document']

class MileageImportForm(forms.Form):
    mileage_file = forms.FileField(required=True)        

class AdditionalVehicleInformationImportForm(forms.Form):
    additional_information_file = forms.FileField(required=True)
