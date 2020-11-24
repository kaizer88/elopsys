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


class ElectricityMeterNumberForm(forms.ModelForm):
    class Meta:
        model = ElectricityMeterNumber
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):        
       
        super(ElectricityMeterNumberForm, self).__init__(*args, **kwargs)
          
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Electricity Meter Number Details',

                 Div(
                    'branch', 
                    'meter_number', 
                    'meter_type', 
                    'service_provider',                                                                                                      
                    css_class = "col-sm-6"
                    ),  
                )
            )


class ElectricityPurchaseForm(forms.ModelForm):
    class Meta:
        model = ElectricityPurchase
        fields = '__all__'
        widgets = {
            'purchase_date': forms.TextInput(attrs={'class': 'datepicker'}),          
                      
        } 
    
    def __init__(self, *args, **kwargs):        
        user = kwargs.pop('user')
        super(ElectricityPurchaseForm, self).__init__(*args, **kwargs)
        instance = kwargs.pop('instance')
        if not user.has_perm('fleet.authorize_vehiclemaintenance'):
            self.fields["authorize"].widget = HiddenInput()  
        
        # self.fields['service_booking_number'].queryset = ServiceBookings.objects.filter(vehicle=instance.vehicle)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Property Lease Agreement Details',

                Div(
                    'meter_number',                                    
                    'purchase_date', 
                    'amount',                   
                    'token',
                    
                    css_class = "col-sm-6"),
                
                Div( css_class = "col-sm-6"),
                    
                Div(
                    'accept',
                    css_class = "col-sm-2"),

                Div(
                'authorize',
                css_class = "col-sm-4"),
               
             
                )
            )


class TelcomPABXContractForm(forms.ModelForm):
    class Meta:
        model = TelcomPABXContract
        fields = '__all__'
        widgets = {
            'start_date': forms.TextInput(attrs={'class': 'datepicker'}), 
            'expiry_date': forms.TextInput(attrs={'class': 'datepicker'}), 
        } 
    
    def __init__(self, *args, **kwargs):   
       
        user = kwargs.pop('user')
        super(TelcomPABXContractForm, self).__init__(*args, **kwargs)
        vh = kwargs.pop('instance')
        if not user.has_perm('fleet.authorize_vehiclemaintenance'):
            self.fields["authorize"].widget = HiddenInput()  
        
        # self.fields['service_booking_number'].queryset = ServiceBookings.objects.filter(vehicle=vh.vehicle)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Telcom PABX Contract Details',

                Div(
                    'branch',                                    
                    'start_date', 
                    'expiry_date',                   
                    'extensions',
                    'price',                 
                    css_class = "col-sm-6"),
               
                Div( css_class = "col-sm-6"),
                    
                Div(
                    'accept',
                    css_class = "col-sm-2"),

                Div(
                'authorize',
                css_class = "col-sm-4"),
               
               
                )
            )


class TelcomPABXContractRenewalForm(forms.ModelForm):
    class Meta:
        model = TelcomPABXContractRenewal
        fields = '__all__'
        widgets = {
            'maint_date': forms.TextInput(attrs={'class': 'datepicker'}),     
           
            'description': forms.Textarea(attrs={'cols':'40', 'rows':'4'}),
        } 
    
    def __init__(self, *args, **kwargs):   
       
        user = kwargs.pop('user')
        super(TelcomPABXContractRenewalForm, self).__init__(*args, **kwargs)
        vh = kwargs.pop('instance')
        if not user.has_perm('fleet.authorize_vehiclemaintenance'):
            self.fields["authorize"].widget = HiddenInput()  
        
        # self.fields['service_booking_number'].queryset = ServiceBookings.objects.filter(vehicle=vh.vehicle)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Telkom PABX Contract Renewal Details',

                Div(
                    'branch',                                    
                    'date_expired', 
                    'start_date',                   
                    'expiry_date',
                    'extensions',
                    'price',
                    css_class = "col-sm-6"),
               
                Div( css_class = "col-sm-6"),
                    
                Div(
                    'accept',
                    css_class = "col-sm-2"),

                Div(
                'authorize',
                css_class = "col-sm-4"), 
                )
            )


