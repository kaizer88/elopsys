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
from django.db.models import Count, Sum, Q, F, ExpressionWrapper, IntegerField
from django.db.models.functions import Concat
from django.db.models import Value as V
import json
import threading

from lib.file_handler import file_download

from models import Vehicle, VehicleTyre, PurchaseDetail, VehicleMaintenance, FinanceDetail
from models import FuelCard, FuelCardUsage, Tracker, Insurance, Branding, VehicleDocument, ServiceMaintanceDocument
from models import VehicleDriver, Incident, IncidentDocument, ServiceBooking, InsuranceClaimDocument

from forms import VehicleForm, VehicleTyreForm, PurchaseDetailForm, FinanceDetailForm
from forms import VehicleMaintenanceForm, FuelCardUsageForm, TrackerForm, VehicleMakeForm, VehicleModelForm
from forms import InsuranceForm, InsuranceForm, BrandingForm, VehicleDocumentForm, AddFuelCardForm

from forms import VehicleDriver, VehicleFilterForm, VehicleImportForm, FuelCardImportForm, VehicleTyreFormset
from forms import VehicleAssignForm, AddIncidentForm, IncidentFilterForm, TrafficFineForm, InsuranceClaimFileForm
from forms import IncidentFileForm, IncidentDocumentForm, VehicleMaintenanceFilterForm, InsuranceClaimDocumentForm

from forms import VehicleDriver, VehicleFilterForm, VehicleImportForm, VehicleTyreFormset, EditFuelCardUsageForm
from forms import FuelCardUsageFilterForm, FuelUsageFilterForm, IncidentForm, DocumentFileForm, PhotoFileForm, FuelCardUsageListForm
from forms import VehicleMakeFilterForm, VehicleModelFilterForm, TrafficFineDocumentForm, InsuranceClaimFilterForm
from forms import VehicleFuelCardForm, FuelCardFilterForm, InsuranceClaimForm, ServiceMaintanceDocumentForm

from forms import InsuredVehiclesFilterForm, TrafficFineFilterForm, VehicleDriverForm, AddVehicleDriverForm
from forms import AddVehicleMaintenanceForm, AddServiceBookingForm, ServiceBookingFilterForm, ServiceBookingForm
from forms import FuelCardUsageDocumentForm, FuelCardUsageFileForm, FuelCardDocumentForm, FuelCardFileForm

from forms import CommentForm, AssignDriverAuthorizationForm, MileageImportForm, ServiceBookingInvoiceForm
from forms import AdditionalVehicleInformationImportForm, FuelCardImportForm

from operations.forms import AddressForm, ContactForm, InsurerForm, InsurerFilterForm, ServiceProviderForm
from operations.forms import ServiceProviderFilterForm, VendorForm, VendorFilterForm, VendorBankDetailForm

from importer import import_vehicle_data, import_fuel_card_data, import_mileage_data, import_additional_vehicle_information_data, import_fuel_cards_data
from exporter import export_vehicle_data, extract_incident_data, extract_fuel_card_usage_data, extract_fuel_cards
from exporter import extract_vehicle_maintenance_data, extract_insurer_vehicles_data, extract_insurers_data
from exporter import extract_service_booking_data, extract_service_providers_data, extract_vendors_data
from exporter import extract_vehicle_makes_data, extract_vehicle_models_data, extract_fuel_card_usage_summary
from exporter import extract_insurance_claims_data, extract_resolved_service_booking_data, extract_vehicle_service_due_data
from exporter import extract_invoice_service_booking_data

# Create your views here.
from employees.models import *

from operations.models import *

from dal import autocomplete
from datetime import datetime

from django.template import Context
import StringIO
from reportlab.pdfgen import canvas
from xhtml2pdf import pisa
from django.views.generic import View
from io import BytesIO
from django.template.loader import get_template

@login_required
def vehicles(request, template="fleet_management/vehicles.html"):
    context = {}
    filter_form = VehicleFilterForm(request.GET or None)
    district_id = request.user.get_user_district
    region_id = request.user.get_user_region
    is_regional_user = request.user.is_regional_user
    
    if request.user.is_superuser or request.user.is_management:
        vehicles = Vehicle.objects.all()
    elif district_id and is_regional_user:
        vehicles = Vehicle.objects.filter(district__id=district_id)
    elif region_id and is_regional_user: 
        vehicles = Vehicle.objects.filter(region__id=region_id)
    else:
        vehicles = Vehicle.objects.none()

    if u'search' in request.GET or u'extract' in request.GET:

        if filter_form.is_valid():
            vehicles = filter_form.filter(vehicles)

    if u'extract' in request.GET:
        download_thread = threading.Thread(target=export_vehicle_data,
                                           args=(request.user, 'all_vehicles',
                                                 vehicles, filter_form.cleaned_data))
        download_thread.start()
        messages.success(request, 'Your extract has been added to the download queue. Queue processing may take a while. Check your report in downloads.')
        if len(set(filter_form.cleaned_data.values())) > 1:
            context['reset_button'] = True

    context['all_vehicles'] = vehicles
    context['filter_form'] = filter_form

    return render(request, template, context)

@login_required
@csrf_exempt
def get_districts(request, region_id):
    if region_id:
        districts = Branch.objects.filter(region__id=region_id)
    else:
        districts = Branch.objects.all()

    data = []

    for d in districts:
        district = {}
        district['id'] = d.id
        district['label'] = d.code +' - '+ d.description
        district['value'] = d.code +' - '+ d.description
        data.append(district)

    results = json.dumps(data)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)


@login_required
@csrf_exempt
def get_vehicle_models(request, make_id):
    models = VehicleModel.objects.filter(make__id=make_id)
    data = []

    for m in models:
        model = {}
        model['id'] = m.id
        model['label'] = m.model_name
        model['value'] = m.model_name
        data.append(model)

    results = json.dumps(data)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)

@login_required
@csrf_exempt
def get_vehicle_driver(request, vehicle_id):

    transaction_date = request.GET['transaction_date']

    # transaction_date = datetime.strptime(str(request.GET['transaction_date']), '%Y-%m-%d %H:%M')

    vehicledriver = VehicleDriver.objects.filter((Q(vehicle__id = vehicle_id) & \
                                                  Q(start_date__lte=transaction_date)) &\
                                                 (Q(end_date__gte=transaction_date) | \
                                                  Q(end_date=None))) \
                                         .first()

    vehicle_driver = {}
    vehicle_driver['id'] = vehicledriver.driver.id if vehicledriver else ""
    vehicle_driver['label'] = vehicledriver.driver.full_name if vehicledriver else ""
    vehicle_driver['value'] = vehicledriver.driver.full_name if vehicledriver else ""

    results = json.dumps(vehicle_driver)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)

@login_required
@csrf_exempt

def get_vehicle_of_driver(request, driver_id):

    transaction_date = request.GET['transaction_date']

    # transaction_date = datetime.strptime(str(request.GET['transaction_date']), '%Y-%m-%d %H:%M')

    vehicledriver = VehicleDriver.objects.filter((Q(driver__id = driver_id) & \
                                                  Q(start_date__lte=transaction_date)) &\
                                                 (Q(end_date__gte=transaction_date) | \
                                                  Q(end_date=None))) \
                                         .first()

    vehicle_driver = {}
    vehicle_driver['id'] = vehicledriver.vehicle.id if vehicledriver else ""
    vehicle_driver['label'] = vehicledriver.vehicle.registration_number if vehicledriver else ""
    vehicle_driver['value'] = vehicledriver.vehicle.registration_number if vehicledriver else ""

    results = json.dumps(vehicle_driver)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)

def get_vehicle_details(request, vehicle_id):
    if vehicle_id:
        vehicle = Vehicle.objects.get(pk=vehicle_id)

    if vehicle:
        vehicle_details = {}
        vehicle_details['id'] = vehicle.id

        vehicle_details['division'] = vehicle.get_division_display()
        vehicle_details['region'] = "{} - {}".format(vehicle.region.code, vehicle.region.name) if vehicle.region else ""
        vehicle_details['district'] = "{} - {}".format(vehicle.district.code, vehicle.district.description) if vehicle.district else ""
        vehicle_details['ownership'] = vehicle.get_ownership_display()
        vehicle_details['vin_number'] = vehicle.vin_number
        vehicle_details['engine_number'] = vehicle.engine_number
        vehicle_details['colour'] = vehicle.colour
        vehicle_details['make'] = vehicle.make
        vehicle_details['model'] = vehicle.model
        vehicle_details['year_model'] = vehicle.year_model

    results = json.dumps(vehicle_details)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)


def get_vehicle_division(request, vehicle_id):

    transaction_date = request.GET['transaction_date']

    vehicledriver = VehicleDriver.objects.filter((Q(vehicle__id = vehicle_id) & \
                                                  Q(start_date__lte=transaction_date)) &\
                                                 (Q(end_date__gte=transaction_date) | \
                                                  Q(end_date=None))) \
                                         .first()

    vehicle_driver = {}
    vehicle_driver['id'] = vehicledriver.vehicle.id if vehicledriver else ""
    vehicle_driver['label'] = vehicledriver.vehicle.division if vehicledriver else ""
    vehicle_driver['value'] = vehicledriver.vehicle.division if vehicledriver else ""

    results = json.dumps(vehicle_driver)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)

@login_required
@csrf_exempt
def get_vehicle_region(request, vehicle_id):

    transaction_date = request.GET['transaction_date']

    vehicledriver = VehicleDriver.objects.filter((Q(vehicle__id = vehicle_id) & \
                                                  Q(start_date__lte=transaction_date)) &\
                                                 (Q(end_date__gte=transaction_date) | \
                                                  Q(end_date=None))) \
                                         .first()

    vehicle_driver = {}
    vehicle_driver['id'] = vehicledriver.vehicle.id if vehicledriver else ""
    vehicle_driver['label'] = vehicledriver.vehicle.region if vehicledriver else ""
    vehicle_driver['value'] = vehicledriver.vehicle.region if vehicledriver else ""

    results = json.dumps(vehicle_driver)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)

@login_required
@csrf_exempt
def get_vehicle_district(request, vehicle_id):

    transaction_date = request.GET['transaction_date']

    vehicledriver = VehicleDriver.objects.filter((Q(vehicle__id = vehicle_id) & \
                                                  Q(start_date__lte=transaction_date)) &\
                                                 (Q(end_date__gte=transaction_date) | \
                                                  Q(end_date=None))) \
                                         .first()

    vehicle_driver = {}
    vehicle_driver['id'] = vehicledriver.vehicle.id if vehicledriver else ""
    vehicle_driver['label'] = vehicledriver.vehicle.district if vehicledriver else ""
    vehicle_driver['value'] = vehicledriver.vehicle.district if vehicledriver else ""

    results = json.dumps(vehicle_driver)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)

@login_required
@csrf_exempt
def get_vehicle_ownership(request, vehicle_id):

    transaction_date = request.GET['transaction_date']

    vehicledriver = VehicleDriver.objects.filter((Q(vehicle__id = vehicle_id) & \
                                                  Q(start_date__lte=transaction_date)) &\
                                                 (Q(end_date__gte=transaction_date) | \
                                                  Q(end_date=None))) \
                                         .first()

    vehicle_driver = {}
    vehicle_driver['id'] = vehicledriver.vehicle.id if vehicledriver else ""
    vehicle_driver['label'] = vehicledriver.vehicle.ownership if vehicledriver else ""
    vehicle_driver['value'] = vehicledriver.vehicle.ownership if vehicledriver else ""

    results = json.dumps(vehicle_driver)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)


@login_required
@csrf_exempt
def get_vehicle_vin_number(request, vehicle_id):

    transaction_date = request.GET['transaction_date']

    vehicledriver = VehicleDriver.objects.filter((Q(vehicle__id = vehicle_id) & \
                                                  Q(start_date__lte=transaction_date)) &\
                                                 (Q(end_date__gte=transaction_date) | \
                                                  Q(end_date=None))) \
                                         .first()

    vehicle_driver = {}
    vehicle_driver['id'] = vehicledriver.vehicle.id if vehicledriver else ""
    vehicle_driver['label'] = vehicledriver.vehicle.vin_number if vehicledriver else ""
    vehicle_driver['value'] = vehicledriver.vehicle.vin_number if vehicledriver else ""

    results = json.dumps(vehicle_driver)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)

@login_required
@csrf_exempt
def get_vehicle_engine_number(request, vehicle_id):

    transaction_date = request.GET['transaction_date']

    vehicledriver = VehicleDriver.objects.filter((Q(vehicle__id = vehicle_id) & \
                                                  Q(start_date__lte=transaction_date)) &\
                                                 (Q(end_date__gte=transaction_date) | \
                                                  Q(end_date=None))) \
                                         .first()

    vehicle_driver = {}
    vehicle_driver['id'] = vehicledriver.vehicle.id if vehicledriver else ""
    vehicle_driver['label'] = vehicledriver.vehicle.engine_number if vehicledriver else ""
    vehicle_driver['value'] = vehicledriver.vehicle.engine_number if vehicledriver else ""

    results = json.dumps(vehicle_driver)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)

@login_required
@csrf_exempt
def get_vehicle_colour(request, vehicle_id):

    transaction_date = request.GET['transaction_date']

    vehicledriver = VehicleDriver.objects.filter((Q(vehicle__id = vehicle_id) & \
                                                  Q(start_date__lte=transaction_date)) &\
                                                 (Q(end_date__gte=transaction_date) | \
                                                  Q(end_date=None))) \
                                         .first()

    vehicle_driver = {}
    vehicle_driver['id'] = vehicledriver.vehicle.id if vehicledriver else ""
    vehicle_driver['label'] = vehicledriver.vehicle.colour if vehicledriver else ""
    vehicle_driver['value'] = vehicledriver.vehicle.colour if vehicledriver else ""

    results = json.dumps(vehicle_driver)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)

@login_required
@csrf_exempt
def get_vehicle_make(request, vehicle_id):

    transaction_date = request.GET['transaction_date']

    vehicledriver = VehicleDriver.objects.filter((Q(vehicle__id = vehicle_id) & \
                                                  Q(start_date__lte=transaction_date)) &\
                                                 (Q(end_date__gte=transaction_date) | \
                                                  Q(end_date=None))) \
                                         .first()

    vehicle_driver = {}
    vehicle_driver['id'] = vehicledriver.vehicle.id if vehicledriver else ""
    vehicle_driver['label'] = vehicledriver.vehicle.make if vehicledriver else ""
    vehicle_driver['value'] = vehicledriver.vehicle.make if vehicledriver else ""

    results = json.dumps(vehicle_driver)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)

