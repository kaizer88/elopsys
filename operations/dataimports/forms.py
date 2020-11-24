from django.conf import settings
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.utils.safestring import mark_safe
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, MultiField, ButtonHolder, Submit, HTML
from crispy_forms.bootstrap import TabHolder, Tab, Div
from django.db.models import Q
from fleet.models import *
from employees.models import *
from datetime import datetime
from django.forms.widgets import HiddenInput

class fileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ('file',)
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': True}),
        }