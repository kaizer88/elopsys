from django.conf import settings
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.utils.safestring import mark_safe
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, MultiField, ButtonHolder, Submit, HTML
from crispy_forms.bootstrap import TabHolder, Tab, Div
from .models import  FileUpload, \
            VehicleMakeAndModel, InsuranceClaim, MileageLog, \
            Incident, RenewLicenceDisk, FuelCard, FuelAllocation, \
            VehicleMaintenance, VehicleExtras,Trafficfine, Comment,\
            Vehicle,  ServiceBooking, VehicleAllocation, Requisition, RequisitionItem,FuelTransfer
from django.db.models import Q
from employees.models import *
from offices.models import *
from datetime import datetime
from django.forms.widgets import HiddenInput

class fileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ('file',)
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': True}),
        }

    def __init__(self, *args, **kwargs):
        super(fileUploadForm, self).__init__(*args, **kwargs)
        self.fields["file"].widget.attrs["multiple"]=True


class tripImportUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ('file', 'vehicle',)
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': True}),
            'vehicle': forms.Select(),
        }


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comments',)
        widgets = {            
            'comments': forms.Textarea(),
        }


class DrivingLicenceForm(forms.ModelForm):
    class Meta:
        model = DrivingLicence
        fields = '__all__'
        widgets = {
            'date_of_issue': forms.TextInput(attrs={'class': 'datepicker'}),
            'expiry_date': forms.TextInput(attrs={'class': 'datepicker'}),
        }
    def __init__(self,  *args, **kwargs):
        super(DrivingLicenceForm, self).__init__(*args, **kwargs)       
        self.fields['driver'].widget.attrs['id'] = 'id_driver'
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                '',
                Div(
                    'driver',                                         
                    'licence_number',                     
                    'from_fuel_card',
                    'date_of_issue', 
                    'expiry_date', 
                    'code',
                    'vehicle_restrictions', 
                    'driver_restrictions',
                ),  
            )
        )

class addNewVehicleForm(forms.ModelForm):
    def __init__(self,  *args, **kwargs):
        super(addNewVehicleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)       
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Vehicle Description Details ',             
                
                    Div(
                        'licence_plate',
                        'make_n_model',
                        'model_year',                   
                        'vin_number',                        
                        'color',
                        'signing_mileage',
                        'licence_disk_expiry',                                              
                                             
                        css_class = "col-md-6"),
                    Div(
                        'division',
                        'ownership_type',                       
                        css_class = "col-md-6"),
                    Div('lease_starting',  css_class = "col-md-3"),
                    Div('lease_ending',  css_class = "col-md-3"),
                    Div('rental_starting',  css_class = "col-md-3"),
                    Div('rental_ending',  css_class = "col-md-3"),
                    Div('account_number',css_class = "col-md-6"),
                    Div('insured',  css_class = "col-md-2"),
                    Div('insurer',  css_class = "col-md-4"),
                    Div('has_tracker',  css_class = "col-md-2"),
                    Div('tracker_provider', css_class = "col-md-4"),
                    HTML('<a  href="#vehicle-purchase-details" data-toggle="tab" onclick="newTabToggle()" aria-expanded="true">Next Tab <i class="fa fa-forward" aria-hidden="true"></i></a>'),                
                                        
                       
                    ),
                Tab(
                    'Vehicle Purchase Details ',
                    Div(                        
                        'purchase_date', 
                        'purchase_amount',                      
                        'supplier',
                        'condition', 
                        'status', 
                        'invoice_number', 
                        'warranty_expiry',                         
                        css_class = "col-md-6 outer-div"),
                    Div(
                        'financier', 
                        'on_service_plan', 
                        'on_maintenance_plan', 
                        'plan_provider',
                        'period', 
                        'plan_starting', 
                        'plan_ending', 
                        'mileage_covered',                                  
                        css_class = "col-md-6"),
                    HTML('<a  href="#vehicle-description-details" data-toggle="tab" aria-expanded="true" onclick="newTabToggle()"><i class="fa fa-backward" aria-hidden="true"> Back</i></a>'),             
                    )               
                )
            )

    class Meta:
        model = Vehicle
        fields = '__all__'
        widgets = {
            'licence_disk_expiry': forms.TextInput(attrs={'class': 'datepicker'}),
            'lease_starting': forms.TextInput(attrs={'class': 'datepicker'}),
            'lease_ending': forms.TextInput(attrs={'class': 'datepicker'}),
            'rental_starting': forms.TextInput(attrs={'class': 'datepicker'}),
            'rental_ending': forms.TextInput(attrs={'class': 'datepicker'}),
            'purchase_date': forms.TextInput(attrs={'class': 'datepicker'}),
            'plan_starting': forms.TextInput(attrs={'class': 'datepicker'}),
            'plan_ending': forms.TextInput(attrs={'class': 'datepicker'}),     
        }



class VehicleMakeAndModelForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        TabHolder(
            Tab(
                'Vehicle Description',
                Div(
                    'make_n_model', 'vehicle_class', 'fuel_type', 'engine_capacity','transmission_type',
                    css_class = "col-md-6"
                    ),
                Div(
                    'seats', 'steering', 'doors', 'tank_capacity', 'wheel_size',
                    css_class = "col-md-6"
                    )               
                ),                  
            )
        )
    class Meta:
        model = VehicleMakeAndModel
        fields = '__all__'



class VehicleExtrasForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        TabHolder(
            Tab(
                'Vehicle Description',
                Div(
                    'model_type', 'make_n_model', 'air_conditioner', 'turbo', 'sunroof', 'alloy_wheels',
                    css_class = "col-md-6"
                    ),
                Div(
                    'canopy', 'leather_seats', 'keyless_entry', 'anti_bracking_system', 'airbag', 'dual_airbag',
                    css_class = "col-md-6"
                    ),
                Div(
                    'long_base', 'power_windows', 'power_steering', 'power_mirros', 'anti_theft', 'electronic_fuel_injection',
                    css_class = "col-md-6"
                    )       
                ),                  
            )
        )
    class Meta:
        model = VehicleExtras
        fields = '__all__'

class FuelCardForm(forms.ModelForm):
    class Meta:
        model = FuelCard
        fields ='__all__'

    def __init__(self,  *args, **kwargs):
        super(FuelCardForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Fuel Card Details',

                Div('card_number', 
                    'card_type', 
                    css_class = "col-md-6")
                )
            )

class FuelAllocationForm(forms.ModelForm):
    class Meta:
        model = FuelAllocation
        fields ='__all__'
        widgets = {
            'allocation_date': forms.TextInput(attrs={'class': 'datepicker'}),
        }   

    def __init__(self,  *args, **kwargs):
        user = kwargs.pop('user')
        super(FuelAllocationForm, self).__init__(*args, **kwargs)
        if not user.has_perm('fleet.authorize_fuelallocation'):
            self.fields["authorize"].widget = HiddenInput()  
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Vehicle Allocation Details',


                Div( 
                    'allocation_date', 
                    'transaction_type', 
                    'vehicle', 
                    'driver',                    
                    
                    css_class = "col-md-6"),
                Div(
                    'fuel_card',
                    'balance', 
                    'amount_allocated', 
                    'new_balance',
                    css_class = "col-md-6"),           
                
               
                Div(
                    
                    css_class = "col-md-6"),
               
                Div(
                    'accept',
                    css_class = "col-md-2"),
               
                Div(
                    'authorize',                       
                   
                    css_class = "col-md-2"), 
                 Div(
                  
                    css_class = "col-md-2"), 
            ))

class FuelTransferForm(forms.ModelForm):
    class Meta:
        model = FuelTransfer
        fields ='__all__'
        widgets = {
            'transfer_date': forms.TextInput(attrs={'class': 'datepicker'}),
        }   

    def __init__(self,  *args, **kwargs):
        user = kwargs.pop('user')
        super(FuelTransferForm, self).__init__(*args, **kwargs)
        if not user.has_perm('fleet.authorize_fuelallocation'):
            self.fields["authorize"].widget = HiddenInput()  
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Fuel Transfer Details',
                Div(
                    'from_driver',                                         
                    'from_vehicle',                     
                    'from_fuel_card',
                    'from_balance', 
                    'from_amount_allocated', 
                    'from_new_balance',
                    'transfer_date', 
                    css_class = "col-md-6"),  
               
                Div(
                    'driver',
                    'vehicle', 
                    'to_fuel_card',
                    'to_balance', 
                    'to_amount_allocated', 
                    'to_new_balance',
                    css_class = "col-md-6"),
               
                Div(
                    'accept',
                    css_class = "col-md-2"),
               
                Div(
                    'authorize',                       
                   
                    css_class = "col-md-2"), 
                Div(
                  
                    css_class = "col-md-2"), 
            ))
        self.fields['from_driver'].widget.attrs['onchange'] = 'pop_from_vehicle_info(this)'
        self.fields['from_vehicle'].widget.attrs['onchange'] = 'pop_from_vehicle_info(this)'

        self.fields['driver'].widget.attrs['onchange'] = 'pop_vehicle_info(this)'
        self.fields['vehicle'].widget.attrs['onchange'] = 'pop_vehicle_info(this)'