class MobilePurchaseForm(forms.ModelForm):
    class Meta:
        model = MobilePurchase
        fields = '__all__'
        widgets = {
            'purchase_date': forms.TextInput(attrs={'class': 'datepicker'}),            
            
        } 
    
    def __init__(self, *args, **kwargs):        
        user = kwargs.pop('user')
        super(MobilePurchaseForm, self).__init__(*args, **kwargs)
        instance = kwargs.pop('instance')
        if not user.has_perm('fleet.authorize_vehiclemaintenance'):
            self.fields["authorize"].widget = HiddenInput()  
        # self.fields['phone_number'].queryset = Branches.objects.filter(branch=instance.branch)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Mobile Purchase Details',

                 Div(
                    'branch', 
                    'purchase_date', 
                    'mobile_option', 
                    'service_provider',
                    'phone_number', 
                    'units',
                    'price',                                                                                      
                    css_class = "col-sm-6"
                    ),
                
                Div( css_class = "col-sm-6"),
                    
                Div(
                    'accept',
                    css_class = "col-sm-2"),

                Div(
                'authorize',
                css_class = "col-sm-4"),
                )
            )



class OfficeInspectionForm(forms.ModelForm):
    class Meta:
        model = OfficeInspection
        fields = '__all__'
        widgets = {
            'date_checked': forms.TextInput(attrs={'class': 'datepicker'}),            
            
        } 
    
    def __init__(self, *args, **kwargs):        
        user = kwargs.pop('user')
        super(OfficeInspectionForm, self).__init__(*args, **kwargs)
        instance = kwargs.pop('instance')
        if not user.has_perm('fleet.authorize_vehiclemaintenance'):
            self.fields["authorize"].widget = HiddenInput()  
        self.fields['floor'].queryset = Floor.objects.filter(branch=instance.branch)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Property Inspection Details',

                 Div(
                    'branch', 
                    'floor', 
                    'section', 
                    'date_checked',
                    'time_checked', 
                    'inspector',
                    'status',                                                                                      
                    css_class = "col-sm-6"
                    ),
                Div(  
                    HTML('<h4>Check List</h4>'),                      
                    'walls_and_covering',
                    'windows_and_handles',
                    'blinds', 
                    'ceiling',  
                    'lights_and_switches',
                    'doors_and_handles',
                    'air_conditioner',
                    'furniture',
                    'fire_extinguisher', 
                    'white_board',  
                    'overhead_projector',
                    'appliances',
                    'shelving',
                    css_class = "col-sm-6"
                    ),      
                
                Div( css_class = "col-sm-6"),
                    
                Div(
                    'accept',
                    css_class = "col-sm-2"),

                Div(
                'authorize',
                css_class = "col-sm-4"),
               
                )
            )


class ToiletInspectionForm(forms.ModelForm):
    class Meta:
        model = ToiletInspection
        fields = '__all__'
        widgets = {
            'date_checked': forms.TextInput(attrs={'class': 'datepicker'}),            
            
        } 
    
    def __init__(self, *args, **kwargs):        
        user = kwargs.pop('user')
        super(ToiletInspectionForm, self).__init__(*args, **kwargs)
        instance = kwargs.pop('instance')
        if not user.has_perm('fleet.authorize_vehiclemaintenance'):
            self.fields["authorize"].widget = HiddenInput()  
        self.fields['floor'].queryset = Floor.objects.filter(branch=instance.branch)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Property Toilet Inspection Details',

                 Div(
                    'branch', 
                    'floor', 
                    'toilet', 
                    'date_checked',
                    'time_checked', 
                    'inspector',
                    'status',                                                                                      
                    css_class = "col-sm-6"
                    ),
                Div(
                    HTML('<h4>Check List</h4>'),
                     css_class = "col-sm-6"),  
                Div(                                         
                    'walls_and_covering',
                    'windows_and_handles',                    
                    'ceiling',  
                    'lights_and_switches',
                    'doors_and_handles',
                    'air_extractor',
                    'furniture',
                    'fire_extinguisher',                   
                    'shelving',
                    css_class = "col-sm-3"
                    ),      
                Div(                                           
                    'seat_and_cover',
                    'urinary',
                    'water_dispenser',                    
                    'washing_basin',
                    'taps',
                    'towel_dispencer',
                    'detegent_dispencer',
                    'mirror',
                    css_class = "col-sm-3"
                    ),
                Div(
                    HTML('<br/><br/><br/><br/><br/>'),
                     css_class = "col-sm-6"),      
                Div( css_class = "col-sm-6"),
                    
                Div(
                    'accept',
                    css_class = "col-sm-2"),

                Div(
                'authorize',
                css_class = "col-sm-4"),
               
                )
            )