@login_required
@csrf_exempt
def get_vehicle_model(request, vehicle_id):

    transaction_date = request.GET['transaction_date']

    vehicledriver = VehicleDriver.objects.filter((Q(vehicle__id = vehicle_id) & \
                                                  Q(start_date__lte=transaction_date)) &\
                                                 (Q(end_date__gte=transaction_date) | \
                                                  Q(end_date=None))) \
                                         .first()

    vehicle_driver = {}
    vehicle_driver['id'] = vehicledriver.vehicle.id if vehicledriver else ""
    vehicle_driver['label'] = vehicledriver.vehicle.model if vehicledriver else ""
    vehicle_driver['value'] = vehicledriver.vehicle.model if vehicledriver else ""

    results = json.dumps(vehicle_driver)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)

@login_required
@csrf_exempt
def get_vehicle_year_model(request, vehicle_id):

    transaction_date = request.GET['transaction_date']

    vehicledriver = VehicleDriver.objects.filter((Q(vehicle__id = vehicle_id) & \
                                                  Q(start_date__lte=transaction_date)) &\
                                                 (Q(end_date__gte=transaction_date) | \
                                                  Q(end_date=None))) \
                                         .first()

    vehicle_driver = {}
    vehicle_driver['id'] = vehicledriver.vehicle.id if vehicledriver else ""
    vehicle_driver['label'] = vehicledriver.vehicle.year_model if vehicledriver else ""
    vehicle_driver['value'] = vehicledriver.vehicle.year_model if vehicledriver else ""

    results = json.dumps(vehicle_driver)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)

def get_driver_licence(request, vehicle_id):

    transaction_date = request.GET['transaction_date']

    currentdriver = VehicleDriver.objects.filter((Q(vehicle__id = vehicle_id) & \
                                                  Q(start_date__lte=transaction_date)) &\
                                                 (Q(end_date__gte=transaction_date) | \
                                                  Q(end_date=None))).first()

    driverlicence =  currentdriver.driver.driving_licence if currentdriver else ""

    driver_licence = {}
    driver_licence['id'] = driverlicence.id if driverlicence else ""
    driver_licence['label'] = driverlicence.licence_number if driverlicence else ""
    driver_licence['value'] = driverlicence.licence_number if driverlicence else ""

    results = json.dumps(driver_licence)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)

def get_driver_licence_expiry_date(request, vehicle_id):

    transaction_date = request.GET['transaction_date']

    currentdriver = VehicleDriver.objects.filter((Q(vehicle__id = vehicle_id) & \
                                                  Q(start_date__lte=transaction_date)) &\
                                                 (Q(end_date__gte=transaction_date) | \
                                                  Q(end_date=None))).first()

    driverlicence =  currentdriver.driver.driving_licence if currentdriver else ""

    driver_licence = {}
    driver_licence['id'] = driverlicence.id if driverlicence else ""
    driver_licence['label'] = datetime.strftime(driverlicence.expiry_date, '%Y-%m-%d') if driverlicence else ""
    driver_licence['value'] = datetime.strftime(driverlicence.expiry_date, '%Y-%m-%d') if driverlicence else ""

    results = json.dumps(driver_licence)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)

@login_required
@csrf_exempt
def get_vehicle_ownership(request, vehicle_id):

    transaction_date = request.GET['transaction_date']

    vehicledriver = VehicleDriver.objects.filter((Q(vehicle__id = vehicle_id) & \
                                                  Q(start_date__lte=transaction_date)) &\
                                                 (
                                                  Q(end_date=None))) \
                                         .first()

    vehicle_driver = {}
    vehicle_driver['id'] = vehicledriver.vehicle.id if vehicledriver else ""
    vehicle_driver['label'] = vehicledriver.vehicle.ownership if vehicledriver else ""
    vehicle_driver['value'] = vehicledriver.vehicle.ownership if vehicledriver else ""

    results = json.dumps(vehicle_driver)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)

@login_required
@csrf_exempt
def get_vehicle_fuel_card(request, fuel_card_id):

    fuel_card = FuelCard.objects.filter(id=fuel_card_id).first()
    vehicle_fuel_card = {}
    vehicle_fuel_card['id'] = fuel_card.id if fuel_card else ""
    vehicle_fuel_card['label'] = fuel_card.card_number if fuel_card else ""
    vehicle_fuel_card['value'] = fuel_card.card_number if fuel_card else ""


    results = json.dumps(vehicle_fuel_card)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)

@login_required
@csrf_exempt
def get_current_vehicle_driver(request, vehicle_id):

    vehicledriver = VehicleDriver.objects.filter(vehicle__id=vehicle_id,
                                                     end_date=None).first()
    vehicle_driver = {}
    vehicle_driver['id'] = vehicledriver.driver.id if vehicledriver else ""
    vehicle_driver['label'] = vehicledriver.driver.full_name if vehicledriver else ""
    vehicle_driver['value'] = vehicledriver.driver.full_name if vehicledriver else ""


    results = json.dumps(vehicle_driver)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)

def get_service_booking_balances(request, vendor_id):
    if vendor_id:
        vendor = Vendor.objects.get(pk=vendor_id)

    if vendor:
        service_booking_balances = {}
        service_booking_balances['id'] = vendor.id
        service_booking_balances['balances'] = str(vendor.balance)

    results = json.dumps(service_booking_balances)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)

@login_required
@csrf_exempt
def get_current_driver(request, vehicle_id):

    vehicledriver = VehicleDriver.objects.filter(vehicle__id = vehicle_id,end_date=None) \
                                         .last()

    current_driver = {}
    current_driver['id'] = vehicledriver.driver.id if vehicledriver else ""
    current_driver['label'] = vehicledriver.driver.full_name if vehicledriver else ""
    current_driver['value'] = vehicledriver.driver.full_name if vehicledriver else ""
    current_driver['drivers'] = vehicledriver.driver.full_name if vehicledriver else ""

    results = json.dumps(current_driver)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)


@login_required
@csrf_exempt
def new_vehicle_make(request):
    make =  request.POST['make_name']
    if make:
        vmake = VehicleMake(make_name=make)
        vmake.save()
        success = True
    else:
        success = False
    response = json.dumps([{'success': success}])
    return HttpResponse(response, 'application/json')


@login_required
@csrf_exempt
def new_vehicle_model(request, template='fleet_management/edit_vehicle.html'):
    context = {}
    model = request.POST['model_name']
    make = request.POST['vehicle_make']
    if model and make:
        vmake = VehicleMake.objects.get(id=make)
        vmodel = VehicleModel(model_name=model, make=vmake)
        vmodel.save()

    context['vmodel'] = vmodel

    response = render(request, template, context)

    return HttpResponse(json.dumps({'response_content': response.content}))


@login_required
def vehicle_uploads(request, template="fleet_management/vehicle_uploads.html"):
    context = {}

    form = VehicleImportForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        import_vehicle_data(request.user, form.cleaned_data.get('vehicles_file'))

    context['form'] = form

    return render(request, template, context)

@login_required
def authorize_assigned_driver(request, vehicle_id, template="fleet_management/assign_driver_authorization.html", context=None):
    context = context or {}
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    vehicle_driver = VehicleDriver.objects.filter(vehicle__id=vehicle_id, 
                                                  end_date=None, 
                                                  status="pending authorization").first()
    if vehicle_driver:
        vehicle_driver_form = AssignDriverAuthorizationForm(request.POST or None,instance=vehicle_driver, prefix='vehicle_driver')
    else:
        vehicle_driver_form = AssignDriverAuthorizationForm(request.POST or None, prefix='vehicle_driver')
    if u'authorize' in request.POST:
        if request.user.is_management and vehicle_driver:
            vehicle_driver.status = "authorized"
            vehicle_driver.save()
            messages.info(request, "Vehicle Driver assigning authorized successfully")
        else:
            messages.errors(request, "Vehicle Driver assigning not authorized!")

        return redirect(reverse('fleetmanagement:vehicles'))

    context['vehicle_driver'] = vehicle_driver
    context['vehicle_driver_form'] = vehicle_driver_form

    return render(request, template, context)

@login_required
def edit_vehicle(request, vehicle_id=None, document_id=None, template="fleet_management/edit_vehicle.html", context=None):

    context = context or {}
    # incidents = []
    vehicle_driver = []
    vehicle = Vehicle.objects.get(pk=vehicle_id) if vehicle_id else None
    fleet_admin = vehicle.created_by if vehicle else request.user

    vehicle_form = VehicleForm(request.POST or None, instance=vehicle, fleet_admin=request.user)
    vi_document_file_form = DocumentFileForm(request.POST or None, request.FILES or None, prefix="vi_documents")
    ai_document_file_form = DocumentFileForm(request.POST or None, request.FILES or None, prefix="ai_documents")
    make_form = VehicleMakeForm(request.POST or None, prefix="vehicle_make_form")
    model_form = VehicleModelForm(request.POST or None, prefix="vehicle_model_form")

    has_instance = False

    if vehicle:
        # incidents = Incident.objects.filter(vehicle=vehicle)
        has_instance = True

        vehicle_tyres = vehicle.tyres.all()
        vehicle_tyre_formset = VehicleTyreFormset(request.POST or None,
                                          queryset=vehicle.tyres.all(),
                                          prefix='vehicle_tyre_formset')

        positions = ['fr','fl','rr','rl','spare']
        count = 0

        for form in vehicle_tyre_formset:
            form.initial['position'] = positions[count]
            count += 1

        purchase_detail = vehicle.purchase_detail.first() if vehicle and \
                          vehicle.purchase_detail.exists() else PurchaseDetail()
        purchase_detail_form = PurchaseDetailForm(request.POST or None,
                                                  instance=purchase_detail,
                                                  prefix='purchase_detail')

        finance_detail = purchase_detail.finance_detail.first() if purchase_detail and \
                          purchase_detail.finance_detail.exists() else None
        finance_detail_form = FinanceDetailForm(request.POST or None,
                                                instance=finance_detail,
                                                prefix='finance_detail')

        insurance = vehicle.insurance.first() if vehicle and \
                    vehicle.insurance.exists() else Insurance()
        insurance_form = InsuranceForm(request.POST or None, instance=insurance,
                                       prefix='insurance')

        tracker = vehicle.tracker.first() if vehicle and \
                    vehicle.tracker.exists() else Tracker()
        tracker_form = TrackerForm(request.POST or None, instance=tracker,
                                       prefix='tracker')

        branding = vehicle.branding.first() if vehicle and \
                    vehicle.branding.exists() else Branding()
        branding_form = BrandingForm(request.POST or None, instance=branding,
                                       prefix='branding')


        maintenance = vehicle.maintenance_plan.first() if vehicle and vehicle.maintenance_plan.exists() else None
        maintenance_form = VehicleMaintenanceForm(request.POST or None, instance = maintenance, prefix='maintenance')

        service_bookings = vehicle.service_bookings.first() if vehicle and \
                    vehicle.service_bookings.exists() else ServiceBooking()
        service_booking_form = ServiceBookingForm(request.POST or None, instance=service_bookings,
                                       prefix='service_bookings')

        vehicle_driver = VehicleDriver.objects.filter(vehicle=vehicle, end_date=None).first()
        vehicle_driver_form = VehicleDriverForm(request.POST or None, car=vehicle,driver=vehicle_driver, prefix='vehicle_driver')
        add_vehicle_driver_form = AddVehicleDriverForm(request.POST or None,  prefix='vehicle_driver')

        # fuel_card = vehicle.fuel_card.first() if vehicle and \
        #             vehicle.fuel_card.exists() else FuelCard()
        fuel_card = FuelCard.objects.filter(vehicle_assigned=vehicle, cancelled_date=None).first()
        fuel_card_form = VehicleFuelCardForm(request.POST or None, vehicle=vehicle, prefix='fuel_card')

        document_file_form = DocumentFileForm(request.POST or None, request.FILES or None, prefix="documents")
        fuel_card_document_file_form = DocumentFileForm(request.POST or None, request.FILES or None, prefix="fuel_card_documents")
        driver_document_file_form = DocumentFileForm(request.POST or None, request.FILES or None, prefix="driver_documents")
        tyres_document_file_form = DocumentFileForm(request.POST or None, request.FILES or None, prefix="tyres_documents")
        pd_document_file_form = DocumentFileForm(request.POST or None, request.FILES or None, prefix="pd_documents")
        tracker_document_file_form = DocumentFileForm(request.POST or None, request.FILES or None, prefix="tracker_documents")
        branding_document_file_form = DocumentFileForm(request.POST or None, request.FILES or None, prefix="branding_documents")
        sb_document_file_form = DocumentFileForm(request.POST or None, request.FILES or None, prefix="sb_documents")

        photo_file_form = PhotoFileForm(prefix="photos")

        fuel_card_history = FuelCard.objects.filter(vehicle_assigned=vehicle)

        context['vehicle_documents'] = VehicleDocument.objects.filter(vehicle=vehicle).order_by('-created_at')
        context['vi_documents'] = VehicleDocument.objects.filter(vehicle=vehicle, document_type='Vehicle documents').order_by('-created_at')
        context['fuel_card_documents'] = VehicleDocument.objects.filter(vehicle=vehicle, document_type='Fuel card documents').order_by('-created_at')
        context['driver_documents'] = VehicleDocument.objects.filter(vehicle=vehicle, document_type='Driver documents').order_by('-created_at')
        context['tyre_documents'] = VehicleDocument.objects.filter(vehicle=vehicle, document_type='Tyre documents').order_by('-created_at')
        context['pd_documents'] = VehicleDocument.objects.filter(vehicle=vehicle, document_type='Purchase details documents').order_by('-created_at')
        context['tracker_documents'] = VehicleDocument.objects.filter(vehicle=vehicle, document_type='Tracker documents').order_by('-created_at')
        context['branding_documents'] = VehicleDocument.objects.filter(vehicle=vehicle, document_type='Branding documents').order_by('-created_at')
        context['sb_documents'] = VehicleDocument.objects.filter(vehicle=vehicle, document_type='Service booking documents').order_by('-created_at')

        context['purchase_detail_form'] = purchase_detail_form
        context['purchase_detail'] = purchase_detail
        context['insurance'] = insurance
        context['insurance_form'] = insurance_form
        context['vehicle_tyre_formset'] = vehicle_tyre_formset
        context['tracker'] = tracker
        context['tracker_form'] = tracker_form
        context['branding_form'] = branding_form
        context['branding'] = branding
        context['finance_detail_form'] = finance_detail_form

        context['document_file_form'] = document_file_form
        context['fuel_card_document_file_form'] = fuel_card_document_file_form
        context['driver_document_file_form'] = driver_document_file_form
        context['tyres_document_file_form'] = tyres_document_file_form
        context['pd_document_file_form'] = pd_document_file_form
        context['tracker_document_file_form'] = tracker_document_file_form
        context['branding_document_file_form'] = branding_document_file_form
        context['sb_document_file_form'] = sb_document_file_form

        context['photo_file_form'] = photo_file_form
        context['maintenance_form'] = maintenance_form
        context['service_booking_form'] = service_booking_form
