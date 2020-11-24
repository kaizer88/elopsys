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

class StockItemImportForm(forms.Form):
    stock_item_file = forms.FileField(required=True)

class StockItemForm(forms.ModelForm):

    category = forms.ChoiceField(required = False, label = 'Category',
                                 choices = [('', '--- Select Category ---')] + list(StockItem.STOCK_CATEGORIES))

    class Meta:
        model = StockItem
        exclude = ['deleted', 'created_by', 'modified_by']

    def __init__(self, *args, **kwargs):
        super(StockItemForm, self).__init__(*args, **kwargs)


    def save(self, user, commit=True, *args, **kwargs):
        stock_item = super(StockItemForm, self).save(commit=False)
        stock_item.modified_by = user
        stock_item.created_by = user
        if commit:
            stock_item.save()

        return stock_item

    
class StockTransactionForm(forms.ModelForm):

    stock_item = forms.ModelChoiceField(queryset=StockItem.objects.all(),
                                     label='Stock Item',
                                     required=False,
                                     widget=autocomplete.ListSelect2(url='fleetmanagement:stock_item-autocomplete',
                                                                     attrs={'data-placeholder': '--- Select Stock Item ---'}))
    supplier = forms.ModelChoiceField(queryset=Vendor.objects.filter(vendor_type='dealer'),
                                     label='Supplier',
                                     required=False,
                                     widget=autocomplete.ListSelect2(url='fleetmanagement:vendor_purchase_detail-autocomplete',
                                                                     attrs={'data-placeholder': '--- Select Supplier Name ---'}))

    class Meta:
        model = StockTransaction
        exclude = ['deleted', 'created_by', 'modified_by']

    def __init__(self, *args, **kwargs):
        super(StockTransactionForm, self).__init__(*args, **kwargs)

        self.fields['transaction_date'].widget.attrs['class'] = 'date_time_field'
        self.fields['opening_stock'].widget.attrs['class'] = 'autofill_balance'
        self.fields['opening_stock'].widget.attrs['readonly'] = True
        if self.instance.stock_item:
            self.fields['stock_item'].widget.attrs['readonly'] = True
            self.fields['stock_item'].widget.attrs['disabled'] = True
            self.fields['transaction_type'].widget.attrs['readonly'] = True
            self.fields['transaction_type'].widget.attrs['disabled'] = True


    def clean_stock_item(self):
        stock_item = self.cleaned_data.get('stock_item')
        if self.instance and self.instance.id is None:           
            if stock_item is None:
                raise forms.ValidationError('This field is required')
        return stock_item

    def clean_quantity(self):
        allocation = self.cleaned_data.get('quantity')
        opening_balance = self.cleaned_data.get('opening_stock')
        transaction = self.cleaned_data.get('transaction_type')
        if allocation > opening_balance and transaction=='allocated':
            raise forms.ValidationError('Quantity allocation exceeds available Opening Stock')
        elif allocation <= 0 or allocation is None:
            raise forms.ValidationError('This field is required')

        return allocation

    def clean_opening_stock(self):
        opening_balance = self.cleaned_data.get('opening_stock')
        transaction = self.cleaned_data.get('transaction_type')
        if (opening_balance <= 0 or opening_balance is None) and transaction=='allocated':
            raise forms.ValidationError('Opening Stock must be greater than 0')
        return opening_balance 

    def clean_transaction_type(self):       
        transaction = self.cleaned_data.get('transaction_type')
        if (transaction == "" or transaction is None):
            raise forms.ValidationError('This field is required')
        return transaction

    def clean_supplier(self):
        supplier = self.cleaned_data.get('supplier')        
        transaction = self.cleaned_data.get('transaction_type')
        if (supplier == "" or supplier is None) and transaction=='received':
            raise forms.ValidationError('This field is required')
        return supplier  

    def clean_district(self):
        district = self.cleaned_data.get('district')        
        transaction = self.cleaned_data.get('transaction_type')
        if (district == "" or district is None) and transaction=='allocated':
            raise forms.ValidationError('This field is required')
        return district 


class StockFilterForm(forms.Form):

    stock_item = forms.CharField(required = False)
    
    category = forms.ChoiceField(required = False, label = 'Category',
                                 choices = [('', '--- Select Category ---')] + list(StockItem.STOCK_CATEGORIES))
    
    def __init__(self, *args, **kwargs):
        super(StockFilterForm, self).__init__(*args, **kwargs)

        
    def filter(self, stock_items):
        if self.cleaned_data is not None:
            if self.cleaned_data['stock_item']:
                stock_items = stock_items.filter(item_name__icontains=self.cleaned_data['stock_item'])
            if self.cleaned_data['category']:
                stock_items = stock_items.filter(category=self.cleaned_data['category'])
            
        return stock_items


class StockTransactionFilterForm(forms.Form):

    stock_item = forms.CharField(required = False)
    
    category = forms.ChoiceField(required = False, label = 'Category',
                                 choices = [('', '--- Select Category ---')] + list(StockItem.STOCK_CATEGORIES))
    start_date = forms.DateTimeField(required=False, label='Start date')

    end_date = forms.DateTimeField(required=False, label='End date')

    transaction_type = forms.ChoiceField(required = False, label = 'Category',
                                 choices = [('', '--- Select Transaction Type ---')] + list(StockTransaction.STOCK_TRANSACTION_TYPES))

    district = forms.ChoiceField(required = False, label='District',
                                 choices=[('','--- Select District ---')]+list(Branch.objects.all().values_list('id','description')))
    supplier = forms.CharField(required = False)

    def __init__(self, *args, **kwargs):
        super(StockTransactionFilterForm, self).__init__(*args, **kwargs)
        self.fields['end_date'].widget.attrs['class'] = 'date_field'
        self.fields['start_date'].widget.attrs['class'] = 'date_field'
        self.fields['start_date'].widget.attrs['placeholder'] = 'Start Date'
        self.fields['end_date'].widget.attrs['placeholder'] = 'End Date'

        
    def filter(self, stock_items):
        if self.cleaned_data is not None:

            if self.cleaned_data['stock_item']:
                stock_items = stock_items.filter(stock_item__item_name__icontains=self.cleaned_data['stock_item'])

            if self.cleaned_data['category']:
                stock_items = stock_items.filter(stock_item__category=self.cleaned_data['category'])

            if self.cleaned_data['transaction_type']:
                stock_items = stock_items.filter(transaction_type=self.cleaned_data['transaction_type'])

            if self.cleaned_data['start_date']:
                stock_items = stock_items.filter(transaction_date__gte = self.cleaned_data['start_date'])

            if self.cleaned_data['end_date']:
                stock_items = stock_items.filter(transaction_date__lte = self.cleaned_data['end_date'])

            if self.cleaned_data['district']:
                stock_items = stock_items.filter(district=self.cleaned_data['district'])

            if self.cleaned_data['supplier']:

                suppliers = Vendor.objects.filter(name__icontains=self.cleaned_data['supplier'])\
                                          .values_list('id', flat=True)
                stock_items = stock_items.filter(supplier_id__in=suppliers)
            
        return stock_items