class VehicleAllocationForm(forms.ModelForm):
    comments = forms.Textarea()
    class Meta:
            model = VehicleAllocation
            fields = '__all__'
            widgets = {
               
                'allocation_date': forms.TextInput(attrs={'class': 'datepicker'}),
            }   
    def __init__(self,  *args, **kwargs):
        user = kwargs.pop('user')
        super(VehicleAllocationForm, self).__init__(*args, **kwargs)
        
        if not user.has_perm('fleet.authorize_vehicleallocation'):
            self.fields["authorize"].widget = HiddenInput()  
        self.helper = FormHelper(self)       
        self.helper.layout = Layout(
            Fieldset(
                'Vehicle Allocation Details',

                Div('vehicle', 
                     'driver',
                    'transaction_type',
                    'allocation_date',                 
                    'mileage',
                    'status',
                    'accept',
                    'authorize',                       
                   
                    css_class = "col-md-4"), 
                 Div(
                    HTML(" {% include 'carallocations.html' %}"),
                    css_class = "col-md-8"), 

                )
            )
        self.fields['driver'].widget.attrs['onchange'] = 'validate_driver(this)'

    def clean_transaction_type(self):
        vehicle = self.cleaned_data.get('vehicle')
        transaction_type = self.cleaned_data.get('transaction_type') 
        last_transaction = VehicleAllocation.objects.filter(vehicle=vehicle).order_by("-allocation_date","-id").first()
        if last_transaction:
            last_transaction_type =last_transaction.transaction_type 
            if not self.instance.pk:
                if transaction_type == last_transaction_type:
                    raise forms.ValidationError("Tansaction repeated choose another transaction type")      
                return self.cleaned_data.get('transaction_type')
            else:
                return self.cleaned_data.get('transaction_type')
        else:
            return self.cleaned_data.get('transaction_type')

    
   