#        context['vehicle_driver'] = vehicle_driver
        context['vehicle_driver_form'] = vehicle_driver_form
        context['add_vehicle_driver_form'] = add_vehicle_driver_form
        # context['fuel_card_form'] = fuel_card_form
        context['driver_history'] = VehicleDriver.objects.filter(vehicle=vehicle).order_by('-created_at')
        context['fuel_card_history'] = fuel_card_history
        context['service_history'] = ServiceBooking.objects.filter(vehicle=vehicle).order_by('-created_at')
        context['incidents_history'] = Incident.objects.filter(vehicle=vehicle).exclude(incident_type='tyres').order_by('-created_at')
        context['tyres_history'] = Incident.objects.filter(vehicle=vehicle, incident_type='tyres').order_by('-created_at')
        context['insurance_claims'] = InsuranceClaim.objects.filter(vehicle=vehicle).order_by('-created_at')
        context['own_type'] = vehicle.ownership

    if vehicle_form.is_valid():
        vehicle = vehicle_form.save(request.user)
        vehicle.save()
        vs = VehicleStatus.objects.filter(vehicle=vehicle).order_by('-created_at').first()
        status = vs.status_type if vs else ""
        if not status or status != vehicle.status:
            vehicle_status = VehicleStatus(vehicle=vehicle,
                                         status_type=vehicle.status,
                                         comment="Vehicle status change to %s"%(vehicle.status),
                                         created_by=request.user)
            vehicle_status.save()

        has_errors = False

        if has_instance:
            if request.method == 'POST':
                submitted = request.POST.get('tab','')
                # has_errors = edit_vehicle_form_check(maintenance_form, vehicle, request, has_errors)
                # has_errors = edit_vehicle_form_check(insurance_form, vehicle, request, has_errors)

                if submitted == 'details':
                    file_form = vi_document_file_form
                    document_type = 'Vehicle documents'
                elif submitted == 'extras':
                    file_form = ai_document_file_form
                    document_type = 'Vehicle documents'
                # elif submitted == 'fuel_card':
                #     file_form = fuel_card_document_file_form
                #     document_type = 'Fuel card documents'
                #     has_errors = edit_vehicle_fuel_card(fuel_card_form, vehicle, request.user, has_errors)
                elif submitted == 'vehicle_driver':
                    if request.user.is_regional_user or request.user.is_regional_manager:
                        status='pending authorization'
                    else:
                        status='authorized'

                    file_form = driver_document_file_form
                    document_type = 'Driver documents'                           
                    has_errors = edit_vehicle_driver(request, vehicle_driver_form, file_form, request.user, vehicle, has_errors, status)                 
                elif submitted == 'vehicle_tyre':
                    file_form = tyres_document_file_form
                    document_type = 'Tyre documents'
                    has_errors = edit_vehicle_tyres(vehicle_tyre_formset, tyres_document_file_form, vehicle, has_errors, request.user)
                elif submitted == 'purchase_detail':
                    file_form = pd_document_file_form
                    document_type = 'Purchase details documents'
                    has_errors = edit_vehicle_purchase_details(purchase_detail_form, finance_detail_form, vehicle, request.user, has_errors)
                elif submitted == 'tracker':
                    file_form = tracker_document_file_form
                    document_type = 'Tracker documents'
                    has_errors = edit_vehicle_tracker(tracker_form, vehicle, has_errors, request.user)
                elif submitted == 'branding':
                    file_form = branding_document_file_form
                    document_type = 'Branding documents'
                    has_errors = edit_vehicle_branding(branding_form,vehicle, request.user, has_errors)
                elif submitted == 'service_booking':
                    file_form = sb_document_file_form
                    document_type = 'Service booking documents'
                    has_errors = edit_vehicle_service_booking(request, service_booking_form, vehicle, has_errors, request.user)
                else:
                    file_form = document_file_form
                    document_type = "Vehicle documents"

                has_errors = edit_vehicle_document(file_form, document_type, vehicle, request.user, has_errors)

        if not has_errors:
            return redirect(reverse('fleetmanagement:edit_vehicle',
                                   kwargs={'vehicle_id':vehicle.id}))

    context['vehicle'] = vehicle
    context['vehicle_form'] = vehicle_form
    context['vehicle_driver'] = vehicle_driver
    context['vi_document_file_form'] = vi_document_file_form
    context['ai_document_file_form'] = ai_document_file_form
    context['make_form'] = make_form
    context['model_form'] = model_form


    return render(request, template, context)


def edit_vehicle_form_check(form, vehicle, request, has_errors):
    if form.has_changed() and form.is_valid():
        item = form.save(commit=False)
        item.vehicle = vehicle
        if not item.created_by_id:
            item.created_by_id = request.user.id
        item.modified_by_id = request.user.id
        item.save()
        return has_errors
    elif form.has_changed() and form.errors:
        has_errors = True
    return has_errors

def edit_vehicle_purchase_details(purchase_detail_form, finance_detail_form, vehicle, user, has_errors):
    if purchase_detail_form.has_changed() or finance_detail_form.has_changed():
        if purchase_detail_form.is_valid() and finance_detail_form.is_valid():
            purchase_detail = purchase_detail_form.save(commit=False)
            purchase_detail.vehicle = vehicle

            if not purchase_detail.created_by_id:
                purchase_detail.created_by_id = user.id
            purchase_detail.modified_by_id = user.id
            purchase_detail.save()

            finance = finance_detail_form.save(commit=False)
            finance.purchase_detail = purchase_detail
            if not finance.created_by_id:
                finance.created_by_id = user.id
            finance.modified_by_id = user.id

            if finance.purchase_detail.purchase_type == "cash":
                finance.financier = None

            finance.save()
        if purchase_detail_form.errors or finance_detail_form.errors or has_errors:
            has_errors = True

    return has_errors

def edit_vehicle_tracker(tracker_form, vehicle, has_errors, user):
    if tracker_form.has_changed or tracker_address_form.has_changed() or tracker_contact_person_form.has_changed():

        if tracker_form.is_valid():
            tracker = tracker_form.save(commit=False)
            tracker.vehicle = vehicle

            tracker.save()
        elif (tracker_form.has_changed() and tracker_form.errors) or has_errors:
            has_errors = True

    return has_errors

def edit_vehicle_service_booking(request, service_booking_form, vehicle, has_errors, user):
    if service_booking_form.has_changed:

        if service_booking_form.is_valid():
            service_booking = service_booking_form.save(commit=False)
            service_booking.vehicle = vehicle

            if service_booking.other and not service_booking.comment:
                messages.error(request, "Please enter maintenance descriptive text in the comment field")
                has_errors = True
            else:
                service_booking.save()

        elif (service_booking_form.has_changed() and service_booking_form.errors) or has_errors:
            has_errors = True

    return has_errors

# def edit_vehicle_fuel_card(fuel_card_form, vehicle, user, has_errors):

    # if fuel_card_form.has_changed():
    #     if fuel_card_form.is_valid():
    #         fuel_card = fuel_card_form.save(user, vehicle)
    #     elif fuel_card_form.has_changed() and fuel_card_form.errors:
    #         has_errors = True


    # return has_errors

def edit_vehicle_branding(branding_form, vehicle, user, has_errors):

    if branding_form.has_changed():

        if branding_form.has_changed() and branding_form.is_valid():
            branding = branding_form.save(commit=False)
            branding.vehicle = vehicle

            if not branding.created_by_id:
                branding.created_by_id = user.id
            branding.modified_by_id = user.id
            branding.save()
        elif (branding_form.has_changed() and branding_form.errors) or has_errors:
            has_errors = True

    return has_errors

def edit_vehicle_tyres(vehicle_tyre_formset, tyres_document_file_form, vehicle, has_errors, user):
    if vehicle_tyre_formset.has_changed() and tyres_document_file_form.has_changed():
        if tyres_document_file_form.is_valid():
            for tyre_form in vehicle_tyre_formset:
                if tyre_form.is_valid():
                    tyre = tyre_form.save(commit=False)
                    tyre.vehicle = vehicle
                    if not tyre.created_by_id:
                        tyre.created_by = user
                    tyre.modified_by_id = user.id
                    tyre.save()
                elif tyre_form.errors:
                    has_errrors = True
        else:
            messages.error(request, 'Please upload supporting document(s)')

    return has_errors

def edit_vehicle_driver(request, vehicle_driver_form, file_form, user, vehicle, has_errors, status):

    if user.is_regional_user or user.is_regional_manager:
        if vehicle_driver_form.has_changed() and file_form.has_changed():
            if file_form.is_valid():
                if vehicle_driver_form.is_valid():
                    vehicle_driver = vehicle_driver_form.save(user, vehicle, status)
                    status_type = VehicleStatusType.objects.filter(description="Active").first()
                    comment = "Vehicle was assigned, status changed to %s"%(status_type)

                    if status_type is not None and comment !="" and vehicle:
                        vehicle_status = change_vehicle_status(request, vehicle, status_type, comment)
                elif vehicle_driver_form.has_changed() and vehicle_driver_form.errors:
                    has_errors = True
            else:
                has_errors = True
                messages.error(request, 'Please upload supporting document(s)')
    else:
        if vehicle_driver_form.has_changed():
            if vehicle_driver_form.is_valid():
                vehicle_driver = vehicle_driver_form.save(user, vehicle, status)
                status_type = VehicleStatusType.objects.filter(description="Active").first()
                comment = "Vehicle was assigned, status changed to %s"%(status_type)

                if status_type is not None and comment !="" and vehicle:
                    vehicle_status = change_vehicle_status(request, vehicle, status_type, comment)
            elif vehicle_driver_form.has_changed() and vehicle_driver_form.errors:
                has_errors = True

    return has_errors

def edit_vehicle_document(document_file_form, document_type, vehicle, user, has_errors):

    if document_file_form.has_changed():
        if document_file_form.is_valid():
            document = document_file_form.save(commit=False)
            document.document_name = document.document.name
            document.file_type = 'document'
            document.vehicle = vehicle
            document.vehicle = vehicle
            document.save()
            # if document_type == "":
            #     document_type = document_file_form.cleaned_data['document_type']

            vehicle_documents = VehicleDocument.objects.create(vehicle_id=vehicle.id,
                                                               document_id=document.id,
                                                               created_by_id=user.id,
                                                               document_type = document_type)
        elif document_file_form.has_changed() and document_file_form.errors:
            has_errors = True
    return has_errors

@login_required
def vehicle_dashboard(request, vehicle_id, template="fleet_management/vehicle_dashboard.html"):
    context =  {}

    vehicle = Vehicle.objects.get(pk=vehicle_id)

    vehicle_assign_form = VehicleAssignForm(vehicle=vehicle)
    vehicle = Vehicle.objects.get(pk=vehicle_id)

    incident_form = IncidentForm(request.POST or None)
    incidents = Incident.objects.filter(vehicle_driver__vehicle=vehicle)

    vehicle_fines = incidents.filter(incident_type='traffic fine').order_by('incident_date')
    vehicle_accidents = incidents.filter(Q(incident_type='vehicle theft') | Q(incident_type='windscreen') |
                                        Q(incident_type='smash and grab') | Q(incident_type='road accident')).order_by('incident_date')
    vehicle_speed_warnings = incidents.filter(incident_type='tracker warning').order_by('incident_date')

    context['vehicle'] = vehicle
    context['incident_form'] = incident_form
    context['vehicle_assign_form'] = vehicle_assign_form
    context['incidents'] = incidents
    context['vehicle_fines'] = vehicle_fines
    context['vehicle_accidents'] = vehicle_accidents
    context['vehicle_speed_warnings'] = vehicle_speed_warnings

    return render(request, template, context)

@login_required
def assign_driver(request, vehicle_id):

    vehicle = Vehicle.objects.get(pk=vehicle_id)
    vehicle_assign_form = VehicleAssignForm(request.POST or None, vehicle=vehicle)
    if vehicle_assign_form.is_valid():
        vehicle_driver = vehicle_assign_form.save(commit=False)
        vehicle_driver.vehicle = Vehicle.objects.get(pk=vehicle_id)
        vehicle_driver.created_by_id = request.user.id
        vehicle_driver.save()

    return redirect(reverse('fleetmanagement:vehicle_dashboard', kwargs={"vehicle_id":vehicle_id}))


@login_required
@csrf_exempt
def _load_new_purchase_detail(request, vehicle_id, template='fleet_management/widgets/_purchase_detail.html'):
    context = {}
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    purchase_detail = vehicle.purchase_detail.first() if vehicle and \
                      vehicle.purchase_detail.exists() else None
    purchase_detail_form = PurchaseDetailForm(request.POST or None,
                                              instance=purchase_detail,
                                              prefix='purchase_detail')

    finance_detail = purchase_detail.finance_detail.first() if purchase_detail and \
                      purchase_detail.finance_detail.exists() else None
    finance_detail_form = FinanceDetailForm(request.POST or None,
                                            instance=finance_detail,
                                            prefix='finance_detail')



    context['purchase_detail_form'] = purchase_detail_form
    context['finance_detail_form'] = finance_detail_form

    response = render(request, template, context)

    return HttpResponse(json.dumps({'response_content': response.content}))


@login_required
@csrf_exempt
def _load_new_insurance(request, vehicle_id, template='fleet_management/widgets/insurance.html'):

    context = context or {}
    vehicle = None

    vehicle_form = VehicleForm(request.POST or None, instance=vehicle)

    insurance_form = InsuranceForm(request.POST or None,
                                   instance=vehicle.insurance.first()if vehicle else None)

    context['insurance_form'] = insurance_form

    response = render_to_response(template, context, context_instance=RequestContext(request))

    # return HttpResponse(json.dumps({'response_content': response.content))
