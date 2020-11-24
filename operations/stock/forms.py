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
        model = STDocument
        fields = ('file',)
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': True}),
        }

class CommentsForm(forms.ModelForm):
    class Meta:
        model = STComment
        fields = ('comments',)
        widgets = {            
            'comments': forms.Textarea(),
        }


class RequisitionForm(forms.ModelForm):
    class Meta:
        model = STRequisition
        fields = '__all__'
        widgets = {            
            'description': forms.Textarea(attrs={'cols':'40', 'rows':'6'}),      
        }  

    def __init__(self,  *args, **kwargs):
        user = kwargs.pop('user')
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
                    'quote_number',                                                       
                    css_class = "col-sm-6"),
                Div(
                    'requisition_type',
                    'supplier',
                    'description',
                    'vat_included',                   
                    css_class = "col-sm-6"),
                )
            )
    
class RequisitionItemForm(forms.ModelForm):
    class Meta:
        model = STRequisitionItem
        fields = '__all__'
        widgets = {            
            'description': forms.Textarea(attrs={'cols':'40', 'rows':'10'}),      
        }
    def __init__(self,  *args, **kwargs):
        user = kwargs.pop('user')
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


class StockItemForm(forms.ModelForm):
    class Meta:
        model = StockItem
        fields = '__all__'       
    
    def __init__(self, *args, **kwargs): 
        user = kwargs.pop('user') 
        super(StockItemForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Stock Item Details',
                 Div(
                    'item_name', 
                    'item_code', 
                    'category',
                    Submit('save', 'Save & Add'),                                                                                                    
                    css_class = "col-sm-4"
                    ), 
                 Div(
                    HTML(" {% include 'stockItemsList.html' %} "),
                    css_class = "col-sm-8") 
                )
            )



class BranchStockForm(forms.ModelForm):
    class Meta:
        model = BranchStock
        fields = '__all__'
        widgets = {
                      
        } 
    
    def __init__(self, *args, **kwargs):        
        user = kwargs.pop('user')
        super(BranchStockForm, self).__init__(*args, **kwargs)
        instance = kwargs.pop('instance')
        if not user.has_perm('fleet.authorize_vehiclemaintenance'):
            self.fields["authorize"].widget = HiddenInput()  
        
        # self.fields['service_booking_number'].queryset = ServiceBookings.objects.filter(vehicle=instance.vehicle)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Branch Stock Item Details',

                Div(
                    'branch',                 
                    'item',
                    'quantity',
                    'reorder_quantity',
                    Submit('save', 'Save & Add'),
                    css_class = "col-sm-4"),
                Div(
                    HTML(" {% include 'branchStockItems.html' %} "),
                    css_class = "col-sm-8")
                             
                )

            )


class StockTakeForm(forms.ModelForm):
    class Meta:
        model = StockTake
        fields = '__all__'
        widgets = {
            'date_checked': forms.TextInput(attrs={'class': 'datepicker'}),            
            
        } 
    
    def __init__(self, *args, **kwargs):        
        user = kwargs.pop('user')
        super(StockTakeForm, self).__init__(*args, **kwargs)
        instance = kwargs.pop('instance')
        if not user.has_perm('fleet.authorize_vehiclemaintenance'):
            self.fields["authorize"].widget = HiddenInput()  
        self.fields['floor'].queryset = Floor.objects.filter(branch=instance.branch)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Stock Item Details',

                 Div(
                    'branch', 
                    'floor',
                    'item',
                    'quantity', 
                    'date_checked',
                    'time_checked',
                    'checker',
                    Submit('save', 'Save & Add'),
                    css_class = "col-sm-4"
                    ),      
                
                Div(
                    HTML(" {% include 'branchStockItems.html' %} "),
                    css_class = "col-sm-8")
               
                )
            )



class StockReplenishmentForm(forms.ModelForm):
    class Meta:
        model = StockReplenishment
        fields = '__all__'
        widgets = {
            'date_replenished': forms.TextInput(attrs={'class': 'datepicker'}),         
        } 
    
    def __init__(self, *args, **kwargs):        
        user = kwargs.pop('user')
        super(StockReplenishmentForm, self).__init__(*args, **kwargs)
        instance = kwargs.pop('instance')
        if not user.has_perm('fleet.authorize_vehiclemaintenance'):
            self.fields["authorize"].widget = HiddenInput()  
        
        # self.fields['service_booking_number'].queryset = ServiceBookings.objects.filter(vehicle=instance.vehicle)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Branch Stock Replenishment Details',

                Div(
                    'branch',                                    
                    'item', 
                    'quantity',                   
                    'replenisher', 
                    'date_replenished',                   
                    Submit('save', 'Save & Add'),
                    css_class = "col-sm-3"),
                Div(
                    HTML(" {% include 'branchStockItems.html' %} "),
                    css_class = "col-sm-9")
               
             
                )
            )

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'        


class BookReplenishmentForm(forms.ModelForm):
    class Meta:
        model = BookReplenishment
        fields = '__all__'
        widgets = {
            'date_ordered': forms.TextInput(attrs={'class': 'datepicker'}),
            'date_received': forms.TextInput(attrs={'class': 'datepicker'}),         
        } 
    
    def __init__(self, *args, **kwargs):        
        user = kwargs.pop('user')
        super(BookReplenishmentForm, self).__init__(*args, **kwargs)
        instance = kwargs.pop('instance')
        if not user.has_perm('fleet.authorize_vehiclemaintenance'):
            self.fields["authorize"].widget = HiddenInput()  
        
        # self.fields['service_booking_number'].queryset = ServiceBookings.objects.filter(vehicle=instance.vehicle)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Book Replenishment Details',

                Div(
                    'book',                                    
                    'range_from', 
                    'range_to', 
                    'in_stock',                  
                    'quantity', 
                    'date_ordered', 
                    'date_received',  
                    'accept',
                    'authorize',
                    css_class = "col-sm-4"),
                Div(
                    HTML(" {% include 'applicationBooks.html' %} "),
                    css_class = "col-sm-8")
                )
            )

class BookAllocationForm(forms.ModelForm):
    class Meta:
        model = BookAllocation
        fields = '__all__'
        widgets = {
            'date_allocated': forms.TextInput(attrs={'class': 'datepicker'}),         
        } 
    
    def __init__(self, *args, **kwargs):        
        user = kwargs.pop('user')
        super(BookAllocationForm, self).__init__(*args, **kwargs)
        instance = kwargs.pop('instance')
        if not user.has_perm('fleet.authorize_vehiclemaintenance'):
            self.fields["authorize"].widget = HiddenInput()  
        
        # self.fields['service_booking_number'].queryset = ServiceBookings.objects.filter(vehicle=instance.vehicle)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Fieldset(
                'Book Replenishment Details',

                Div(
                    'date_allocated',
                    'regional_admin_manager',
                    'region',
                    'book',                                    
                    'range_from', 
                    'range_to',                   
                    'quantity', 
                    'accept',
                    'authorize',
                    css_class = "col-sm-3"),
                Div(
                    HTML(" {% include 'bookreplenishments.html' %} "),
                    css_class = "col-sm-9")
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