class TransactionsFilterForm(forms.Form):
    region = forms.CharField(widget = forms.TextInput(attrs = {'placeholder' : 'Region', 'class' : 'form-control auto-complete-region'}),required=False,label='Region')
    vehicle = forms.CharField(widget = forms.TextInput(attrs = {'placeholder' : 'Vehicle Registration', 'class' : 'form-control auto-complete-vehicle'}), required=False,label='Licence Plate')
    driver = forms.CharField(widget = forms.TextInput(attrs = {'placeholder' : 'Driver', 'class' : 'form-control auto-complete-driver'}),required=False,label='Driver')
    start_date = forms.DateTimeField(widget = forms.TextInput(attrs = {'placeholder' : 'Start Date','class' : 'form-control datepicker'}),required=False,label='Start Date')
    end_date = forms.DateTimeField(widget = forms.TextInput(attrs = {'placeholder' : 'End Date', 'class' : 'form-control datepicker'}),required=False,label='End Date')

        
    def __init__(self,  *args, **kwargs):
        super(TransactionsFilterForm, self).__init__(*args, **kwargs)
        # self.initial['start_date'] = datetime.now().replace(day=1)
        # self.initial['end_date'] = datetime.now()

    def filter(self,transactions, transactions_date):  
        if self.cleaned_data is not None:
            if self.cleaned_data['vehicle']:
                if transactions_date =='purchase_date' or transactions_date =='licence_disk_expiry':  
                    transactions = transactions.filter(licence_plate__icontains=self.cleaned_data['vehicle'])
                else:
                    vehicle = Vehicle.objects.filter(licence_plate__icontains=self.cleaned_data['vehicle'])
                    transactions = transactions.filter(vehicle=vehicle)

            if self.cleaned_data['driver']:
                term = self.cleaned_data['driver']       
                employee = Employee.objects.filter(first_name__icontains=term)
                if transactions_date =='purchase_date' or transactions_date =='licence_disk_expiry':  
                    transactions = transactions.filter(current_driver=employee)
                else:
                    transactions = transactions.filter(driver=employee)

            if self.cleaned_data['region']:
                term = self.cleaned_data['region']       
                reg = Region.objects.filter(region__icontains=term)
                if transactions_date =='purchase_date' or transactions_date =='licence_disk_expiry':  
                    transactions = transactions.filter(current_driver__branch__region=reg)
                else:
                    transactions = transactions.filter(driver__branch__region=reg)

            if self.cleaned_data['start_date'] and self.cleaned_data['end_date']:
                start_date = self.cleaned_data['start_date']
                end_date = self.cleaned_data['end_date']
                if transactions_date == 'allocation_date':
                    transactions = transactions.filter(allocation_date__range=[start_date, end_date])
                elif transactions_date =='service_date':
                    transactions = transactions.filter(service_date__range=[start_date, end_date])
                elif transactions_date =='purchase_date':
                    transactions = transactions.filter(purchase_date__range=[start_date, end_date])
                elif transactions_date =='log_date':
                    transactions = transactions.filter(log_date__range=[start_date, end_date])
                elif transactions_date =='incident_date':
                    transactions = transactions.filter(incident_date__range=[start_date, end_date])
                elif transactions_date =='renewal_date':
                    transactions = transactions.filter(renewal_date__range=[start_date, end_date])
                elif transactions_date =='licence_disk_expiry':
                    transactions = transactions.filter(licence_disk_expiry__range=[start_date, end_date])
                elif transactions_date =='maint_date':
                    transactions = transactions.filter(maint_date__range=[start_date, end_date])
                elif transactions_date =='claims':
                    transactions = transactions.filter(submission_date__range=[start_date, end_date])
                elif transactions_date =='claims_finalized':
                    transactions = transactions.filter(payout_date__range=[start_date, end_date])
                elif transactions_date =='tf_due_date':
                    transactions = transactions.filter(due_date__range=[start_date, end_date])
                elif transactions_date =='offence_date':
                    transactions = transactions.filter(offence_date__range=[start_date, end_date])
                elif transactions_date =='commented':
                    transactions = transactions.filter(commented__range=[start_date, end_date])    
                elif transactions_date =='transfer_date':
                    transactions = transactions.filter(transfer_date__range=[start_date, end_date])    
        return transactions
                
        
class ServiceBookingForm(forms.ModelForm):
    def __init__(self,  *args, **kwargs):
        super(ServiceBookingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Vehicle Service Booking Details',

                Div(
                    'vehicle', 
                    'driver', 
                    'service_type', 
                    'service_description',                   
                    css_class = "col-md-6"),
                Div(
                    'booking_date', 
                    'service_date', 
                    'garage', 
                    'mileage',
                    'next_service_mileage', 
                    Div('wheel_alignment', css_class = "col-md-6"), 
                    Div('wheel_balancing', css_class = "col-md-6"), 
                    Div('change_cam_belt', css_class = "col-md-6"), 
                    Div('air_con_regass', css_class = "col-md-6"),                   
                    css_class = "col-md-6"),
                )
            )
    class Meta:
        model = ServiceBooking
        fields = '__all__'
        widgets = {
            'booking_date': forms.TextInput(attrs={'class': 'datepicker'}),
            'service_date': forms.TextInput(attrs={'class': 'datepicker'}),
            'service_description': forms.Textarea(attrs={'cols':'40', 'rows':'10'}),      
        }