@login_required
def edit_fuel_card(request, fuel_card_id=None, template="fleet_management/edit_fuel_card.html", context=None):
    context = context or {}
    fuel_card =  None
    card_documents = None
    documents = None

    if fuel_card_id:
        fuel_card = FuelCard.objects.get(pk=fuel_card_id)
        fuel_card_form = AddFuelCardForm(request.POST or None, instance=fuel_card)
        card_documents = FuelCardDocument.objects.filter(pk=fuel_card_id,
                                                         document_type__description='Card Limit Change')
        documents = Document.objects.all()
    else:
        fuel_card_form = AddFuelCardForm(request.POST or None)

    fuel_card_document_form = FuelCardDocumentForm(request.POST or None, prefix="documents")
    fuel_card_file_form = FuelCardFileForm(request.POST or None, request.FILES or None, prefix="documents")

    if fuel_card_form.is_valid():
        has_errors = False

        if fuel_card_file_form.is_valid():
            document = fuel_card_file_form.save(commit=False)
        if fuel_card_form.has_changed():
            if 'card_limit' in fuel_card_form.changed_data:
                if fuel_card_form.cleaned_data['comment'] is not None and document.document.name is not None:
                    has_errors = False
                else:
                    has_errors = True

        if has_errors:
            messages.error(request, "Cannot save fuel card change, comment & Document upload required for Card Limit Change")
        else:
            fuel_card = fuel_card_form.save(commit=False)
            fuel_card.created_by = request.user
            fuel_card.save()

            if fuel_card_file_form.is_valid():
                document = fuel_card_file_form.save(commit=False)
                document.document_name = document.document.name
                document.file_type = 'document'
                document.description = 'Fuel Card Limit Change Document'
                if document.document_name is not None and fuel_card_document_form.is_valid():
                    document.save()

                    fuel_card_document = fuel_card_document_form.save(commit=False)
                    fuel_card_document.fuel_card = fuel_card
                    fuel_card_document.document = document
                    fuel_card_document.created_by = request.user
                    fuel_card_document.save()
                    fuel_card_document_form.save_m2m()

        if not has_errors:
            return redirect(reverse('fleetmanagement:fuel_cards'))

    context['fuel_card_form'] = fuel_card_form
    context['fuel_card'] = fuel_card
    context['fuel_card_id'] = fuel_card_id
    context['fuel_card_document_form'] = fuel_card_document_form
    context['fuel_card_file_form'] = fuel_card_file_form
    context['card_documents'] = card_documents
    return render(request, template, context)

@login_required
def fuel_cards(request, template="fleet_management/fuel_cards.html", context=None):
    context = context or {}
    fuel_cards = FuelCard.objects.all()

    fuel_card_filter_form = FuelCardFilterForm(request.GET or None)

    if u'search' in request.GET or u'extract' in request.GET:
        if fuel_card_filter_form.is_valid():
            fuel_cards = fuel_card_filter_form.filter(fuel_cards)

    if u'extract' in request.GET:
        download_thread = threading.Thread(target=extract_fuel_cards,
                                               args=(request.user, 'all_fuel_cards', fuel_cards,
                                                     fuel_card_filter_form.cleaned_data))
        download_thread.start()
        messages.success(request, 'Your extract has been added to the download queue. Queue processing may take a while. Check your report in downloads.')

    context['fuel_cards'] = fuel_cards
    context['fuel_card_filter_form'] = fuel_card_filter_form

    return render(request, template, context)

@login_required
def detail_fuel_card_usage(request, fuel_card_id=None, template="fleet_management/detail_fuel_card_usage.html", context=None):
    context = context or {}
    fuel_card_usage = []
    fuel_card_usage_form = FuelCardUsageFilterForm(request.GET or None)
    fuel_card_document_history = []
    reset_button = False
    transaction_types = FuelCardUsageTransactionType.objects.filter(description__in=['FUEL', 'OIL','TOLL-GATE'])
    if fuel_card_id and int(fuel_card_id) > 0:
        fuel_card_usage = FuelCardUsage.objects.filter(fuel_card__id=fuel_card_id,
                                                       transaction_type__in=transaction_types)\
                                               .order_by('-transaction_date').distinct()
    else:
        fuel_card_usage = FuelCardUsage.objects.filter(fuel_card__id__isnull=False,
                                                       transaction_type__in=transaction_types)\
                                               .order_by('-transaction_date').distinct()

    if (u'search'in request.GET, u'extract'in request.GET) and fuel_card_usage_form.is_valid():
        if fuel_card_usage_form.cleaned_data['driver']:
            fuel_card_usage = FuelCardUsage.objects.filter( transaction_type__in=transaction_types)\
                                                   .exclude(fuel_card__id__isnull=True)\
                                                   .order_by('-transaction_date').distinct()
        else:
            fuel_card_usage = FuelCardUsage.objects.filter(fuel_card__id=fuel_card_id,
                                                           transaction_type__in=transaction_types)\
                                                   .order_by('-transaction_date').distinct()
        fuel_card_usage = fuel_card_usage_form.filter(fuel_card_usage)

    total_usage =  fuel_card_usage.aggregate(Sum('amount'))['amount__sum'] or 0

    last_transaction = fuel_card_usage.first()
    if last_transaction:
        if last_transaction.fuel_card.status == 'cancelled':
            available = 0
        else:
            available = last_transaction.fuel_card.balance
    else:
        available = 0

    if fuel_card_usage:
        fuel_card_document_history = FuelCardUsageDocument.objects.filter(fuel_usage=fuel_card_usage.first().fuel_card.id)

    if u'extract'in request.GET and fuel_card_usage_form.is_valid():
        download_thread = threading.Thread(target=extract_fuel_card_usage_data,
                                           args=(request.user,
                                                 'all_fuel_cards',
                                                 fuel_card_usage, total_usage, available,
                                                 fuel_card_usage_form.cleaned_data))
        download_thread.start()
        messages.success(request, 'Your extract has been added to the download queue. Queue processing may take a while. Check your report in downloads.')


    context['reset_button'] = reset_button
    context['total_usage'] = total_usage 
    context['available'] = available
    context['fuel_card_usage'] = fuel_card_usage
    context['fuel_card_usage_form'] = fuel_card_usage_form
    context['fuel_card_id'] = fuel_card_id
    context['fuel_card_document_history'] = fuel_card_document_history
    
    return render(request, template, context)

def current_balance(fuel_card):
    first_of_month = datetime.now().replace(day=1)
    usage =  FuelCardUsage.objects.filter(fuel_card=fuel_card.pk, 
                                          transaction_type__description__in=['FUEL', 'OIL','TOLL-GATE'],
                                          transaction_date__gte=first_of_month,)\
                                  .aggregate(Sum('amount'))['amount__sum'] or 0
    return fuel_card.card_limit - usage

def balance(fuel_card):
    first_of_month = datetime.now().replace(day=1)
    if datetime.now().month == 12:
        last_of_month = datetime.now().replace(day=31)

    else:
        last_of_month = datetime.now().replace(month=datetime.now().month+1, day=1) - timedelta(days=1)

    usage =  FuelCardUsage.objects.filter(fuel_card=fuel_card.pk,
                                          transaction_type__description__in=['FUEL', 'OIL','TOLL-GATE'], 
                                          transaction_date__gte=first_of_month,)\
                                  .aggregate(Sum('amount'))['amount__sum'] or 0

    last_fuel_card = fuel_card.previous_fuel_card()

    if last_fuel_card and fuel_card.start_date.date() >= first_of_month.date():
        return last_fuel_card.fuel_card_usage.last().current_balance - usage

    elif fuel_card.status == 'cancelled':
        return 0

    else:
        return fuel_card.current_balance

@login_required
def fuel_card_usage(request, template="fleet_management/fuel_card_usage.html"):
    context = {}
    fuel_card_usage_form = FuelUsageFilterForm(request.GET or None)
    reset_button = False
    date_from = datetime.today().replace(day=1)
    date_to   = datetime.today()

    fuel_card_usage = FuelCardUsage.objects.filter(transaction_type__description__in=['FUEL', 'OIL','TOLL-GATE'],
                                                   transaction_date__gte=date_from,
                                                   transaction_date__lte=date_to)\
                                           .exclude(fuel_card__id__isnull=True)

    if u'search'in request.GET or u'extract' in request.GET:
        fuel_card_usage = FuelCardUsage.objects.filter(transaction_type__description__in=['FUEL', 'OIL','TOLL-GATE'])\
                                               .exclude(fuel_card__id__isnull=True)
        if fuel_card_usage_form.is_valid():

            date_from = fuel_card_usage_form.cleaned_data['date_from'] if (fuel_card_usage_form.cleaned_data['date_from'] and fuel_card_usage_form.cleaned_data['date_from'] is not None) else date_from
            date_to = fuel_card_usage_form.cleaned_data['date_to'] if (fuel_card_usage_form.cleaned_data['date_to'] and fuel_card_usage_form.cleaned_data['date_to'] is not None) else date_to
            date_type = fuel_card_usage_form.cleaned_data['date_type']
            driver = fuel_card_usage_form.cleaned_data['driver']
            vehicle = fuel_card_usage_form.cleaned_data['vehicle']
            card = fuel_card_usage_form.cleaned_data['card_number']

            if driver:
                drivers =  Employee.objects.annotate(driver_full_name=Concat('first_name', V(' '), 'last_name'))\
                                           .filter(Q(driver_full_name__icontains=driver)|
                                                   Q(first_name__icontains=driver)|
                                                   Q(last_name__icontains=driver))\
                                           .values_list('id', flat=True)
                fuel_card_usage = fuel_card_usage.filter(driver__id__in=drivers)
            
            if date_type == 'transacted':
                if date_from and date_to:
                    fuel_card_usage = fuel_card_usage.filter(transaction_date__range=(date_from.date(),date_to.date()))
            else:
                if date_from and date_to:
                    fuel_card_usage = fuel_card_usage.filter(created_at__range=(date_from,date_to))

            if vehicle:
                vehicles = Vehicle.objects.filter(registration_number__icontains=vehicle)\
                                          .values_list('id', flat=True)
                fuel_card_usage = fuel_card_usage.filter(vehicle__id__in=vehicles)

            if card:
                cards = FuelCard.objects.filter(card_number__icontains=card)\
                                          .values_list('id', flat=True)
                fuel_card_usage = fuel_card_usage.filter(fuel_card__id__in=cards)
            
    fuel_card_usage = fuel_card_usage.values('fuel_card__id',
                                             'fuel_card__card_number',
                                             'fuel_card__status',
                                             'fuel_card__card_limit',
                                             'vehicle__id',
                                             'vehicle__registration_number',
                                             'driver__id',
                                             'driver__first_name',
                                             'driver__last_name')\
                                     .annotate(sum_amount=Sum('amount'))\
                                     .order_by('-sum_amount')

    total_usage =  fuel_card_usage.aggregate(Sum('amount'))['amount__sum'] or 0

    if u'extract' in request.GET:

        download_thread = threading.Thread(target=extract_fuel_card_usage_summary,
                                           args=(request.user, 'all_fuel_cards', fuel_card_usage, total_usage,
                                                 fuel_card_usage_form.cleaned_data))
        download_thread.start()
        messages.success(request, 'Your extract has been added to the download queue. Queue processing may take a while. Check your report in downloads.')

    context['date_from'] = str(date_from.date())
    context['date_to'] = str(date_to.date())
    context['total_usage'] = total_usage
    context['reset_button'] = reset_button
    context['fuel_card_usage'] = fuel_card_usage
    context['fuel_card_usage_form'] = fuel_card_usage_form

    return render(request, template, context)

@login_required
def edit_fuel_card_usage(request,  fuel_card_id=None, template="fleet_management/edit_fuel_card_usage.html", context=None):

    context = context or {}
    fuel_card_usage = None
    use_type = None
    usage_documents = None
    documents = None

    if fuel_card_id:
        try:
            fuel_card_usage = FuelCardUsage.objects.get(pk=fuel_card_id,fuel_card__id__isnull=False)
        except FuelCardUsage.DoesNotExist:
            fuel_card_usage = None
        fuel_card_usage_form = EditFuelCardUsageForm(
            request.POST or None, instance=fuel_card_usage)
        if fuel_card_usage:
            usage_documents = FuelCardUsageDocument.objects.filter(fuel_usage=fuel_card_usage.fuel_card.id,document_type__description__in=['Proof Of Payment','Fuel Slips'])
            documents = Document.objects.all()
        has_instance = True
    else:
        fuel_card_usage_form = EditFuelCardUsageForm(request.POST or None)
        has_instance = False

    fuel_usage_document_form = FuelCardUsageDocumentForm(request.POST or None, prefix="documents")
    fuel_usage_file_form = FuelCardUsageFileForm(request.POST or None, request.FILES or None, prefix="documents")

    if fuel_card_usage_form.is_valid():

        has_errors = False
        no_driver_allocation = False
        fuel_card_usage = fuel_card_usage_form.save(commit=False)
        fuel_card_usage.created_by = request.user
        fuel_card_usage.usage_type = 'manual'
        if has_instance:
            fuel_card = fuel_card_usage.fuel_card
        else:
            fuel_card = FuelCard.objects.filter(vehicle_assigned=fuel_card_usage.vehicle, cancelled_date=None).first()

        if fuel_card:
            fuel_card_usage.fuel_card = fuel_card
        else:
            has_errors = True
            messages_text = 'Fuel Card not assigned to a vehicle.'
        
        if not fuel_card_usage.driver:
            if fuel_usage_file_form.is_valid():
                document = fuel_usage_file_form.save(commit=False)

            if fuel_card_usage.comment and document.document.name is not None:
                has_errors = False
                no_driver_allocation = True

            else:
                has_errors = True
                messages_text = 'Comments & Document upload required when no Driver is selected.'

        if not no_driver_allocation:
            if fuel_card_usage.vehicle:
                driver = VehicleDriver.objects.filter((Q(vehicle = fuel_card_usage.vehicle) & \
                                                       Q(start_date__lte=fuel_card_usage.transaction_date)) &\
                                                      (Q(end_date__gte=fuel_card_usage.transaction_date) | \
                                                       Q(end_date=None))) \
                                              .first()
                if driver:
                    fuel_card_usage.driver = driver.driver

                else:
                    has_errors = True
                    messages_text = 'Cannot save fuel usage transaction, no Vehicle Allocation on the provided Date Used.'
            else:
                has_errors = True
                messages_text = 'Cannot save fuel usage transaction, no Vehicle Allocation on the provided Date Used.'


        if has_errors:
            messages.error(request, messages_text)

        else:
            fuel_card_usage.save()
            fuel_card_usage_form.save_m2m()

            if fuel_usage_file_form.is_valid():
                document = fuel_usage_file_form.save(commit=False)
                document.document_name = document.document.name
                document.file_type = 'document'
                document.description = 'fuel card usage document'

                if document.document_name is not None and fuel_usage_document_form.is_valid():
                    document.save()

                    fuel_usage_document = fuel_usage_document_form.save(commit=False)
                    fuel_usage_document.fuel_usage = fuel_card_usage.fuel_card
                    fuel_usage_document.document = document
                    fuel_usage_document.created_by = request.user
                    fuel_usage_document.save()
                    fuel_usage_document_form.save_m2m()

                    return redirect(reverse('fleetmanagement:detail_fuel_card_usage', kwargs={"fuel_card_id":fuel_card_usage.fuel_card.id}))
                else:
                    return redirect(reverse('fleetmanagement:detail_fuel_card_usage', kwargs={"fuel_card_id":fuel_card_usage.fuel_card.id}))
            else:
                return redirect(reverse('fleetmanagement:detail_fuel_card_usage', kwargs={"fuel_card_id":fuel_card_usage.fuel_card.id}))

            return redirect(reverse('fleetmanagement:detail_fuel_card_usage', kwargs={"fuel_card_id":fuel_card_usage.fuel_card.id}))

    context['fuel_card_usage_form'] = fuel_card_usage_form
    context['fuel_card_usage'] = fuel_card_usage
    context['fuel_usage_file_form'] = fuel_usage_file_form
    context['fuel_usage_document_form'] = fuel_usage_document_form
    context['usage_documents'] = usage_documents
    context['fuel_card_id'] = fuel_card_id
    return render(request, template, context)

