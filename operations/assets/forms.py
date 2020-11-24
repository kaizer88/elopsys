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


class AssetForm(forms.ModelForm):

    class Meta:
        model = Asset
        exclude = ['created_by','modified_by','deleted','contact_person', 'address', 'asset_detail', 'asset_purchase_detail']

    def __init__(self, *args, **kwargs):
        super(AssetForm, self).__init__(*args, **kwargs)

        self.fields['warranty_expiry'].widget.attrs['class'] = 'date_field'

class AssetFilterForm(forms.Form):

    model = forms.CharField(required = False)
    serial_number = forms.CharField(required = False)
    condition = forms.CharField(required = False)
    status = forms.CharField(required = False)
    condition = forms.ChoiceField(choices=[('', '--- Select Condition ---')]+list(Asset.CONDITION_LIST),required=False)
    status = forms.ChoiceField(choices=[('', '--- Select Status ---')]+list(Asset.STATUS_LIST),required=False)

    def __init__(self, *args, **kwargs):
        super(AssetFilterForm, self).__init__(*args, **kwargs)

    def filter(self, assets):
        if self.cleaned_data is not None:

            if self.cleaned_data['model']:
                    assets = assets.filter(model=self.cleaned_data['model'])

            if self.cleaned_data['serial_number']:
                    assets = assets.filter(serial_number=self.cleaned_data['serial_number'])

            if self.cleaned_data['condition']:
                    assets = assets.filter(condition=self.cleaned_data['condition'])

            if self.cleaned_data['status']:
                    assets = assets.filter(status=self.cleaned_data['status'])

        return assets

class AssetDetailForm(forms.ModelForm):

    class Meta:
        model = AssetDetail
        exclude = ['created_by','modified_by','deleted']

    def __init__(self, *args, **kwargs):
        super(AssetDetailForm, self).__init__(*args, **kwargs)

class AssetPurchaseDetailForm(forms.ModelForm):

    class Meta:
        model = AssetPurchaseDetail
        exclude = ['created_by','modified_by','deleted']

    def __init__(self, *args, **kwargs):
        super(AssetPurchaseDetailForm, self).__init__(*args, **kwargs)

        self.fields['purchase_date'].widget.attrs['class'] = 'date_field'