class TrafficfineForm(forms.ModelForm):    
    def __init__(self,  *args, **kwargs):
        user = kwargs.pop('user')
        super(TrafficfineForm, self).__init__(*args, **kwargs)
        if not user.has_perm('fleet.authorize_trafficfine'):
            self.fields["authorize"].widget = HiddenInput()  
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Vehicle Traffic Fines Details',

                Div(
                    'vehicle', 
                    'driver', 
                    'notice_number',
                    Div('offence_date',css_class = "col-md-6"),
                    Div('offence_time',css_class = "col-md-6"),
                    'due_date',
                    'location', 
                    'conversion_date',                                      
                    css_class = "col-md-6"),
                Div(
                    'description',
                    Div('serious_offence', css_class = "col-md-6"), 
                    Div('awaiting_summons', css_class = "col-md-6" ),
                    Div('court_appearance', css_class = "col-md-6"),
                    Div('court_attended', css_class = "col-md-6" ),
                    'court_date',                   
                    'payment_date',                  
                    css_class = "col-md-6"),
                Div('paid', css_class = "col-md-2" ),
                Div('amount', css_class = "col-md-4"),                 
               
                Div(
                    'accept',
                    css_class = "col-md-2"),
               
                Div(
                    'authorize',                       
                   
                    css_class = "col-md-4"),
                )
            )
            
    class Meta:
        model = Trafficfine
        fields = '__all__'
        widgets = {

            'offence_date':forms.TextInput(attrs={'class': 'datepicker'}),
            'due_date': forms.TextInput(attrs={'class': 'datepicker'}),
            'court_date': forms.TextInput(attrs={'class': 'datepicker'}),
            'payment_date': forms.TextInput(attrs={'class': 'datepicker'}),
            'description': forms.Textarea(attrs={'cols':'40','rows':'4'}),         
        }

class HorizRadioRenderer(forms.RadioSelect.renderer):
    """ this overrides widget method to put radio buttons horizontally
        instead of vertically.
    """
    def render(self):
            """Outputs radios"""
            return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))
 
                         
class MileageLogForm(forms.ModelForm):  
    def __init__(self,  *args, **kwargs):
        super(MileageLogForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
           TabHolder(
                Tab(
                    'Vehicle Inspection Details',
                   
                    Div(
                        'vehicle', 
                        'driver', 
                        'log_date',
                        'start_date', 
                        'end_date',
                        'status',                        
                        css_class = "col-md-6"),
                    Div(
                        'starting_mileage', 
                        'current_mileage', 
                        'mileage', 
                        'fuel_balance_bf',
                        'fuel_used',
                        'fuel_balance',

                        css_class = "col-md-6"),
                     HTML('<a  href="#inspection-check-list" data-toggle="tab" onclick="newTabToggle()" aria-expanded="true">Next Tab <i class="fa fa-forward" aria-hidden="true"></i></a>'),
                   
                   
                    ),
                Tab(
                    'Inspection Check List',
                  
                        Div(
                            'doors',
                            'seats',
                            'body',
                            'tires',
                            'interior',                         
                            
                            css_class = "col-md-4"),
                        Div(
                            'boot',
                            'under_hood',
                            'engine_check',
                            'exhaust_check',
                            'feature_check',
                           
                            css_class = "col-md-4"),
                        Div(
                            'sound_system',
                            'steering',
                            'brakes',
                            'transmission',
                            'overall_feel',
                            css_class = "col-md-4"),                                            
                           
                            HTML('<a href="#vehicle-inspection-details" data-toggle="tab" aria-expanded="true" onclick="newTabToggle()"><i class="fa fa-backward" aria-hidden="true"></i><span>  Back</span></a>'),
                   
                    )
                )
            )
    class Meta:
        model = MileageLog
        fields = '__all__'
        widgets = {
            'log_date': forms.TextInput(attrs={'class': 'datepicker'}),
            'start_date': forms.TextInput(attrs={'class': 'datepicker'}),
            'end_date': forms.TextInput(attrs={'class': 'datepicker'}),           
           
        }

        
class MaintenanceForm(forms.ModelForm):    
    def __init__(self, *args, **kwargs):      
       
        user = kwargs.pop('user')
        super(MaintenanceForm, self).__init__(*args, **kwargs)
        vh = kwargs.pop('instance')
        if not user.has_perm('fleet.authorize_vehiclemaintenance'):
            self.fields["authorize"].widget = HiddenInput()  
        
        self.fields['service_booking_number'].queryset = ServiceBooking.objects.filter(vehicle=vh.vehicle).order_by('-service_date')
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Vehicle Maintenance Details',

                Div(
                    'vehicle', 
                    'driver',                    
                    'maint_date', 
                    'maint_type',
                    'service_booking_number',
                    'invoice_number',
                    'service_provider',                      
                     
                    
                    css_class = "col-md-6"),
                Div(
                    'current_mileage', 
                    'description', 
                    'projected_cost', 
                    'actual_cost', 
                    'difference', 
                    'status',
                    css_class = "col-md-6"),
                Div( css_class = "col-md-6"),

                    
                Div(
                    'accept',
                    css_class = "col-md-2"),
                Div(
                'authorize',
                css_class = "col-md-2"),
               
                Div(                                               
                  
                    css_class = "col-md-2"),                        
                                   
                   
                )
                
            )
    class Meta:
        model = VehicleMaintenance
        fields = '__all__'
        widgets = {
            'maint_date': forms.TextInput(attrs={'class': 'datepicker'}),
            'last_service_date': forms.TextInput(attrs={'class': 'datepicker'}),           
            'description': forms.Textarea(attrs={'cols':'40', 'rows':'4'}),  
            
        }