@login_required
def fuel_card_uploads(request, template="fleet_management/fuel_card_uploads.html"):
    context = {}

    form = FuelCardImportForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        import_thred = threading.Thread(target=import_fuel_card_data,
                                        args=(request.user,
                                              form.cleaned_data.get('fuel_card_file')))
        import_thred.start()
        messages.success(request, 'Your import file is being processed in the background. Queue processing may take a while.')

    context['form'] = form

    return render(request, template, context)


@login_required
def view_incident(request, incident_id, template="fleet_management/view_incidents.html"):
    context =  {}
    incident = Incident.objects.get(pk=incident_id)

    context['incident'] = incident

    return render(request, template, context)

@login_required
def add_incident(request, vehicle_driver_id, template="fleet_management/add_incident.html", context=None):

    context = context or {}
    vehicle_driver = VehicleDriver.objects.get(pk=vehicle_driver_id)
    vehicle = vehicle_driver.vehicle

    incident_form = IncidentForm(request.POST or None)

    if request.POST:

        if incident_form.is_valid():

            incident = incident_form.save(commit=False)
            incident.created_by_id = request.user.id
            incident.vehicle_driver_id = vehicle_driver.id
            if vehicle_driver:
                incident.driver = vehicle_driver.driver
            incident.save()

            messages.info(request, 'incident added')

        return redirect(reverse('fleetmanagement:vehicle_dashboard', kwargs={"vehicle_id":vehicle.id}))

    context['incident_form'] = incident_form

    return render(request, template, context)

@login_required
def view_incidents(request, template="fleet_management/view_incidents.html"):
    context = {}
    incidents = Incident.objects.all().order_by('incident_date').reverse()
    filter_form = IncidentFilterForm(request.POST or None)

    if u'search' in request.POST or u'extract' in request.POST:
        if filter_form.is_valid():
            incidents = filter_form.filter(incidents)

    if u'extract' in request.POST:
        if filter_form.is_valid():
            download_thread = threading.Thread(target=extract_incident_data,
                                               args=(request.user,
                                                     incidents, filter_form.cleaned_data))
            download_thread.start()
            messages.success(request, 'Your extract has been added to the download queue. Queue processing may take a while. Check your report in downloads.')


    context['incidents'] = incidents
    context['filter_form'] = filter_form

    return render(request, template, context)

@login_required
def vehicle_summary(request, vehicle_id, template="fleet_management/vehicle_summary.html"):
    context = {}

    vehicle = Vehicle.objects.get(pk=vehicle_id)
    incidents = Incident.objects.filter(vehicle_driver__vehicle=vehicle)
    vehicle_tire = VehicleTyre.objects.filter(vehicle = vehicle, in_use = True)
    purchase_detail = PurchaseDetail.objects.filter(vehicle=vehicle).first()
    financial_detail = None
    if purchase_detail:
        financial_detail = FinanceDetail.objects.filter(purchase_detail=purchase_detail).first()
    fuel_card = FuelCard.objects.filter(vehicle=vehicle).first()
    insurance = Insurance.objects.filter(vehicle=vehicle).first()
    tracker = Tracker.objects.filter(vehicle=vehicle, active=True).first()
    branding = Branding.objects.filter(vehicle=vehicle).first()
    vehicle_documents = VehicleDocument.objects.filter(vehicle=vehicle)
    driver_history = VehicleDriver.objects.filter(vehicle=vehicle)

    context['vehicle'] = vehicle
    context['vehicle_tyres'] = vehicle_tire

    context['incidents'] = incidents

    context['purchase_detail'] = purchase_detail
    context['financial_detail'] = financial_detail

    context['fuel_card'] = fuel_card

    context['insurance'] = insurance

    context['tracker'] = tracker

    context['branding'] = branding

    context['vehicle_documents'] = vehicle_documents

    context['driver_history'] = driver_history
    return render(request, template, context)

@login_required
def traffic_fine_list(request, template="fleet_management/traffic_fines.html"):
    context = {}

    filter_form = TrafficFineFilterForm(request.GET or None)
    all_fines = Incident.objects.filter(incident_type = 'traffic fine').order_by('-incident_date')

    if u'search' in request.GET or u'extract' in request.GET:
        if filter_form.is_valid():
            all_fines = filter_form.filter(all_fines)
            context['reset_button'] = True

    if u'extract' in request.GET:
        if filter_form.is_valid():
            download_thread = threading.Thread(target=extract_incident_data,
                                               args=(request.user, all_fines,
                                                     filter_form.cleaned_data, True))
            download_thread.start()
            messages.success(request, 'Your extract has been added to the download queue. Queue processing may take a while. Check your report in downloads.')

    context['all_fines'] = all_fines
    context['filter_form'] = filter_form
    context['traffic_fines'] = True
    return render(request, template, context)

@login_required
def add_document(request, vehicle_id, context=None):

    context = context or {}

    vehicle = Vehicle.objects.get(pk=vehicle_id)

    document_file_form = DocumentFileForm(request.POST or None, request.FILES or None, prefix="documents")

    if request.POST:

        if document_file_form.is_valid():
            document = document_file_form.save(commit=False)
            document.document_name = document.document.name
            document.file_type = 'document'
            document.save()
            vehicle_documents = VehicleDocument.objects.create(vehicle_id=vehicle.id, document_id=document.id, created_by_id=request.user.id, document_type = document_file_form.cleaned_data['document_type'])

        return redirect(reverse('fleetmanagement:edit_vehicle', kwargs={'vehicle_id': vehicle.id}) + "#file_upload")

@login_required
def add_photo(request, vehicle_id, context=None):

    context = context or {}
    vehicle = Vehicle.objects.get(pk=vehicle_id)

    photo_file_form = PhotoFileForm(request.POST or None, request.FILES or None, prefix="photos")

    if request.POST:

        if photo_file_form.is_valid():

            photo = photo_file_form.save(commit=False)
            photo.document_name = photo.image.name
            photo.file_type = 'photo'
            photo.save()

            vehicle_documents = VehicleDocument.objects.create(vehicle_id=vehicle.id, document_id=photo.id, created_by_id=request.user.id)

    return redirect(reverse('fleetmanagement:vehicles'))

@login_required
def edit_traffic_fine(request, incident_id=None, template="fleet_management/edit_traffic_fine.html", context=None):

    context = context or {}
    incident = None
    vehicle_driver = None
    if incident_id:
        incident = Incident.objects.get(pk=incident_id)
        traffic_fine_form = TrafficFineForm(request.POST or None, instance=incident)
        traffic_fine_form.initial['vehicle'] = incident.vehicle
        if incident.driver:
            traffic_fine_form.initial['driver'] = incident.driver

        status=incident.status
    else:
        traffic_fine_form = TrafficFineForm(request.POST or None)

    traffic_fine_document_form = TrafficFineDocumentForm(request.POST or None)
    file_form = IncidentFileForm(request.POST or None, request.FILES or None, prefix="documents")

    if u'captured' in request.POST:
            status = "captured"

    if u'rejected' in request.POST:
        status = "rejected"

    if u'submit_for_payment' in request.POST:
        status = "submitted for payment"

    if u'paid' in request.POST:
        status = "paid"
    
    if traffic_fine_form.is_valid():        
        incident = traffic_fine_form.save(commit=False)
        incident.incident_type = 'traffic fine'
        incident.created_by = request.user
        incident.status = status
        vehicle_driver = VehicleDriver.objects.filter(vehicle = traffic_fine_form.cleaned_data['vehicle'],
                                                      start_date__lte=traffic_fine_form.cleaned_data['incident_date'])\
                                              .filter(Q(end_date__gte=incident.incident_date) |
                                                      Q(end_date=None)).first()

        if vehicle_driver:
            incident.vehicle_driver = vehicle_driver
            incident.driver = vehicle_driver.driver

        incident.save()

        if file_form.is_valid():
            document = file_form.save(commit=False)
            document.document_name = document.document.name
            document.file_type = 'document'
            document.description = 'trafic fine file'
            if document.document_name is not None and traffic_fine_document_form.is_valid():
                document.save()

                incident_document = traffic_fine_document_form.save(commit=False)
                incident_document.incident = incident
                incident_document.document = document
                incident_document.created_by = request.user
                incident_document.save()
                traffic_fine_document_form.save_m2m()

                return redirect(reverse('fleetmanagement:view_traffic_fines'))

            else:

                return redirect(reverse('fleetmanagement:view_traffic_fines'))

        else:
            return redirect(reverse('fleetmanagement:view_traffic_fines'))

    proof_of_payment = IncidentDocument.objects.filter(
                                incident=incident,
                                document_type__description="Proof Of Payment").exists()

    context['incident'] = incident
    context['file_form'] = file_form
    context['traffic_fine_form'] = traffic_fine_form
    context['traffic_fine_document_form'] = traffic_fine_document_form
    context['vehicle_driver'] = vehicle_driver
    context['proof_of_pay'] = proof_of_payment
    return render(request, template, context)

@login_required
def resolve_fine(request, incident_id):
    incident = Incident.objects.get(pk=incident_id)

    incident.resolved = True
    incident.save()

    return redirect(reverse('fleetmanagement:view_traffic_fines'))


@login_required
def edit_incident(request, incident_id=None, document_name=None, template="fleet_management/edit_incident.html", context=None):

    context = context or {}
    incident = None
    vehicle_driver = None
    incident = Incident.objects.get(pk=incident_id) if incident_id else None

    incident_documents = IncidentDocument.objects.filter(incident_id=incident_id)
    incident_comments = IncidentComment.objects.filter(incident_id=incident_id)
    documents = Document.objects.all()

    if incident:
        incident = Incident.objects.get(pk=incident_id)
        incident_form = AddIncidentForm(request.POST or None, instance=incident)

        status=incident.status
    else:
        incident_form = AddIncidentForm(request.POST or None)


    incident_document_form = IncidentDocumentForm(request.POST or None, prefix='documents')
    incident_file_form = IncidentFileForm(request.POST or None, request.FILES or None, prefix="documents" if not document_name else None)
    incident_comment_form = CommentForm(request.POST or None, prefix='comment')

    if u'captured' in request.POST:
            status = "captured"

    if u'rejected' in request.POST:
        status = "rejected"

    if u'submit_for_payment' in request.POST:
        status = "submitted for payment"

    if u'paid' in request.POST:
        status = "paid"


    if incident_form.is_valid():
        incident = incident_form.save(commit=False)
        incident.created_by = request.user
        incident.status = status
        vehicle_driver = VehicleDriver.objects.filter(vehicle = incident_form.cleaned_data['vehicle'],
                                                      start_date__lte=incident_form.cleaned_data['incident_date'])\
                                              .filter(Q(end_date__gte=incident.incident_date) |
                                                      Q(end_date=None)).first()

        if vehicle_driver:
            incident.driver = vehicle_driver.driver

        if incident.driver_co_payment=='no':
          incident.percentage = None
          incident.share_amount = None

        incident.save()

        if incident_comment_form.has_changed() and incident_comment_form.is_valid():
            comment = incident_comment_form.save(commit=False)
            if comment.comment is not None or comment.comment != "":
                comment.save()
                incident_comment = IncidentComment.objects.create(incident_id=incident.id, 
                                                                    comment_id=comment.id, 
                                                                    created_by_id=request.user.id)

        if incident_file_form.is_valid():
            document = incident_file_form.save(commit=False)
            document.document_name = document.document.name
            document.file_type = 'document'
            document.description = 'incident file'

            if document.document_name is not None and incident_document_form.is_valid():
                document.save()

                incident_document = incident_document_form.save(commit=False)
                incident_document.incident = incident
                incident_document.document = document
                incident_document.created_by = request.user
                incident_document.save()
                incident_document_form.save_m2m()

                return redirect(reverse('fleetmanagement:view_incidents'))

            else:

                return redirect(reverse('fleetmanagement:view_incidents'))

        else:
            return redirect(reverse('fleetmanagement:view_incidents'))


    context['incident_form'] = incident_form
    context['incident'] = incident
    context['incident_file_form'] = incident_file_form
    context['incident_form'] = incident_form
    context['incident_documents'] = incident_documents
    context['incident_comments'] = incident_comments
    context['documents'] = documents
    context['incident_document_form'] = incident_document_form
    context['incident_comment_form'] = incident_comment_form

    return render(request, template, context)