class LeaseAgreementForm(forms.ModelForm):
    class Meta:
        model = LeaseAgreement
        fields = '__all__'
        widgets = {
            'lease_expiry_date': forms.TextInput(attrs={'class': 'datepicker'}),
        } 
    
    def __init__(self, *args, **kwargs):        
        user = kwargs.pop('user')
        super(LeaseAgreementForm, self).__init__(*args, **kwargs)
        instance = kwargs.pop('instance')
        if not user.has_perm('fleet.authorize_vehiclemaintenance'):
            self.fields["authorize"].widget = HiddenInput()  
        
        # self.fields['service_booking_number'].queryset = ServiceBooking.objects.filter(vehicle=instance.vehicle)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Property Lease Agreement Details',

                Div(
                    'branch',                                    
                    'current_leasee', 
                    'leasor',                   
                    'contact_person',
                    'lease_expiry_date',
                    'notice_term',
                    'status',                  
                    css_class = "col-sm-6"),

                Div(                    
                    'rental_amount', 
                    'deposit', 
                    HTML('<br/>'),
                    'surety',
                    'surety_deposit',
                    'electricity_deposit', 
                    'electricity',
                    HTML('<br/>'),
                    'exit_clause_sent', 
                     HTML('<br/>'),
                    css_class = "col-sm-6"),

                
                Div( css_class = "col-sm-6"),
                    
                Div(
                    'accept',
                    css_class = "col-sm-2"),

                Div(
                'authorize',
                css_class = "col-sm-4"),
               
             
                )
            )



class PropertyMaintenanceForm(forms.ModelForm):
    class Meta:
        model = PropertyMaintenance
        fields = '__all__'
        widgets = {
            'maint_date': forms.TextInput(attrs={'class': 'datepicker'}),     
           
            'description': forms.Textarea(attrs={'cols':'40', 'rows':'4'}),
        } 
    
    def __init__(self, *args, **kwargs):   
       
        user = kwargs.pop('user')
        super(PropertyMaintenanceForm, self).__init__(*args, **kwargs)
        vh = kwargs.pop('instance')
        if not user.has_perm('fleet.authorize_vehiclemaintenance'):
            self.fields["authorize"].widget = HiddenInput()  
        
        # self.fields['service_booking_number'].queryset = ServiceBooking.objects.filter(vehicle=vh.vehicle)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Property Maintenance Details',

                Div(
                    'branch',                                    
                    'maint_date', 
                    'maintenance_type',                   
                    'invoice_number',
                    'service_provider',
                    'status',
                    css_class = "col-sm-6"),

                Div(                    
                    'description', 
                    'projected_cost', 
                    'actual_cost', 
                    'difference', 
                    
                    css_class = "col-sm-6"),
                
                Div( css_class = "col-sm-6"),
                    
                Div(
                    'accept',
                    css_class = "col-sm-2"),

                Div(
                'authorize',
                css_class = "col-sm-4"),
               
               
                )
            )


class RequisitionForm(forms.ModelForm):
    class Meta:
        model = PFRequisition
        fields = '__all__'
        widgets = {            
            'description': forms.Textarea(attrs={'cols':'40', 'rows':'4'}),  
            'mortivation': forms.Textarea(attrs={'cols':'40', 'rows':'4'}),    
        }  

    def __init__(self,  *args, **kwargs):
        super(RequisitionForm, self).__init__(*args, **kwargs)
        self.fields["requisition_type"].widget = HiddenInput() 
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Requisition',

                Div(
                    'branch',
                    'driver',
                    'requested_by',  
                    'quotation_1', 
                    'quotation_2',
                    'amount',
                    Div(    'vat_included',
                        css_class = "col-sm-6"),
                    Div(    'budgeted', 
                        css_class = "col-sm-6"),
                    css_class = "col-sm-6"),
                
                Div(
                    'requisition_type',
                    'supplier',
                    
                    'description',
                    'mortivation',
                                       
                    css_class = "col-sm-6"),
                )
            )
    
class RequisitionItemForm(forms.ModelForm):
    class Meta:
        model = PFRequisitionItem
        fields = '__all__'
        widgets = {            
            'description': forms.Textarea(attrs={'cols':'40', 'rows':'10'}),      
        }
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
                    css_class = "col-sm-6"),
                Div(
                    HTML(" {% include 'requisitionItems.html' %} "),
                    css_class = "col-sm-6")
                
                )
            )
    