class RequisitionForm(forms.ModelForm):
    def __init__(self,  *args, **kwargs):
        super(RequisitionForm, self).__init__(*args, **kwargs)
        self.fields["requisition_type"].widget = HiddenInput() 
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Requisition',

                Div(
                    'vehicle',
                    'driver',
                    'requested_by',  
                    'quotation_1', 
                    'quotation_2', 
                    'supplier',                    
                                                                         
                    css_class = "col-md-6"),
                Div(
                    'requisition_type',
                                      
                    'description',
                    'mortivation', 
                    'amount',
                    'budgeted', 
                    'vat_included',                                     
                    css_class = "col-md-6"),
             
                )
            )
    class Meta:
        model = Requisition
        fields = '__all__'
        widgets = {            
            'description': forms.Textarea(attrs={'cols':'40', 'rows':'4'}),
            'mortivation': forms.Textarea(attrs={'cols':'40', 'rows':'4'}),        
        }


class RequisitionItemForm(forms.ModelForm):
    def __init__(self,  *args, **kwargs):
        super(RequisitionItemForm, self).__init__(*args, **kwargs)
        self.fields["requisition_no"].widget = HiddenInput() 
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Requisition Items',

                Div(
                    'requisition_no',
                    'item_code', 
                    'line_item', 
                    'qty', 
                    'unit_price',
                    'line_total',                                     
                    css_class = "col-md-6"),
                Div(
                    HTML(" {% include 'requisitionItems.html' %} "),
                    css_class = "col-md-6")
                
                )
            )
    class Meta:
        model = RequisitionItem
        fields = '__all__'
        widgets = {            
            'description': forms.Textarea(attrs={'cols':'40', 'rows':'10'}),      
        }



class RenewLicenceDiskForm(forms.ModelForm):
    def __init__(self,  *args, **kwargs):
        user = kwargs.pop('user')
        super(RenewLicenceDiskForm, self).__init__(*args, **kwargs)
        if not user.has_perm('fleet.authorize_renewlicencedisk'):
            self.fields["authorize"].widget = HiddenInput() 
        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Fieldset(
                'Vehicle Licencing Details',

                Div(
                    'vehicle', 
                    'driver', 
                    'expiry_date',                                       
                    css_class = "col-md-6"),
                Div(
                    'renewal_date', 
                    'new_expiry_date',
                    'amount',                                         
                    css_class = "col-md-6"),
                
                Div(
                    
                    css_class = "col-md-6"),
               
                Div(
                    'accept',
                    css_class = "col-md-2"),
               
                Div(
                    'authorize',                       
                   
                    css_class = "col-md-2"), 
                 Div(
                  
                    css_class = "col-md-2"), 
                )
            )   
    class Meta:
        model = RenewLicenceDisk
        fields = '__all__'
        widgets = {
            'expiry_date': forms.TextInput(attrs={'class': 'datepicker'}),
            'renewal_date': forms.TextInput(attrs={'class': 'datepicker'}),
            'new_expiry_date': forms.TextInput(attrs={'class': 'datepicker'}),
           
        }