@login_required
def view_incident(request, incident_id=None, document_name=None, template="fleet_management/view_incident.html", context=None):

    context = context or {}
    incident = None
    vehicle_driver = None
    incident = Incident.objects.get(pk=incident_id) if incident_id else None

    incident_documents = IncidentDocument.objects.filter(incident_id=incident_id)
    documents = Document.objects.all()

    if incident:
        incident = Incident.objects.get(pk=incident_id)
        incident_form = AddIncidentForm(request.POST or None, instance=incident)
        incident_form.initial['vehicle'] = incident.vehicle
        if incident.driver:
            incident_form.initial['driver'] = incident.driver

        status=incident.status
    else:
        incident_form = AddIncidentForm(request.POST or None)


    incident_document_form = IncidentDocumentForm(request.POST or None, prefix='documents')
    incident_file_form = IncidentFileForm(request.POST or None, request.FILES or None, prefix="documents" if not document_name else None)

    if u'captured' in request.POST:
            status = "captured"

    if u'rejected' in request.POST:
        status = "rejected"

    if u'submit_for_payment' in request.POST:
        status = "submitted for payment"

    if u'paid' in request.POST:
        status = "paid"


    if incident_form.is_valid():
        incident = incident_form.save(commit=False)
        incident.created_by = request.user
        incident.status = status
        vehicle_driver = VehicleDriver.objects.filter(vehicle = incident_form.cleaned_data['vehicle'],
                                                      start_date__lte=incident_form.cleaned_data['incident_date'])\
                                              .filter(Q(end_date__gte=incident.incident_date) |
                                                      Q(end_date=None)).first()

        if vehicle_driver:
            incident.vehicle_driver = vehicle_driver
            incident.driver = vehicle_driver.driver

        incident.save()

        if incident_file_form.is_valid():
            document = incident_file_form.save(commit=False)
            document.document_name = document.document.name
            document.file_type = 'document'
            document.description = 'incident file'

            if document.document_name is not None and incident_document_form.is_valid():
                document.save()

                incident_document = incident_document_form.save(commit=False)
                incident_document.incident = incident
                incident_document.document = document
                incident_document.created_by = request.user
                incident_document.save()
                incident_document_form.save_m2m()

                return redirect(reverse('fleetmanagement:view_incidents'))

            else:

                return redirect(reverse('fleetmanagement:view_incidents'))

        else:
            return redirect(reverse('fleetmanagement:view_incidents'))


    context['incident_form'] = incident_form
    context['incident'] = incident
    context['incident_file_form'] = incident_file_form
    context['incident_form'] = incident_form
    context['incident_documents'] = incident_documents
    context['documents'] = documents
    context['incident_document_form'] = incident_document_form

    return render(request, template, context)

@login_required
def file_download_task(request, file_id):
    saved_file = Document.objects.get(pk=file_id)
    return file_download(file=saved_file)

@login_required
def vehicle_maintenance(request, template="fleet_management/vehicle_maintenance.html"):
    context = {}
    vehicle_maintenance_form = VehicleMaintenanceFilterForm(request.POST or None)

    vehicle_maintenances = VehicleMaintenance.objects.all()

    if u'search' in request.POST:
        if vehicle_maintenance_form.is_valid():
            vehicle_maintenances = vehicle_maintenance_form.filter(vehicle_maintenances)
            if len(set(vehicle_maintenance_form.cleaned_data.values())) > 1:
                context['reset_button'] = True

    if u'extract' in request.POST:
        if vehicle_maintenance_form.is_valid():
            vehicle_maintenances = vehicle_maintenance_form.filter(vehicle_maintenances)
            download_thread = threading.Thread(target=extract_vehicle_maintenance_data,
                                               args=(request.user, 'all_vehicle_maintenances',
                                                     vehicle_maintenances,
                                                     vehicle_maintenance_form.cleaned_data))
            download_thread.start()
            if len(set(vehicle_maintenance_form.cleaned_data.values())) > 1:
                context['reset_button'] = True


    context['vehicle_maintenance'] = vehicle_maintenances
    context['vehicle_maintenance_form'] = vehicle_maintenance_form

    return render(request, template, context)

@login_required
def edit_vehicle_maintenance(request,  vehicle_maintenance_id=None, template="fleet_management/edit_vehicle_maintenance.html", context=None):

    context = context or {}
    vehicle_maintenance = None

    if vehicle_maintenance_id:
        vehicle_maintenance = VehicleMaintenance.objects.get(pk=vehicle_maintenance_id)
        vehicle_maintenance_form = AddVehicleMaintenanceForm(
            request.POST or None, instance=vehicle_maintenance)
    else:
        vehicle_maintenance_form = AddVehicleMaintenanceForm(request.POST or None)

    if vehicle_maintenance_form.is_valid():
        vehicle_maintenance = vehicle_maintenance_form.save(commit=False)
        vehicle_maintenance.created_by = request.user
        vehicle_maintenance.save()

        return redirect(reverse('fleetmanagement:vehicle_maintenance'))

    context['vehicle_maintenance_form'] = vehicle_maintenance_form
    context['vehicle_maintenance'] = vehicle_maintenance

    return render(request, template, context)


@login_required
def edit_insurer(request,  insurer_id=None, template="fleet_management/edit_insurer.html", context=None):

    context = context or {}
    insurer = None
    contact_person = None
    address = None

    if insurer_id:
        insurer = Insurer.objects.get(pk=insurer_id)
        insurer_form = InsurerForm(request.POST or None, instance=insurer)
        if insurer.contact_person:
            contact_person = Contact.objects.get(pk=insurer.contact_person_id)
        contact_form = ContactForm(request.POST or None, instance=contact_person)
        if insurer.address:
            address = Address.objects.get(pk=insurer.address_id)
        address_form = AddressForm(request.POST or None, instance=address)
    else:
        insurer_form = InsurerForm(request.POST or None)
        contact_form = ContactForm(request.POST or None)
        address_form = AddressForm(request.POST or None)
    if contact_form.is_valid():
        contact_person = contact_form.save(commit=False)
        contact_person.save()

    if address_form.is_valid():
        address = address_form.save(commit=False)
        address.address_type = 'business'
        address.save()

    if insurer_form.is_valid():
        insurer = insurer_form.save(commit=False)
        insurer.contact_person = contact_person
        insurer.address = address
        insurer.created_by = request.user
        insurer.save()

        return redirect(reverse('fleetmanagement:view_insurers'))

    context['insurer_form'] = insurer_form
    context['contact_form'] = contact_form
    context['address_form'] = address_form
    context['insurer'] = insurer

    return render(request, template, context)

@login_required
def insurers(request, template="fleet_management/insurers.html", context=None):
    context = context or {}

    insurers = Insurer.objects.all()

    filter_form = InsurerFilterForm(request.POST or None)
    if u'search' in request.POST:
        if filter_form.is_valid():
            insurers = filter_form.filter(insurers)

    if u'extract' in request.POST:
        if filter_form.is_valid():
            insurers = filter_form.filter(insurers)
            download_thread = threading.Thread(target=extract_insurers_data,
                                               args=(request.user, "insurers", insurers,
                                                     filter_form.cleaned_data))
            download_thread.start()


    context['insurers'] = insurers
    context['filter_form'] = filter_form

    return render(request, template, context)

@login_required
def insured(request, insurer_id, template="fleet_management/insured.html", context=None):

    context = context or {}
    insurer = Insurer.objects.get(pk=int(insurer_id))
    insured_vehicles =  Insurance.objects.filter(insurer=insurer)

    vehicles_filter_form = InsuredVehiclesFilterForm(request.POST or None)

    if u'search' in request.POST:
        if vehicles_filter_form.is_valid():
            insured_vehicles = vehicles_filter_form.filter(insured_vehicles)
            if len(set(vehicles_filter_form.cleaned_data.values())) > 1:
                context['reset_button'] = True

    if u'extract' in request.POST:
        if vehicles_filter_form.is_valid():
            insured_vehicles = vehicles_filter_form.filter(insured_vehicles)
            download_thread = threading.Thread(target=extract_insurer_vehicles_data,
                                               args=(request.user, "insured_vehicles", insurer,
                                                     insured_vehicles, vehicles_filter_form.cleaned_data))
            download_thread.start()
            if len(set(vehicles_filter_form.cleaned_data.values())) > 1:
                context['reset_button'] = True


    context['title'] = "Insured Vehicles: "+ insurer.name
    context['insurer'] = insurer
    context['total'] = insured_vehicles.count()
    context['insured_vehicles'] = insured_vehicles
    context['vehicles_filter_form'] = vehicles_filter_form

    return render(request, template, context)

@login_required
def document_delete(request, vehicle_document_id):

    vehicle_document = VehicleDocument.objects.get(pk=vehicle_document_id)
    vehicle = vehicle_document.vehicle.id
    document = vehicle_document.document.id

    vehicle_document.deleted = True
    vehicle_document.save()

    documents = Document.objects.get(id=document)
    documents.deleted = True
    documents.save()

    return redirect(reverse('fleetmanagement:edit_vehicle', kwargs={'vehicle_id': vehicle}) + "#file_upload")

@login_required
def unassign_vehicle(request, vehicle_id):
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    vehicle_driver = vehicle.current_vehicle_driver
    vehicle_driver.end_date = datetime.now()
    vehicle_driver.save()

    return redirect(reverse('fleetmanagement:edit_vehicle', kwargs={'vehicle_id': vehicle_id}) + "#vehicle_driver")

@login_required
def incident_document_delete(request, incident_document_id):
    incident_document = IncidentDocument.objects.get(pk=incident_document_id)
    incident = incident_document.incident.id
    document = incident_document.document.id

    incident_document.deleted = True
    incident_document.save()

    documents = Document.objects.get(id=document)
    documents.deleted = True
    documents.save()

    return redirect(reverse('fleetmanagement:edit_incident', kwargs={'incident_id': incident}))

@login_required
def service_booking(request, template="fleet_management/service_booking.html"):
    context = {}
    service_booking_form = ServiceBookingFilterForm(request.POST or None)

    service_bookings = ServiceBooking.objects.filter(Q(status="booked")|Q(status="declined")|Q(status="authorised")|Q(status="awaiting authorisation")).order_by('service_date').reverse()

    if u'search' in request.POST:
        if service_booking_form.is_valid():
            service_bookings = service_booking_form.filter(service_bookings)
            if len(set(service_booking_form.cleaned_data.values())) > 1:
                context['reset_button'] = True

    if u'extract' in request.POST:
        if service_booking_form.is_valid():
            service_bookings = service_booking_form.filter(service_bookings)
            download_thread = threading.Thread(target=extract_service_booking_data,
                                               args=(request.user, 'all_resolved_service_bookings',
                                                     service_bookings,
                                                     service_booking_form.cleaned_data))
            download_thread.start()
            messages.success(request, 'Your extract has been added to the download queue. Queue processing may take a while. Check your report in downloads.')

            if len(set(service_booking_form.cleaned_data.values())) > 1:
                context['reset_button'] = True

    context['service_bookings'] = service_bookings
    context['service_booking_form'] = service_booking_form

    return render(request, template, context)

@login_required
def resolved_service_booking(request, template="fleet_management/resolved_service_booking.html"):
    context = {}
    service_booking_form = ServiceBookingFilterForm(request.POST or None)

    service_bookings = ServiceBooking.objects.filter(status="resolved").order_by('service_date').reverse()

    if u'search' in request.POST:
        if service_booking_form.is_valid():
            service_bookings = service_booking_form.filter(service_bookings)
            if len(set(service_booking_form.cleaned_data.values())) > 1:
                context['reset_button'] = True

    if u'extract' in request.POST:
        if service_booking_form.is_valid():
            service_bookings = service_booking_form.filter(service_bookings)
            download_thread = threading.Thread(target=extract_resolved_service_booking_data,
                                               args=(request.user, 'all_service_bookings',
                                                     service_bookings,
                                                     service_booking_form.cleaned_data))
            download_thread.start()
            messages.success(request, 'Your extract has been added to the download queue. Queue processing may take a while. Check your report in downloads.')

            if len(set(service_booking_form.cleaned_data.values())) > 1:
                context['reset_button'] = True

    context['service_bookings'] = service_bookings
    context['service_booking_form'] = service_booking_form

    return render(request, template, context)

@login_required
def service_booking_invoice(request, template="fleet_management/service_booking_invoice.html"):
    context = {}
    service_booking_form = ServiceBookingFilterForm(request.POST or None)

    service_bookings = ServiceBooking.objects.filter(status="captured").order_by('service_date').reverse()

    if u'search' in request.POST:
        if service_booking_form.is_valid():
            service_bookings = service_booking_form.filter(service_bookings)
            if len(set(service_booking_form.cleaned_data.values())) > 1:
                context['reset_button'] = True

    if u'extract' in request.POST:
        if service_booking_form.is_valid():
            service_bookings = service_booking_form.filter(service_bookings)
            download_thread = threading.Thread(target=extract_invoice_service_booking_data,
                                               args=(request.user, 'all_service_bookings',
                                                     service_bookings,
                                                     service_booking_form.cleaned_data))
            download_thread.start()
            messages.success(request, 'Your extract has been added to the download queue. Queue processing may take a while. Check your report in downloads.')

            if len(set(service_booking_form.cleaned_data.values())) > 1:
                context['reset_button'] = True

    context['service_bookingss'] = service_bookings
    context['service_booking_form'] = service_booking_form

    return render(request, template, context)

