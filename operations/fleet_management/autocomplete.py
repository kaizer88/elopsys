import os
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db.models import Count, Sum, Q
import json
import threading

from lib.file_handler import file_download

from models import Vehicle, VehicleTyre, PurchaseDetail, VehicleMaintenance, FinanceDetail
from models import FuelCard, Tracker, Insurance, Branding, VehicleDocument
from models import VehicleDriver, Incident, IncidentDocument

from forms import VehicleForm, VehicleTyreForm, PurchaseDetailForm, FinanceDetailForm
from forms import VehicleMaintenanceForm, FuelCardUsageForm, TrackerForm  #, FuelCardForm
from forms import InsuranceForm, InsuranceForm, BrandingForm, VehicleDocumentForm

from forms import VehicleDriver, VehicleFilterForm, VehicleImportForm, VehicleTyreFormset
from forms import VehicleAssignForm, AddIncidentForm, IncidentFilterForm, TrafficFineForm
from forms import IncidentFileForm, IncidentDocumentForm, VehicleMaintenanceFilterForm
from forms import VehicleDriver, VehicleFilterForm, VehicleImportForm, FuelCardImportForm, VehicleTyreFormset
from forms import FuelCardUsageFilterForm, IncidentForm, DocumentFileForm, PhotoFileForm #, FuelCardFilterForm
from forms import InsuredVehiclesFilterForm, TrafficFineFilterForm, MileageImportForm

from operations.forms import AddressForm, ContactForm, InsurerForm, InsurerFilterForm

from importer import import_vehicle_data, import_fuel_card_data
from exporter import export_vehicle_data, extract_incident_data
from exporter import extract_vehicle_maintenance_data, extract_insurer_vehicles_data, extract_insurers_data

# Create your views here.
from employees.models import *

from operations.models import *

from facilities.models import *

from dal import autocomplete

class VehicleAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        if not self.request.user.is_authenticated():
            return Vehicle.objects.none()

        qs = Vehicle.objects.all().order_by('registration_number')

        if self.q:
            qs = qs.filter(registration_number__istartswith=self.q)

        return qs 


class DriverAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        if not self.request.user.is_authenticated():
            return Employee.objects.none()

        qs = Employee.objects.all().order_by('first_name','last_name')

        if self.q:
            qs = qs.filter(Q(first_name__icontains=self.q) |
                           Q(last_name__icontains=self.q))

        return qs 

class FuelCardAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        
        if not self.request.user.is_authenticated():
            return FuelCard.objects.none()

        vehicle_id = self.forwarded.get('vehicle_id', None)

        if vehicle_id:
            qs = FuelCard.objects.filter(vehicle_assigned__id=vehicle_id).order_by('card_number')
        else:
            qs = FuelCard.objects.all().order_by('card_number')

        if self.q:
            qs = qs.filter(card_number__icontains=self.q)

        return qs 

class VendorTrackerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        if not self.request.user.is_authenticated():
            return Vendor.objects.none()

        qs = Vendor.objects.filter(vendor_type='tracker')

        if self.q:
            qs = qs.filter(Q(name__icontains=self.q))

        return qs 

class VendorPurchaseDetailAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        if not self.request.user.is_authenticated():
            return Vendor.objects.none()

        qs = Vendor.objects.filter(vendor_type='dealer')

        if self.q:
            qs = qs.filter(Q(name__icontains=self.q))

        return qs 

class VendorFuelCardSupplierAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        if not self.request.user.is_authenticated():
            return Vendor.objects.none()

        qs = Vendor.objects.filter(vendor_type='fuel card supplier')

        if self.q:
            qs = qs.filter(Q(name__icontains=self.q))

        return qs 
        
class VendorServiceMaintenanceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        if not self.request.user.is_authenticated():
            return Vendor.objects.none()

        qs = Vendor.objects.filter(vendor_type='service provider')

        if self.q:
            qs = qs.filter(Q(name__icontains=self.q))

        return qs 

class VendorInsuranceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        if not self.request.user.is_authenticated():
            return Vendor.objects.none()

        qs = Vendor.objects.filter(vendor_type='insurance')

        if self.q:
            qs = qs.filter(Q(name__icontains=self.q))

        return qs 

class StockItemAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        if not self.request.user.is_authenticated():
            return StockItem.objects.none()

        qs = StockItem.objects.all()

        if self.q:
            qs = qs.filter(Q(item_name__icontains=self.q))

        return qs 