class IncidentForm(forms.ModelForm):
    def __init__(self,  *args, **kwargs):
        super(IncidentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Incidence Description',
                    Div(
                        'vehicle', 
                        'driver', 
                        'incident_date', 
                        'time_of_incident',
                        'location',                         
                                                                     
                        css_class = "col-md-6"
                        ),
                    Div( 
                        'incident_type',
                        'case_number',
                        'date_reported', 
                        'police_station',  
                        'damage_extent',
                        'no_claim',                        
                        css_class = "col-md-6",
                        ),
                     HTML('<a  href="#incidence-damge-description" data-toggle="tab" onclick="newTabToggle()" aria-expanded="true">Next Tab <i class="fa fa-forward" aria-hidden="true"></i></a>'), 
                        
                ),
                Tab(
                    'Incidence Damage Description',
                    Div('Description',),
                    Div(
                        'left_rear_fender', 
                        'left_rear_wheel', 
                        'left_rear_door', 
                        'left_rear_lamp', 
                        'left_rear_window',
                        'left_rear_door_window', 
                        'left_rear_viewmirror', 
                        'left_front_door_window', 
                        'left_front_door', 
                        'left_front_wheel',
                        'left_front_fender', 
                        'left_head_lamp',                       
                        css_class = "col-md-3"
                        ),
                    Div(
                        
                        'right_rear_fender',
                        'right_rear_wheel', 
                        'right_rear_door', 
                        'right_rear_lamp', 
                        'right_rear_window', 
                        'right_rear_door_window',
                        'right_rear_viewmirror', 
                        'right_front_door_window', 
                        'right_front_door', 
                        'right_front_wheel', 
                        'right_front_fender',
                        'right_head_lamp',
                        css_class = "col-md-3"
                        ),
                    Div(
                        'rear_bumper', 
                        'boot_door', 
                        'rear_wind_screen', 
                        'car_top', 
                        'wind_screen',
                        'hood', 
                        'grill', 
                        'front_bumper',
                        'chasis',
                        'suspension',
                        'engine',
                        'gear_box',
                        css_class = "col-md-3"
                        ),
                    Div(
                        'dashboard' ,
                        'dashboard_controls',
                        'sound_system',
                        'Steering',
                        'left_front_seat',
                        'rear_seat',
                        'right_front_seat',
                        'door_panels',
                        'foot_pedals',
                        'hand_brake',
                        'capets',
                        'ceiling',
                         css_class = "col-md-3"
                        ), 
                   
                    HTML('<a  href="#incidence-description" data-toggle="tab" aria-expanded="true" onclick="newTabToggle()"><i class="fa fa-backward" aria-hidden="true"> Back</i></a>'),
                  
                             
                    ),

            )
        )

    class Meta:
        model = Incident
        fields = '__all__'
        widgets = {
            'incident_date': forms.TextInput(attrs={'class': 'datepicker'}),
            'date_reported': forms.TextInput(attrs={'class': 'datepicker'}),
            'time_of_incident': forms.TextInput(attrs={'class': 'timepicker'}),
            'Description': forms.Textarea(attrs={'cols':'40', 'rows':'4'}),
            'recomendations': forms.Textarea(),            
        }

        

class AddInsuranceClaimForm(forms.ModelForm):
    class Meta:
        model = InsuranceClaim
        fields = '__all__'
        widgets = {
            'submission_date': forms.TextInput(attrs={'class': 'datepicker'}),
            'payout_date': forms.TextInput(attrs={'class': 'datepicker'}),
            'sp_payout_date': forms.TextInput(attrs={'class': 'datepicker'}),
           
        }

    def __init__(self,  *args, **kwargs):
        user = kwargs.pop('user')
        super(AddInsuranceClaimForm, self).__init__(*args, **kwargs)
        vh = kwargs.pop('instance')        
        self.fields['incidence_number'].queryset = Incident.objects.filter(vehicle=vh.vehicle).order_by('-id')
        if not user.has_perm('fleet.authorize_insuranceclaim'):
            self.fields["authorize"].widget = HiddenInput() 
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Vehicle Insurance Claims Details',
                Div(
                    'vehicle',
                    'driver', 
                    'incidence_number',                  
                    'submission_date',
                    'claim_number',                    
                   
                    css_class = "col-md-6"
                    ),              
            
                Div(
                   
                    'payout_date',
                    'payout_amount',
                    'sp_payout_date',
                    'sp_payout_amount',
                    'excess',                    
                    css_class = "col-md-6"
                    ),
                
                Div('claim_status',  css_class = "col-md-6"),
                          
                Div('accept', css_class = "col-md-2"),                
                Div('authorize', css_class = "col-md-4"),
                                    
                    
                    

                )                   
            )