@login_required
def edit_service_booking(request,  service_booking_id=None, document_name=None, template="fleet_management/edit_service_booking.html", context=None):
    context = context or {}
    service_booking = None
    contact_person = None
    address = None
    vendor_id = None
    document_name=None

    service_booking_documents = ServiceMaintanceDocument.objects.filter(service_booking_id=service_booking_id).order_by('-id')

    if service_booking_id:
        service_booking = ServiceBooking.objects.get(pk=service_booking_id)
        service_booking_form = AddServiceBookingForm(request.POST or None, instance=service_booking)

        status=service_booking.status

    else:
        service_booking_form = AddServiceBookingForm(request.POST or None)

    service_booking_document_form = ServiceMaintanceDocumentForm(request.POST or None, request.FILES or None, prefix="documents" if not document_name else None)

    if u'book' in request.POST:
        status = "booked"

    if u'escalate' in request.POST:
        status = "escalated"

    if u'accept' in request.POST:
        status = "awaiting authorisation"

    if u'resolve' in request.POST:
        status = "resolved"

    if u'decline' in request.POST:
        status = "declined"

    if u'authorise' in request.POST:
        status = "authorised"



    if service_booking_form.is_valid():
        service_booking = service_booking_form.save(commit=False)
        service_booking.created_by = request.user
        service_booking.status = status
        if service_booking.status == "declined" and service_booking.comment == "":
          messages.error(request, "Please comment when declining")
          return redirect(reverse('fleetmanagement:edit_service_booking', kwargs={'service_booking_id': service_booking_id}))

        if service_booking.long_term_repairs is False:
          service_booking.follow_up_date = None

        if service_booking.other and not service_booking.comment:
            messages.error(request, "Please enter maintenance descriptive text in the comment field")
        else:
            if service_booking.status == "authorised":

                get_vendor = service_booking.vendor.id
                vendor = None
                vendor = Vendor.objects.get(pk=get_vendor)
                get_vendor_balance = vendor.balance
                if vendor.account_type == "debit":
                    vendor_balance = get_vendor_balance - service_booking.document_amount
                    if vendor_balance < 0:
                        messages.error(request, "Insufficient funds")
                    
                    else:
                        if service_booking_id:
                            vendor.balance = vendor_balance
                            obj = Vendor.objects.filter(pk=get_vendor).update(balance=vendor_balance)
                            service_booking.authorised_by = request.user
                            service_booking.save()
                            template = get_template('fleet_management/widgets/documents/requisition_document.html')
                            context = {
                              'pagesize': 'A4',
                              "service_booking":service_booking,
                              'STATIC_URL' : settings.STATIC_URL
                            }

                            html = template.render(context)
                            pdf = render_to_pdf('fleet_management/widgets/documents/requisition_document.html', context)

                            myDate = datetime.now()
                            formatedDate = myDate.strftime("%Y%m%d_%H_%M_%S")

                            folder = "uploads/documents/"
                            name = "requisition_"+formatedDate
                            filename = os.path.join(settings.MEDIA_ROOT, folder) + name + ".pdf"

                            pisa.CreatePDF(StringIO.StringIO(html.encode("UTF-8")),
                                             file(filename,'w'))

                            filename = "requisition_"+formatedDate+".pdf"
                            upload_file = Document.objects.create(file_type="download",
                                                        description="Requisition Document",
                                                        document_name=filename,
                                                        created_at=datetime.now(),
                                                        created_by=request.user)
                            upload_file.document = 'uploads/documents/'+filename

                            upload_file.save()
                            upload_file = ServiceMaintanceDocument.objects.create(service_booking=service_booking,
                                                        document=upload_file,
                                                        created_by=request.user)

                            upload_file.save()
                            return redirect(reverse('fleetmanagement:service_booking'))
                elif vendor.account_type == "credit":
                    vendor_balance = get_vendor_balance + service_booking.document_amount
                    if vendor_balance < 0:
                        messages.error(request, "Funds can not be negetive")
                    
                    else:
                        if service_booking_id:
                            vendor.balance = vendor_balance
                            obj = Vendor.objects.filter(pk=get_vendor).update(balance=vendor_balance)
                            service_booking.authorised_by = request.user
                            service_booking.save()
                            template = get_template('fleet_management/widgets/documents/requisition_document.html')
                            context = {
                              'pagesize': 'A4',
                              "service_booking":service_booking,
                              'STATIC_URL' : settings.STATIC_URL
                            }

                            html = template.render(context)
                            pdf = render_to_pdf('fleet_management/widgets/documents/requisition_document.html', context)

                            myDate = datetime.now()
                            formatedDate = myDate.strftime("%Y%m%d_%H_%M_%S")

                            folder = "uploads/documents/"
                            name = "requisition_"+formatedDate
                            filename = os.path.join(settings.MEDIA_ROOT, folder) + name + ".pdf"

                            pisa.CreatePDF(StringIO.StringIO(html.encode("UTF-8")),
                                             file(filename,'w'))

                            filename = "requisition_"+formatedDate+".pdf"
                            upload_file = Document.objects.create(file_type="download",
                                                        description="Requisition Document",
                                                        document_name=filename,
                                                        created_at=datetime.now(),
                                                        created_by=request.user)
                            upload_file.document = 'uploads/documents/'+filename

                            upload_file.save()
                            upload_file = ServiceMaintanceDocument.objects.create(service_booking=service_booking,
                                                        document=upload_file,
                                                        created_by=request.user)

                            upload_file.save()
                            return redirect(reverse('fleetmanagement:service_booking'))
                else:
                    service_booking.authorised_by = request.user
                    service_booking.save()
                    template = get_template('fleet_management/widgets/documents/requisition_document.html')
                    context = {
                      'pagesize': 'A4',
                      "service_booking":service_booking,
                      'STATIC_URL' : settings.STATIC_URL
                    }

                    html = template.render(context)
                    pdf = render_to_pdf('fleet_management/widgets/documents/requisition_document.html', context)

                    myDate = datetime.now()
                    formatedDate = myDate.strftime("%Y%m%d_%H_%M_%S")

                    folder = "uploads/documents/"
                    name = "requisition_"+formatedDate
                    filename = os.path.join(settings.MEDIA_ROOT, folder) + name + ".pdf"

                    pisa.CreatePDF(StringIO.StringIO(html.encode("UTF-8")),
                                     file(filename,'w'))

                    filename = "requisition_"+formatedDate+".pdf"
                    upload_file = Document.objects.create(file_type="download",
                                                description="Requisition Document",
                                                document_name=filename,
                                                created_at=datetime.now(),
                                                created_by=request.user)
                    upload_file.document = 'uploads/documents/'+filename

                    upload_file.save()
                    upload_file = ServiceMaintanceDocument.objects.create(service_booking=service_booking,
                                                document=upload_file,
                                                created_by=request.user)

                    upload_file.save()

                    return redirect(reverse('fleetmanagement:service_booking'))

            else:
                # service_booking.authorised_by = request.user
                service_booking.save()

                # template = get_template('fleet_management/widgets/documents/requisition_document.html')
                # context = {
                #   'pagesize': 'A4',
                #   "service_booking":service_booking,
                #   'STATIC_URL' : settings.STATIC_URL
                # }

                # html = template.render(context)
                # pdf = render_to_pdf('fleet_management/widgets/documents/requisition_document.html', context)

                # myDate = datetime.now()
                # formatedDate = myDate.strftime("%Y%m%d_%H_%M_%S")

                # folder = "uploads/documents/"
                # name = "requisition_"+formatedDate
                # filename = os.path.join(settings.MEDIA_ROOT, folder) + name + ".pdf"

                # pisa.CreatePDF(StringIO.StringIO(html.encode("UTF-8")),
                #                  file(filename,'w'))

                # filename = "requisition_"+formatedDate+".pdf"
                # upload_file = Document.objects.create(file_type="download",
                #                             description="Requisition Document",
                #                             document_name=filename,
                #                             created_at=datetime.now(),
                #                             created_by=request.user)
                # upload_file.document = 'uploads/documents/'+filename

                # upload_file.save()
                # upload_file = ServiceMaintanceDocument.objects.create(service_booking=service_booking,
                #                             document=upload_file,
                #                             created_by=request.user)

                # upload_file.save()

            vehicle = service_booking.vehicle
            status_type = None
            comment = ""

            if service_booking.status == "booked":
                if service_booking.service:
                    status_type = VehicleStatusType.objects.filter(description="Service (<24 hours)").first()
                if service_booking.maintenance and service_booking.long_term_repairs:
                    status_type = VehicleStatusType.objects.filter(description="Maintenance (>24 hours)").first()
                comment = "Vehicle booked for Service/Maintenance, status changed to %s"%(status_type)

            if service_booking.status == "authorised":
                status_type = VehicleStatusType.objects.filter(description="Active").first()
                comment = "Vehicle Service/Maintenance was authorized, status changed to %s"%(status_type)

            if status_type is not None and comment !="" and vehicle:
                vehicle_status = change_vehicle_status(request, vehicle, status_type, comment)

            if service_booking_document_form.is_valid():
                document = service_booking_document_form.save(commit=False)
                document.document_name = document.document
                document.file_type = 'document'
                document.description = service_booking.document_received
                if document.document_name != None:

                    document.save()

                    service_booking_document = ServiceMaintanceDocument.objects.create(service_booking_id=service_booking.id, 
                                                                  document_id=document.id, 
                                                                  created_by_id=request.user.id)
                    return redirect(reverse('fleetmanagement:service_booking'))

                else:
                    return redirect(reverse('fleetmanagement:service_booking'))


    context['service_booking_form'] = service_booking_form
    context['service_booking'] = service_booking
    context['service_booking_documents'] = service_booking_documents
    context['service_booking_document_form'] = service_booking_document_form

    return render(request, template, context)

@login_required
def edit_service_booking_invoice(request,  service_booking_id=None, document_name=None, template="fleet_management/edit_service_booking_invoice.html", context=None):
    context = context or {}
    service_booking = None
    contact_person = None
    address = None
    vendor_id = None
    document_name=None

    service_booking_documents = ServiceMaintanceDocument.objects.filter(service_booking_id=service_booking_id).order_by('-id')

    if service_booking_id:
        service_booking = ServiceBooking.objects.get(pk=service_booking_id)
        service_booking_form = ServiceBookingInvoiceForm(request.POST or None, instance=service_booking)

        status=service_booking.status

    else:
        service_booking_form = ServiceBookingInvoiceForm(request.POST or None)

    service_booking_document_form = ServiceMaintanceDocumentForm(request.POST or None, request.FILES or None, prefix="documents" if not document_name else None)

    if u'capture' in request.POST:
        status = "captured"

    if u'resolve' in request.POST:
        status = "resolved"

    if service_booking_form.is_valid():
        service_booking = service_booking_form.save(commit=False)
        service_booking.created_by = request.user
        service_booking.status = status

        if service_booking.long_term_repairs is False:
          	service_booking.follow_up_date = None


          	service_booking.save()

          	if service_booking_document_form.is_valid():
	            document = service_booking_document_form.save(commit=False)
	            document.document_name = document.document
	            document.file_type = 'document'
	            document.description = service_booking.document_received
            	if document.document_name != None:
            		document.description = service_booking.document_received
            		document.created_by_id = request.user.id
              		document.save()

              		service_booking_document = ServiceMaintanceDocument.objects.create(service_booking_id=service_booking.id, 
                                                                  document_id=document.id, 
                                                                  created_by_id=request.user.id)
              		return redirect(reverse('fleetmanagement:service_booking_invoice'))

            	else:
              		return redirect(reverse('fleetmanagement:service_booking_invoice'))
          	return redirect(reverse('fleetmanagement:service_booking_invoice'))

    context['service_booking_formm'] = service_booking_form
    context['service_bookingg'] = service_booking
    context['service_booking_documents'] = service_booking_documents
    context['service_booking_document_form'] = service_booking_document_form

    return render(request, template, context)

@login_required
def edit_service_provider(request,  service_provider_id=None, template="fleet_management/edit_service_provider.html", context=None):

    context = context or {}
    service_provider = None
    contact_person = None
    address = None

    if service_provider_id:
        service_provider = ServiceProvider.objects.get(pk=service_provider_id)
        service_provider_form = ServiceProviderForm(request.POST or None, instance=service_provider)
        if service_provider.contact_person:
            contact_person = Contact.objects.get(pk=service_provider.contact_person_id)
        contact_form = ContactForm(request.POST or None, instance=contact_person)
        if service_provider.address:
            address = Address.objects.get(pk=service_provider.address_id)
        address_form = AddressForm(request.POST or None, instance=address)
    else:
        service_provider_form = ServiceProviderForm(request.POST or None)
        contact_form = ContactForm(request.POST or None)
        address_form = AddressForm(request.POST or None)
    if contact_form.is_valid():
        contact_person = contact_form.save(commit=False)
        contact_person.save()

    if address_form.is_valid():
        address = address_form.save(commit=False)
        address.address_type = 'business'
        address.save()

    if service_provider_form.is_valid():
        service_provider = service_provider_form.save(commit=False)
        service_provider.contact_person = contact_person
        service_provider.address = address
        service_provider.created_by = request.user
        service_provider.save()

        return redirect(reverse('fleetmanagement:view_service_providers'))

    context['service_provider_form'] = service_provider_form
    context['contact_form'] = contact_form
    context['address_form'] = address_form
    context['service_provider'] = service_provider

    return render(request, template, context)

@login_required
def service_providers(request, template="fleet_management/service_providers.html", context=None):
    context = context or {}

    service_providers = ServiceProvider.objects.all()

    filter_form = ServiceProviderFilterForm(request.POST or None)
    if u'search' in request.POST:
        if filter_form.is_valid():
            service_providers = filter_form.filter(service_providers)

    if u'extract' in request.POST:
        if filter_form.is_valid():
            service_providers = filter_form.filter(service_providers)
            download_thread = threading.Thread(target=extract_service_providers_data,
                                               args=(request.user, "service_providers", service_providers,
                                                     filter_form.cleaned_data))
            download_thread.start()


    context['service_providers'] = service_providers
    context['filter_form'] = filter_form

    return render(request, template, context)

@login_required
def vendors(request, template="fleet_management/vendors.html", context=None):
    context = context or {}

    vendors = Vendor.objects.all()

    filter_form = VendorFilterForm(request.POST or None)
    if u'search' in request.POST:
        if filter_form.is_valid():
            vendors = filter_form.filter(vendors)

    if u'extract' in request.POST:
        if filter_form.is_valid():
            vendors = filter_form.filter(vendors)
            download_thread = threading.Thread(target=extract_vendors_data,
                                               args=(request.user, "vendors", vendors,
                                                     filter_form.cleaned_data))

            download_thread.start()
            messages.success(request, 'Your extract has been added to the download queue. Queue processing may take a while. Check your report in downloads.')

    context['vendors'] = vendors
    context['filter_form'] = filter_form

    return render(request, template, context)