class RenewLeaseForm(forms.ModelForm):
    class Meta:
        model = LeaseAgreementRenewal
        fields = '__all__'
        widgets = {
            'expiry_date': forms.TextInput(attrs={'class': 'datepicker'}),
            'renewal_date': forms.TextInput(attrs={'class': 'datepicker'}),
            'new_expiry_date': forms.TextInput(attrs={'class': 'datepicker'}),
            
        }
    def __init__(self,  *args, **kwargs):
        user = kwargs.pop('user')
        super(RenewLeaseForm, self).__init__(*args, **kwargs)
        if not user.has_perm('fleet.authorize_renewlicencedisk'):
            self.fields["authorize"].widget = HiddenInput() 
        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Fieldset(
                'Office Lease Renewal Details',

                Div(
                    'branch',                     
                    'expiry_date',                                       
                    css_class = "col-sm-6"),
                Div(
                    'renewal_date', 
                    'new_expiry_date',
                    'rental_amount',                                         
                    css_class = "col-sm-6"),
               
                Div(
                    
                    css_class = "col-sm-6"),
               
                Div(
                    'accept',
                    css_class = "col-sm-2"),
               
                Div(
                    'authorize',                       
                   
                    css_class = "col-sm-4"), 
                
                )
            )   
    

class TransactionsFilterForm(forms.Form):
    branch = forms.CharField(widget = forms.TextInput(attrs = {'placeholder' : 'Branch', 'class' : 'form-control auto-complete-branch'}), 
                                required=False,label='Branch')
    
    start_date = forms.DateTimeField(widget = forms.TextInput(attrs = {'placeholder' : 'Start Date','class' : 'form-control datepicker'}),
                                        required=False,label='Start Date')
    end_date = forms.DateTimeField(widget = forms.TextInput(attrs = {'placeholder' : 'End Date', 'class' : 'form-control datepicker'}),
                                    required=False,label='End Date')

        
    def __init__(self,  *args, **kwargs):
        super(TransactionsFilterForm, self).__init__(*args, **kwargs)
        self.initial['start_date'] = datetime.now().replace(day=1)
        self.initial['end_date'] = datetime.now()

    def filter(self,transactions, transactions_date):  
        if self.cleaned_data is not None:
            if self.cleaned_data['branch']:
                branch = Branch.objects.filter(branch__contains=self.cleaned_data['branch']).first()               
                transactions = transactions.filter(branch=branch)

            
            if self.cleaned_data['start_date'] and self.cleaned_data['end_date']:
                start_date = self.cleaned_data['start_date']
                end_date = self.cleaned_data['end_date']
                # if transactions_date == 'allocation_date':
                #     transactions = transactions.filter(allocation_date__range=[start_date, end_date])
                # elif transactions_date =='service_date':
                #     transactions = transactions.filter(service_date__range=[start_date, end_date])
                # elif transactions_date =='purchase_date':
                #     transactions = transactions.filter(purchase_date__range=[start_date, end_date])
                # elif transactions_date =='log_date':
                #     transactions = transactions.filter(log_date__range=[start_date, end_date])
                # elif transactions_date =='incident_date':
                #     transactions = transactions.filter(incident_date__range=[start_date, end_date])
                # elif transactions_date =='renewal_date':
                #     transactions = transactions.filter(renewal_date__range=[start_date, end_date])
                # elif transactions_date =='licence_disk_expiry':
                #     transactions = transactions.filter(licence_disk_expiry__range=[start_date, end_date])
                # elif transactions_date =='maint_date':
                #     transactions = transactions.filter(maint_date__range=[start_date, end_date])
                # elif transactions_date =='claims':
                #     transactions = transactions.filter(submission_date__range=[start_date, end_date])
                # elif transactions_date =='claims_finalized':
                #     transactions = transactions.filter(payout_date__range=[start_date, end_date])
                # elif transactions_date =='tf_due_date':
                #     transactions = transactions.filter(due_date__range=[start_date, end_date])
                # elif transactions_date =='offence_date':
                #     transactions = transactions.filter(offence_date__range=[start_date, end_date])
                # elif transactions_date =='commented':
                #     transactions = transactions.filter(commented__range=[start_date, end_date])    

        return transactions