@login_required
def edit_vendor(request,  vendor_id=None, template="fleet_management/edit_vendor.html", context=None):

    context = context or {}
    vendor = None
    contact_person = None
    address = None
    vendor_bank_details = None

    if vendor_id:
        vendor = Vendor.objects.get(pk=vendor_id)
        get_account_type = vendor.account_type
        vendor_form = VendorForm(request.POST or None, instance=vendor)
        if vendor.contact_person:
            contact_person = Contact.objects.get(pk=vendor.contact_person_id)
        contact_form = ContactForm(request.POST or None, instance=contact_person)
        if vendor.address:
            address = Address.objects.get(pk=vendor.address_id)
        address_form = AddressForm(request.POST or None, instance=address)

        vendor_bank_details = vendor.vendor_bank_details.first() if vendor and \
                          vendor.vendor_bank_details.exists() else VendorBankDetail()
        vendor_bank_details_form = VendorBankDetailForm(request.POST or None,
                                                  instance=vendor_bank_details,
                                                  prefix='vendor_bank_details')

    else:
        vendor_form = VendorForm(request.POST or None)
        contact_form = ContactForm(request.POST or None)
        address_form = AddressForm(request.POST or None)
        vendor_bank_details_form = VendorBankDetailForm(request.POST or None)
    if contact_form.is_valid():
        contact_person = contact_form.save(commit=False)
        contact_person.save()

    if address_form.is_valid():
        address = address_form.save(commit=False)
        address.address_type = 'business'
        address.save()

    if vendor_bank_details_form.is_valid():
          vendor_bank_details = vendor_bank_details_form.save(commit=False)
          vendor_bank_details.created_by = request.user
          vendor_bank_details.vendor = vendor
          vendor_bank_details.save()

    if vendor_form.is_valid():
        vendor = vendor_form.save(commit=False)
        vendor.contact_person = contact_person
        vendor.address = address
        vendor.created_by = request.user
        if vendor.account_type == 'cash':
          vendor.balance = 0.00
        if vendor.account_type == "":
          vendor.account_type = get_account_type

        vendor.save()

        return redirect(reverse('fleetmanagement:view_vendors'))

    context['vendor_form'] = vendor_form
    context['contact_form'] = contact_form
    context['address_form'] = address_form
    context['vendor_bank_details_form'] = vendor_bank_details_form
    context['vendor'] = vendor

    return render(request, template, context)

@login_required
def change_vehicle_status(request, vehicle, status, comment):
    new_status = VehicleStatus(vehicle=vehicle,
                               status_type=status,
                               comment=comment,
                               created_by=request.user)
    new_status.save()

    vehicle.status = new_status.status_type
    vehicle.save()

    return new_status

@login_required
def unassign(request, vehicle_id=None, template="fleet_management/unassign.html", context=None):

    context = context or {}
    vehicle_driver = None

    if vehicle_id:
        vehicle = Vehicle.objects.get(pk=vehicle_id)
        vehicle_driver = vehicle.current_vehicle_driver
        vehicle = vehicle_driver.vehicle
        add_vehicle_driver_form = AddVehicleDriverForm(
            request.POST or None, instance=vehicle_driver)
    else:
        add_vehicle_driver_form = AddVehicleDriverForm(request.POST or None)

    if add_vehicle_driver_form.is_valid():
        if vehicle_driver.end_date:
            if vehicle_driver.start_date < vehicle_driver.end_date:
                vehicle_driver = add_vehicle_driver_form.save(commit=False)
                vehicle_driver.created_by = request.user
                vehicle_driver.save()

                status_type = VehicleStatusType.objects.filter(description="Unallocated").first()
                comment = "Vehicle was unasigned from driver, status changed to %s"%(status_type)

                if status_type is not None and comment !="" and vehicle_driver.vehicle:
                    vehicle_status = change_vehicle_status(request, vehicle_driver.vehicle, status_type, comment)

                return redirect(reverse('fleetmanagement:edit_vehicle', kwargs={'vehicle_id': vehicle_id}) + "#vehicle_driver")
            else:
                messages.error(request, 'End date should be greater than start date')
        else:
            messages.error(request, 'Please select end date')
    context['add_vehicle_driver_form'] = add_vehicle_driver_form
    context['vehicle_driver'] = vehicle_driver
    return render(request, template, context)

@login_required
def unassign_fuel_card(request, fuel_card_id):
    fuel_card = FuelCard.objects.get(pk=fuel_card_id)
    vehicle = fuel_card.vehicle.id

    fuel_card.vehicle = None
    fuel_card.save()

    return redirect(reverse('fleetmanagement:edit_vehicle', kwargs={'vehicle_id': vehicle}) + "#fuel_card")

@login_required
def vehicle_makes(request, template="fleet_management/vehicle_makes.html", context=None):
    context = context or {}

    vehicle_makes = VehicleMake.objects.all()

    filter_form = VehicleMakeFilterForm(request.POST or None)
    if u'search' in request.POST:
        if filter_form.is_valid():
            vehicle_makes = filter_form.filter(vehicle_makes)

    if u'extract' in request.POST:
        if filter_form.is_valid():
            vehicle_makes = filter_form.filter(vehicle_makes)
            download_thread = threading.Thread(target=extract_vehicle_makes_data,
                                               args=(request.user, "vehicle_makes", vehicle_makes,
                                                     filter_form.cleaned_data))

            download_thread.start()
            messages.success(request, 'Your extract has been added to the download queue. Queue processing may take a while. Check your report in downloads.')

    context['vehicle_makes'] = vehicle_makes
    context['filter_form'] = filter_form

    return render(request, template, context)

@login_required
def edit_vehicle_make(request,  make_id=None, template="fleet_management/edit_vehicle_make.html", context=None):

    context = context or {}
    make = None

    if make_id:
        make = VehicleMake.objects.get(pk=make_id)
        make_form = VehicleMakeForm(request.POST or None, instance=make)

    else:
        make_form = VehicleMakeForm(request.POST or None)

    if make_form.is_valid():
        make = make_form.save(commit=False)
        make.created_by = request.user
        make.save()

        return redirect(reverse('fleetmanagement:view_vehicle_makes'))

    context['make_form'] = make_form
    context['make'] = make

    return render(request, template, context)


@login_required
def vehicle_models(request, template="fleet_management/vehicle_models.html", context=None):
    context = context or {}

    vehicle_models = VehicleModel.objects.all().order_by('make__make_name', 'model_name')

    filter_form = VehicleModelFilterForm(request.POST or None)
    if u'search' in request.POST:
        if filter_form.is_valid():
            vehicle_models = filter_form.filter(vehicle_models)

    if u'extract' in request.POST:
        if filter_form.is_valid():
            vehicle_models = filter_form.filter(vehicle_models)
            download_thread = threading.Thread(target=extract_vehicle_models_data,
                                               args=(request.user, "vehicle_models", vehicle_models,
                                                     filter_form.cleaned_data))

            download_thread.start()
            messages.success(request, 'Your extract has been added to the download queue. Queue processing may take a while. Check your report in downloads.')

    context['vehicle_models'] = vehicle_models
    context['filter_form'] = filter_form

    return render(request, template, context)

@login_required
def edit_vehicle_model(request,  make_id=None, model_id=None, template="fleet_management/edit_vehicle_model.html", context=None):

    context = context or {}
    make = None
    model = None

    if model_id:
        model = VehicleModel.objects.get(pk=model_id)
        model_form = VehicleModelForm(request.POST or None, instance=model)

    elif make_id and not model_id:
        make = VehicleMake.objects.get(pk=make_id)
        model = VehicleModel(make=make)
        model_form = VehicleModelForm(request.POST or None, instance=model)
    else:
        model_form = VehicleModelForm(request.POST or None,)

    if model_form.is_valid():
        model = model_form.save(commit=False)
        model.created_by = request.user
        model.save()

        if make_id and not model_id:
            return redirect(reverse('fleetmanagement:view_vehicle_makes'))
        else:
            return redirect(reverse('fleetmanagement:view_vehicle_models'))

    context['model_form'] = model_form
    context['model'] = model

    return render(request, template, context)

@login_required
def insurance_claims(request, template="fleet_management/view_insurance_claims.html", context=None):
    context = context or {}

    insurance_claims = InsuranceClaim.objects.all()

    filter_form = InsuranceClaimFilterForm(request.GET or None)

    if u'search' in request.GET or u'extract' in request.GET:

        if filter_form.is_valid():
            insurance_claims = filter_form.filter(insurance_claims)

    if u'extract' in request.GET:
        download_thread = threading.Thread(target=extract_insurance_claims_data,
                                           args=(request.user, "insurance claims",insurance_claims,
                                                 filter_form.cleaned_data))

        download_thread.start()
        messages.success(request, 'Your extract has been added to the download queue. Queue processing may take a while. Check your report in downloads.')

    context['insurance_claims'] = insurance_claims
    context['filter_form'] = filter_form

    return render(request, template, context)

@login_required
def edit_insurance_claim(request, insurance_claim_id=None, document_name=None, template="fleet_management/edit_insurance_claim.html", context=None):

    context = context or {}
    insurance_claim = None
    insurance_claim = InsuranceClaim.objects.get(pk=insurance_claim_id) if insurance_claim_id else None

    insurance_claim_documents = InsuranceClaimDocument.objects.filter(insurance_claim_id=insurance_claim_id)
    documents = Document.objects.all()
    insurance_claim_comments = InsuranceClaimComment.objects.filter(insurance_claim_id=insurance_claim_id)

    if insurance_claim:
        insurance_claim = InsuranceClaim.objects.get(pk=insurance_claim_id)
        insurance_claim_form = InsuranceClaimForm(request.POST or None, instance=insurance_claim)

        status=insurance_claim.status
    else:
        insurance_claim_form = InsuranceClaimForm(request.POST or None)

    insurance_claim_document_form = InsuranceClaimDocumentForm(request.POST or None, prefix='documents')      
    insurance_claim_file_form = InsuranceClaimFileForm(request.POST or None, request.FILES or None, prefix="documents" if not document_name else None)
    insurance_claim_comment_form = CommentForm(request.POST or None, prefix="comment")

    if u'captured' in request.POST:
            status = "captured"
        
    if u'rejected' in request.POST:
        status = "rejected"

    if u'submit_for_payment' in request.POST:
        status = "submitted for payment"

    if u'paid' in request.POST:
        status = "paid"
        
    if insurance_claim_form.is_valid():
        insurance_claim = insurance_claim_form.save(commit=False)
        insurance_claim.created_by = request.user 
        insurance_claim.status = status
        vehicle_driver = VehicleDriver.objects.filter(vehicle = insurance_claim_form.cleaned_data['vehicle'],
                                                      start_date__lte=insurance_claim_form.cleaned_data['incident_date'])\
                                              .filter(Q(end_date__gte=insurance_claim.incident_date) |
                                                      Q(end_date=None)).first()

        if vehicle_driver:
            insurance_claim.vehicle_driver = vehicle_driver
            insurance_claim.driver = vehicle_driver.driver

        if insurance_claim and insurance_claim.driver_co_payment=='no':
            insurance_claim.percentage = None
            insurance_claim.share_amount = None

        insurance_claim.save()
        status_type = VehicleStatusType.objects.filter(description="Insurance Claim").first()
        comment = "Vehicle insurance claim captured, status changed to %s"%(status_type)

        if status_type is not None and comment !="" and vehicle:
            vehicle_status = change_vehicle_status(request, vehicle, status_type, comment)
 
        if insurance_claim_comment_form.has_changed() and insurance_claim_comment_form.is_valid():
            comment = insurance_claim_comment_form.save(commit=False)
            if comment.comment is not None or comment.comment != "":
                comment.save()
                insurance_claim_comment = InsuranceClaimComment.objects.create(insurance_claim_id=insurance_claim.id, 
                                                                    comment_id=comment.id, 
                                                                    created_by_id=request.user.id)

        if insurance_claim_file_form.is_valid():

            document = insurance_claim_file_form.save(commit=False)
            document.document_name = document.document.name
            document.file_type = 'document'
            document.description = 'insurance claim file'
            if document.document_name is not None and insurance_claim_document_form.is_valid():
                document.save()

                insurance_claim_document = insurance_claim_document_form.save(commit=False)
                insurance_claim_document.insurance_claim = insurance_claim
                insurance_claim_document.document = document
                insurance_claim_document.created_by = request.user
                insurance_claim_document.save()
                insurance_claim_document_form.save_m2m()

                return redirect(reverse('fleetmanagement:view_insurance_claims'))

            else:

                return redirect(reverse('fleetmanagement:view_insurance_claims'))

        else:
            return redirect(reverse('fleetmanagement:view_insurance_claims'))


    context['insurance_claim_form'] = insurance_claim_form
    context['insurance_claim'] = insurance_claim
    context['insurance_claim_file_form'] = insurance_claim_file_form
    context['insurance_claim_documents'] = insurance_claim_documents
    context['documents'] = documents
    context['insurance_claim_document_form'] = insurance_claim_document_form
    context['insurance_claim_comment_form'] = insurance_claim_comment_form
    context['insurance_claim_comments'] = insurance_claim_comments

    return render(request, template, context)


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)

@login_required
def mileage_uploads(request, template="fleet_management/mileage_uploads.html"):
    context = {}

    form = MileageImportForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        import_mileage_data(request.user, form.cleaned_data.get('mileage_file'))

    context['form'] = form

    return render(request, template, context)

@login_required
def additional_vehicle_information_uploads(request, template="fleet_management/additional_vehicle_information_uploads.html"):
    context = {}

    form = AdditionalVehicleInformationImportForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        import_additional_vehicle_information_data(request.user, form.cleaned_data.get('additional_information_file'))

    context['form'] = form

    return render(request, template, context)

@login_required
def fuel_cards_upload(request, template="fleet_management/fuel_cards_upload.html"):
    context = {}

    form = FuelCardImportForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        import_fuel_cards_data(request.user, form.cleaned_data.get('fuel_card_file'))

    context['form'] = form

    return render(request, template, context)

def vehicle_service_due(req, template="fleet_management/vehicle_service_due.html"):
    serv_int = 0

    vehicles = Vehicle.objects.exclude(ownership__iexact='rental') \
                              .exclude(updated_mileage__isnull=True) 

    for vehicle in vehicles:
        serv_int = vehicle.updated_mileage / vehicle.service_interval
        if (vehicle.updated_mileage -(vehicle.service_interval * serv_int)) <= (vehicle.service_interval - settings.SERVICE_CHECK):
            vehicles = vehicles.exclude(pk=vehicle.pk)

        servicebook = ServiceBooking.objects.filter(vehicle=vehicle).last()
        if servicebook and servicebook.service_date:
            if servicebook.current_mileage + (vehicle.service_interval - settings.SERVICE_CHECK) > vehicle.updated_mileage:
                vehicles = vehicles.exclude(pk=vehicle.pk)
                
    context = {}

    title = "Vehicle Service Due"


    if u'extract' in req.GET:
        download_thread = threading.Thread(target=extract_vehicle_service_due_data,
                                           args=(req.user,vehicles))
        download_thread.start()        
        messages.success(req, 'Extract has been added to the download queue. Check the downloads page for your report download.')

    context['title']  = title
    context['vehicles'] = vehicles
    context['allow_extract'] = True

    return render(req, template, context)
