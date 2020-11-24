from django import http
from django.template.loader import render_to_string, get_template
from django.template import RequestContext, Context
from django.conf import settings
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from django.core.mail import send_mail, EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, render_to_response
from django.core.urlresolvers import reverse
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from datetime import datetime, timedelta, date
from django.views.decorators.csrf import csrf_exempt
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
from forms import *
import csv
import os
from xhtml2pdf import pisa
import cStringIO as StringIO
import cgi
from .forms import  addNewVehicleForm, fileUploadForm, AddInsuranceClaimForm, \
                    IncidentForm,RenewLicenceDiskForm, FuelCardForm, FuelAllocationForm,  \
                    MileageLogForm, MaintenanceForm, VehicleAllocationForm, RequisitionItemForm, RequisitionForm, \
                    ServiceBookingForm, TrafficfineForm, tripImportUploadForm
from .models import Vehicle, FileUpload, RenewLicenceDisk, Comment,  \
                    InsuranceClaim, VehicleAllocation, FuelCard, FuelAllocation, \
                    ServiceBooking, Trafficfine, MileageLog, TripLog, Trip,\
                    VehicleMaintenance,Incident, Requisition, RequisitionItem
from employees.models import *
from offices.models import *
from django.db.models import Count, Sum, Q
import collections
import json
from sms.sms_helper import *

def handler400(request):
    response = render_to_response('400.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 400
    return response

def handler403(request):
    response = render_to_response('403.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 403
    return response

def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response


@login_required
@permission_required('fleet.view_reports', raise_exception=True)
def rpt_driver_incidences(request):

    title='Driver Incidences Report'

    filter_form = TransactionsFilterForm(request.POST or None)

    employees = None

    if filter_form.is_valid():
        date_from = filter_form.cleaned_data.get('start_date', filter_form.initial.get('start_date'))
        date_to = filter_form.cleaned_data.get('end_date', filter_form.initial.get('end_date'))
        f_term = filter_form.cleaned_data.get('driver', None)
        r_term = filter_form.cleaned_data.get('region', None)
        employees = Employee.objects
        if f_term:
            employees = employees.filter(first_name__icontains=f_term).order_by('branch__region', 'first_name')            
        if r_term:
            region = Region.objects.filter(region__icontains=r_term)
            employees = employees.filter(branch__region=region).order_by('branch__region', 'first_name')

        employees = employees.filter(driver_incidences__incident_date__range=[date_from, date_to])

    if employees is None:
        date_from = filter_form.initial.get('start_date')
        date_to = filter_form.initial.get('end_date')
        employees = Employee.objects.filter(driver_incidences__incident_date__range=[date_from, date_to])

    tran_dict = {}
    for employee in employees:
        if not tran_dict.get(employee.full_name, None):
            tran_dict[employee.full_name] = {}

        logs = employee.driver_incidences.filter(incident_date__range=[date_from, date_to]).order_by('incident_date')

        transactions = [{'incident_date': log.incident_date, 'vehicle': log.vehicle.vehicle,
                     'incident_type': log.incident_type, 'location': log.location,
                     'status': log.damage_extent, 'description': log.Description} for log in logs]


        tran_dict[employee.full_name] = {'transactions': transactions}

    if request.POST.get('report', None) and filter_form.is_valid():
        date_from = filter_form.cleaned_data.get('start_date', filter_form.initial.get('start_date')).replace(day=1)
        date_to = filter_form.cleaned_data.get('end_date', filter_form.initial.get('end_date'))
        response = HttpResponse(content_type='text/csv')
        filename = "rpt_driver_incidences.csv"
        response['Content-Disposition'] = 'attachment; filename='+filename
        writer = csv.writer(response)

        writer.writerow(["Vehicle Incidences Report"])
        writer.writerow(["Date From:",date_from,"Date To:",date_to])


        for employee, values in tran_dict.items():
            writer.writerow([employee])
            headers = ["Incident Date","Vehicle","Incident Type","Location","Description","Status"]
            writer.writerow(headers)

            for val in values.get('transactions'):
                writer.writerow([val.get('incident_date'), val.get('vehicle'), val.get('incident_type'), val.get('location'),
                                 val.get('description'), val.get('status')])

        return response

    context ={
        'filter_form': filter_form,
        'title': title,
        'tran_dict':tran_dict
    }

    return render(request, "rpt_driver_incidences.html", context)

@login_required
@permission_required('fleet.view_reports', raise_exception=True)
def rpt_vehicle_incidences(request):
    title='Vehicle Incidences Report'
    filter_form = TransactionsFilterForm(request.POST or None)

    vehicles = None
    if filter_form.is_valid():
        date_from = filter_form.cleaned_data.get('start_date', filter_form.initial.get('start_date'))
        date_to = filter_form.cleaned_data.get('end_date', filter_form.initial.get('end_date'))
        term = filter_form.cleaned_data.get('vehicle')

        vehicles = Vehicle.objects
        if term:
            vehicles = vehicles.filter(vehicle=term)

        vehicles = vehicles.filter(vehicle_incidences__incident_date__range=[date_from, date_to])

    if vehicles is None:
        date_from = filter_form.initial.get('start_date')
        date_to = filter_form.initial.get('end_date')
        vehicles = Vehicle.objects.filter(vehicle_incidences__incident_date__range=[date_from, date_to])

    tran_dict = {}
    for vehicle in vehicles:
        if not tran_dict.get(vehicle.vehicle, None):
            tran_dict[vehicle.vehicle] = {}

        logs = vehicle.vehicle_incidences.filter(incident_date__range=[date_from, date_to]).order_by('incident_date')

        transactions = [{'incident_date': log.incident_date, 'driver': log.driver.full_name,
                     'incident_type': log.incident_type, 'location': log.location,
                     'status': log.damage_extent, 'description': log.Description} for log in logs]


        tran_dict[vehicle.vehicle] = {'transactions': transactions, 'make': vehicle.make_n_model}

    if request.POST.get('report', None) and filter_form.is_valid():
        date_from = filter_form.cleaned_data.get('start_date', filter_form.initial.get('start_date')).replace(day=1)
        date_to = filter_form.cleaned_data.get('end_date', filter_form.initial.get('end_date'))
        response = HttpResponse(content_type='text/csv')
        filename = "rpt_vehicle_incidences.csv"
        response['Content-Disposition'] = 'attachment; filename='+filename
        writer = csv.writer(response)

        writer.writerow(["Vehicle Incidences Report"])
        writer.writerow(["Date From:",date_from,"Date To:",date_to])


        for vehicle, values in tran_dict.items():
            writer.writerow([values.get('make'),vehicle])
            headers = ["Incident Date","Driver","Incident Type","Location","Description","Status"]
            writer.writerow(headers)

            for val in values.get('transactions'):
                writer.writerow([val.get('incident_date'), val.get('driver'), val.get('incident_type'), val.get('location'),
                                 val.get('description'), val.get('status')])

        return response

    context ={
        'vehicles': vehicles,
        'filter_form': filter_form,
        'title': title,
        'tran_dict':tran_dict
    }

    return render(request, "rpt_vehicle_incidences.html", context)



@login_required
@permission_required('fleet.view_reports', raise_exception=True)
def rpt_vehicle_insurance_claims(request):
    title='Vehicle Insurance Claims Report'
    vehicles = Vehicle.objects.all()

    if request.POST.get('report', None):

        response = HttpResponse(content_type='text/csv')
        filename = "rpt_vehicle_maintenance.csv"
        response['Content-Disposition'] = 'attachment; filename='+filename
        writer = csv.writer(response)

        writer.writerow(["Vehicle Insurance Claims Report"])
        headers = ["Driver","Vehicle","Make And Model","All Claims","Pending","Finalized","Rejected","Total Claims","Total Excess"]
        writer.writerow(headers)

        for vehicle in vehicles:
            writer.writerow([vehicle.get_current_driver(), vehicle.vehicle, vehicle.make_n_model,vehicle.get_count_claims(),
                             vehicle.get_count_claims_pending(), vehicle.get_count_claims_finalized(),
                             vehicle.get_count_claims_rejected(),vehicle.get_total_claims(), vehicle.get_total_excess()])

        return response

    context ={
        'vehicles': vehicles,
        'title': title,

    }

    return render(request, "rpt_vehicle_insurance_claims.html", context)



@login_required
@permission_required('fleet.view_reports', raise_exception=True)
def rpt_vehicle_maintenance(request):
    title='Vehicle Maintenance Cost Report'
    vehicles = Vehicle.objects.all()

    if request.POST.get('report', None):

        response = HttpResponse(content_type='text/csv')
        filename = "rpt_vehicle_maintenance.csv"
        response['Content-Disposition'] = 'attachment; filename='+filename
        writer = csv.writer(response)

        writer.writerow(["Vehicle Maintenance Report"])
        headers = ["Driver","Vehicle","Make And Model","Mileage","Incidences","Repairs Cost","Tyres Cost","Service Cost","Total Maintenance","Status"]
        writer.writerow(headers)

        for vehicle in vehicles:
            writer.writerow([vehicle.get_current_driver(), vehicle.vehicle, vehicle.make_n_model,vehicle.get_current_mileage(),
                             vehicle.get_count_incidences(), vehicle.get_total_maintenance(),vehicle.get_total_tyres_cost(),
                             vehicle.get_total_service_cost(),vehicle.get_total_maintenance_cost(), vehicle.status])

        return response

    context ={
        'vehicles': vehicles,
        'title': title,

    }

    return render(request, "rpt_vehicle_maintenance.html", context)



@login_required
@permission_required('fleet.view_reports', raise_exception=True)
def rpt_vehicle_traffic_fines(request):
    title='Vehicle Traffic Fines Report'
    vehicles = Vehicle.objects.filter(~Q(ownership_type="EL Staff"), active=True).order_by('current_driver__branch__region__region', 'current_driver__first_name')
    historical_vehicles = Vehicle.objects.filter(~Q(ownership_type="EL Staff"), active=False).order_by('current_driver__branch__region__region', 'current_driver__first_name')
    date = 'purchase_date'
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_list' in request.GET and filter_form.is_valid():
        vehicles = filter_form.filter(vehicles, date)
        historical_vehicles = filter_form.filter(historical_vehicles, date)
    if request.POST.get('report', None):

        response = HttpResponse(content_type='text/csv')
        filename = "rpt_vehicle_traffic_fines.csv"
        response['Content-Disposition'] = 'attachment; filename='+filename
        writer = csv.writer(response)

        writer.writerow(["Vehicle Traffic Fines Report"])
        headers = ["Driver","Vehicle","Make And Model","Region","All Fines","Paid","Pending","Seriouse","Courts","Total Fines"]
        writer.writerow(headers)

        for vehicle in vehicles:
            writer.writerow([vehicle.get_current_driver(), vehicle.vehicle, vehicle.make_n_model,vehicle.get_current_driver().branch.region,vehicle.get_count_fines(),
                             vehicle.get_count_fines_paid(), vehicle.get_count_fines_pending(),vehicle.get_count_fines_serious(),
                             vehicle.get_count_fines_court(),vehicle.get_total_fines()])
        
        writer.writerow(["Historical Vehicle Traffic Fines Report"])
        headers = ["Driver","Vehicle","Make And Model","Region","All Fines","Paid","Pending","Seriouse","Courts","Total Fines"]
        writer.writerow(headers)

        for vehicle in vehicles:
            writer.writerow([vehicle.get_current_driver(), vehicle.vehicle, vehicle.make_n_model,vehicle.get_current_driver().branch.region,vehicle.get_count_fines(),
                             vehicle.get_count_fines_paid(), vehicle.get_count_fines_pending(),vehicle.get_count_fines_serious(),
                             vehicle.get_count_fines_court(),vehicle.get_total_fines()])
        return response

    context ={
        'vehicles': vehicles,
        "historical_vehicles":historical_vehicles,
        "filter_form":filter_form,
        'title': title,

    }

    return render(request, "rpt_vehicle_traffic_fines.html", context)



@login_required
@permission_required('fleet.view_reports', raise_exception=True)
def rpt_driver_traffic_fines(request):

    title='Driver Traffic Fines Report'

    filter_form = TransactionsFilterForm(request.POST or None)

    employees = None

    if filter_form.is_valid():
        date_from = filter_form.cleaned_data.get('start_date', filter_form.initial.get('start_date'))
        date_to = filter_form.cleaned_data.get('end_date', filter_form.initial.get('end_date'))
        f_term = filter_form.cleaned_data.get('driver', None)
        r_term = filter_form.cleaned_data.get('region', None)
        employees = Employee.objects
        if f_term:
            employees = employees.filter(first_name__icontains=f_term).order_by('branch__region', 'first_name')            
        if r_term:
            region = Region.objects.filter(region__icontains=r_term)
            employees = employees.filter(branch__region=region).order_by('branch__region', 'first_name')

        employees = employees.filter(driver_trafficFines__offence_date__range=[date_from, date_to]).order_by('branch__region', 'first_name')

    if employees is None:
        date_from = filter_form.initial.get('start_date')
        date_to = filter_form.initial.get('end_date')
        employees = Employee.objects.filter(driver_trafficFines__offence_date__range=[date_from, date_to])

    tran_dict = {}
    for employee in employees:

        if not tran_dict.get(employee.first_name, None):
            tran_dict[employee.first_name] = {}

        logs = employee.driver_trafficFines.filter(offence_date__range=[date_from, date_to]).order_by('-offence_date')
        transactions = []
        for log in logs:
            attachs = FileUpload.objects.filter(vehicle=log.vehicle, transaction_id=log.id, transaction="Trafficfine",)
            fine = {'offence_date': log.offence_date, 'time': log.offence_time, 'vehicle': log.vehicle.vehicle,
                     'notice_number': log.notice_number, 'due_date': log.due_date,
                     'location': log.location, 'region': log.driver.branch.region, 'amount': log.amount, 
                     'description': log.description, 'attachs': attachs,}
            transactions.append(fine)
       
        totals = {'amount': sum(logs.values_list('amount', flat=True))}               


        tran_dict[employee.first_name] = {'transactions': transactions, 'totals': totals}

    if request.POST.get('report', None) and filter_form.is_valid():
        date_from = filter_form.cleaned_data.get('start_date', filter_form.initial.get('start_date')).replace(day=1)
        date_to = filter_form.cleaned_data.get('end_date', filter_form.initial.get('end_date'))
        response = HttpResponse(content_type='text/csv')
        filename = "rpt_driver_traffic_fines.csv"
        response['Content-Disposition'] = 'attachment; filename='+filename
        writer = csv.writer(response)

        writer.writerow(["Driver Traffic Fines Report"])      
        writer.writerow(["Date From:",date_from,"Date To:",date_to])        

        for employee, values in tran_dict.items():
            writer.writerow([employee])
            headers = ["Vehicle","Notice Number","Offence Date","Time","Due Date","Location","Region","Description","Amount"]
            writer.writerow(headers)

            for val in values.get('transactions'):
                writer.writerow([val.get('vehicle'), val.get('notice_number'), val.get('offence_date'), val.get('time'),
                                 val.get('due_date'), val.get('location'), val.get('region'), val.get('description'), val.get('amount'),
                                 [settings.BASE_URL+item.file.url for item in val.get('attachs')]])

            writer.writerow(["Totals","","","","","","","",values.get('totals').get('amount'),""])

        return response

    context ={
        'employees': employees,
        'filter_form': filter_form,
        'title': title,
        'tran_dict':tran_dict
    }

    return render(request, "rpt_driver_traffic_fines.html", context)


@login_required
@permission_required('fleet.view_reports', raise_exception=True)
def rpt_licence_disks_due(request):

    title="Vehicle Licencing Due Report"
    due_expiry_date = datetime.now() + timedelta(+30)
    expired_date = datetime.now() + timedelta(-1)
    todays_date = datetime.now()+ timedelta()

    vehicles_due = Vehicle.objects.filter(~Q(ownership_type="EL Staff"),active=True, licence_disk_expiry__lte=expired_date)
    date = 'licence_disk_expiry'
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_list' in request.GET and filter_form.is_valid():
        vehicles_due = filter_form.filter(vehicles_due, date)

    if request.POST.get('report', None):

        response = HttpResponse(content_type='text/csv')
        filename = "rpt_vehicle_service_due.csv"
        response['Content-Disposition'] = 'attachment; filename='+filename
        writer = csv.writer(response)

        writer.writerow(["Vehicle Service Due Report"])
        headers = ["Driver","Vehicle","Make And Model","Model Year", "Region","Last Renewed","Expiring On","Status"]
        writer.writerow(headers)
        for vehicle in vehicles_due:
            writer.writerow([vehicle.get_current_driver(), vehicle.vehicle, vehicle.make_n_model,vehicle.model_year, vehicle.get_current_driver().branch.region,
                             vehicle.get_last_Licence_renewal_date(), vehicle.licence_disk_expiry,
                             vehicle.status])

        return response
    context = {
        "title": title,
        "licencing_list":vehicles_due,
        "filter_form":filter_form,
    }
    return render(request, "rpt_licencing.html", context)


@login_required
@permission_required('fleet.view_reports', raise_exception=True)
def rpt_licence_disks_expired(request):

    title="Vehicle Licencing Expired Report"
    due_expiry_date = datetime.now() + timedelta(+30)
    expired_date = datetime.now() + timedelta(-1)
    todays_date = datetime.now()+ timedelta()

    vehicles_expired = Vehicle.objects.filter(~Q(ownership_type="EL Staff"),active=True, licence_disk_expiry__lte=expired_date)
    date = 'licence_disk_expiry'
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_list' in request.GET and filter_form.is_valid():
        vehicles_expired = filter_form.filter(vehicles_expired, date)

    if request.POST.get('report', None):

        response = HttpResponse(content_type='text/csv')
        filename = "rpt_vehicle_service_due.csv"
        response['Content-Disposition'] = 'attachment; filename='+filename
        writer = csv.writer(response)

        writer.writerow(["Vehicle Service Due Report"])
        headers = ["Driver","Vehicle","Make And Model","Model Year","Region","Last Renewed","Expiring On","Status"]
        writer.writerow(headers)
        for vehicle in vehicles_expired:
            writer.writerow([vehicle.get_current_driver(), vehicle.vehicle, vehicle.make_n_model,vehicle.model_year,vehicle.get_current_driver().branch.region,
                             vehicle.get_last_Licence_renewal_date(), vehicle.licence_disk_expiry, vehicle.status])

        return response
    context = {
        "title": title,
        "licencing_list":vehicles_expired, 
        "filter_form":filter_form,
    }
    return render(request, "rpt_licencing.html", context)


@login_required
@permission_required('fleet.view_reports', raise_exception=True)
def rpt_service_due(request):

    title="Vehicle Service Due Report"
    vehicles = Vehicle.objects.filter(~Q(ownership_type="EL Staff"),active=True,)
    date = 'purchase_date'
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_list' in request.GET and filter_form.is_valid():
        vehicles = filter_form.filter(vehicles, date)
    service_due = []
    for v in vehicles:
        if v.get_next_service_mileage() - v.get_current_mileage() < 1400 and v.get_next_service_mileage() > v.get_current_mileage():
            service_due.append(v)

    if request.POST.get('report', None):

        response = HttpResponse(content_type='text/csv')
        filename = "rpt_vehicle_service_due.csv"
        response['Content-Disposition'] = 'attachment; filename='+filename
        writer = csv.writer(response)

        writer.writerow(["Vehicle Service Due Report"])
        headers = ["Driver","Vehicle","Make And Model","Model Year","Last Services","Current Mileage","Service Mileage","Status"]
        writer.writerow(headers)

        for vehicle in service_due:
            writer.writerow([vehicle.get_current_driver(), vehicle.vehicle, vehicle.make_n_model,vehicle.model_year,
                             vehicle.get_last_service_mileage(), vehicle.get_current_mileage(),vehicle.get_next_service_mileage(),
                             vehicle.status])

        return response

    context = {
        "title": title,
        "service_list":service_due,
        "filter_form":filter_form,
    }
    return render(request, "rpt_service.html", context)


@login_required
@permission_required('fleet.view_reports', raise_exception=True)
def rpt_service_overdue(request):

    title="Vehicle Service Overdue Report"
    vehicles = Vehicle.objects.filter(~Q(ownership_type="EL Staff"),active=True,)
    date = 'purchase_date'
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_list' in request.GET and filter_form.is_valid():
        vehicles = filter_form.filter(vehicles, date)
    service_over_due =[]
    for vkl in vehicles:
        if vkl.get_next_service_mileage() < vkl.get_current_mileage():
            service_over_due.append(vkl)

    if request.POST.get('report', None):

        response = HttpResponse(content_type='text/csv')
        filename = "rpt_vehicle_service_due.csv"
        response['Content-Disposition'] = 'attachment; filename='+filename
        writer = csv.writer(response)

        writer.writerow(["Vehicle Service Due Report"])
        headers = ["Driver","Vehicle","Make And Model","Model Year","Last Services","Current Mileage","Service Mileage","Status"]
        writer.writerow(headers)

        for vehicle in service_over_due:
            writer.writerow([vehicle.get_current_driver(), vehicle.vehicle, vehicle.make_n_model,vehicle.model_year,
                             vehicle.get_last_service_mileage(), vehicle.get_current_mileage(),vehicle.get_next_service_mileage(),
                             vehicle.status])

        return response
    context = {
        "title": title,
        "service_list":service_over_due,
        "filter_form":filter_form,
    }
    return render(request, "rpt_service.html", context)


@login_required
@permission_required('fleet.view_reports', raise_exception=True)
def rpt_driver_mileages(request):

    title='Driver Mileage Report'
    filter_form = TransactionsFilterForm(request.POST or None)

    employees = None

    if filter_form.is_valid():
        date_from = filter_form.cleaned_data.get('start_date', filter_form.initial.get('start_date'))
        date_to = filter_form.cleaned_data.get('end_date', filter_form.initial.get('end_date'))
        f_term = filter_form.cleaned_data.get('driver', None)
        r_term = filter_form.cleaned_data.get('region', None)
        employees = Employee.objects
        if f_term:
            employees = employees.filter(first_name__icontains=f_term).order_by('branch__region', 'first_name')            
        if r_term:
            region = Region.objects.filter(region__icontains=r_term)
            employees = employees.filter(branch__region=region).order_by('branch__region', 'first_name')

        employees = employees.filter(driver_mileageLogs__log_date__range=[date_from, date_to])


    if employees is None:
        date_from = filter_form.initial.get('start_date')
        date_to = filter_form.initial.get('end_date')
        employees = Employee.objects.filter(driver_mileageLogs__log_date__range=[date_from, date_to])

    tran_dict = {}
    for employee in employees:
        if not tran_dict.get(employee.full_name, None):
            tran_dict[employee.full_name] = {}

        logs = employee.driver_mileageLogs.filter(log_date__range=[date_from, date_to]).order_by('log_date')

        transactions = [{'log_date': log.log_date, 'vehicle': log.vehicle.vehicle,
                         'starting_km': log.starting_mileage, 'current_km': log.current_mileage,
                         'mileage': log.mileage, 'fuel_ob': log.fuel_balance_bf,
                         'fuel_used': log.fuel_used, 'fuel_cb': log.fuel_balance,
                         'status': log.status} for log in logs]

        totals = {'mileage': sum(logs.values_list('mileage', flat=True)),
                  'fuel_used': sum(logs.values_list('fuel_used', flat=True))}

        tran_dict[employee.full_name] = {'transactions': transactions, 'totals': totals}

    if request.POST.get('report', None) and filter_form.is_valid():
        date_from = filter_form.cleaned_data.get('start_date', filter_form.initial.get('start_date')).replace(day=1)
        date_to = filter_form.cleaned_data.get('end_date', filter_form.initial.get('end_date'))
        response = HttpResponse(content_type='text/csv')
        filename = "rpt_driver_mileages.csv"
        response['Content-Disposition'] = 'attachment; filename='+filename
        writer = csv.writer(response)

        writer.writerow(["Driver Mileage Report"])
        writer.writerow(["Date From:",date_from,"Date To:",date_to])


        for employee, values in tran_dict.items():
            writer.writerow([employee])
            headers = ["Log Date","Vehicle","Starting KM","Current KM","Mileage","Fuel OB","Fuel Used","Fuel CB","Status"]
            writer.writerow(headers)

            for val in values.get('transactions'):
                writer.writerow([val.get('log_date'), val.get('vehicle'), val.get('starting_km'), val.get('current_km'),
                                 val.get('mileage'), val.get('fuel_ob'), val.get('fuel_used'), val.get('fuel_cb'), val.get('status')])

            writer.writerow(["","","","Totals",values.get('totals').get('mileage'),"",values.get('totals').get('fuel_used'),"",""])


        return response


    context ={
        'employees': employees,
        'filter_form': filter_form,
        'title': title,
        'tran_dict':tran_dict
    }

    return render(request, "rpt_driver_mileages.html", context)



@login_required
@permission_required('fleet.view_reports', raise_exception=True)
def rpt_mileage_aggregates(request):
    title='Vehicle Mileage Aggregates Report'
    vehicles = Vehicle.objects.filter(~Q(ownership_type="EL Staff"),active=True,).order_by('current_driver__branch__region__region', 'current_driver__first_name')
    historical_vehicles = Vehicle.objects.filter(~Q(ownership_type="EL Staff"),active=False,).order_by('current_driver__branch__region__region', 'current_driver__first_name')
    date = 'purchase_date'
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_list' in request.GET and filter_form.is_valid():
        vehicles = filter_form.filter(vehicles, date)
        historical_vehicles = filter_form.filter(historical_vehicles, date)

    if request.POST.get('report', None):

        response = HttpResponse(content_type='text/csv')
        filename = "rpt_vehicle_service_due.csv"
        response['Content-Disposition'] = 'attachment; filename='+filename
        writer = csv.writer(response)

        writer.writerow(["Vehicle Mileage Aggregates Report"])
        headers = ["Current Driver","Vehicle","Make And Model","Region","Current Mileage","Current KM","Current Fuel","Mileage To Date","Fuel To Date"]
        writer.writerow(headers)

        for vehicle in vehicles:
            writer.writerow([vehicle.get_current_driver(), vehicle.vehicle, vehicle.make_n_model,vehicle.get_current_driver().branch.region,vehicle.get_current_mileage(),
                             vehicle.get_monthly_mileage(), vehicle.get_monthly_fuel(),vehicle.get_total_mileage(),
                             vehicle.get_total_fuel()])
        writer.writerow(["Historical Vehicles Mileage Aggregates Report"])
        headers = ["Current Driver","Vehicle","Make And Model","Region","Odometer","This Month KM","This Month Fuel","Mileage To Date","Fuel To Date"]
        writer.writerow(headers)

        for vehicle in historical_vehicles:
            writer.writerow([vehicle.get_current_driver(), vehicle.vehicle, vehicle.make_n_model,vehicle.get_current_driver().branch.region,vehicle.get_current_mileage(),
                             vehicle.get_monthly_mileage(), vehicle.get_monthly_fuel(),vehicle.get_total_mileage(),
                             vehicle.get_total_fuel()])
        return response

    context ={
        'vehicles': vehicles, 
        'historical_vehicles': historical_vehicles, 
        'filter_form': filter_form,
        'title': title,

    }

    return render(request, "rpt_mileage_aggregates.html", context)



@login_required
@permission_required('fleet.view_reports', raise_exception=True)
def rpt_vehicle_mileages(request):

    title='Vehicle Mileage Report'
    filter_form = TransactionsFilterForm(request.POST or None)

    vehicles = None
    if filter_form.is_valid():
        date_from = filter_form.cleaned_data.get('start_date', filter_form.initial.get('start_date'))
        date_to = filter_form.cleaned_data.get('end_date', filter_form.initial.get('end_date'))
        term = filter_form.cleaned_data.get('vehicle')
        r_term = filter_form.cleaned_data.get('region')

        vehicles = Vehicle.objects.order_by('current_driver__branch__region', 'current_driver__first_name')
        if term:
            vehicles = vehicles.filter(vehicle=term)
        if r_term:
            region = Region.objects.filter(region__icontains=r_term)
            vehicles = vehicles.filter(current_driver__branch__region=region)


        vehicles = vehicles.filter(vehicle_mileage_logs__log_date__range=[date_from, date_to])

    if vehicles is None:
        date_from = filter_form.initial.get('start_date')
        date_to = filter_form.initial.get('end_date')
        vehicles = Vehicle.objects.filter(vehicle_mileage_logs__log_date__range=[date_from, date_to]).order_by('current_driver__branch__region', 'current_driver__first_name')

    tran_dict = {}
    for vehicle in vehicles:
        if not tran_dict.get(vehicle.vehicle, None):
            tran_dict[vehicle.vehicle] = {}

        logs = vehicle.vehicle_mileage_logs.filter(log_date__range=[date_from, date_to]).order_by('log_date')

        transactions = [{'log_date': log.log_date, 'driver': log.driver.full_name,
                     'starting_km': log.starting_mileage,'region': log.driver.branch.region, 'current_km': log.current_mileage,
                     'mileage': log.mileage, 'fuel_ob': log.fuel_balance_bf,
                     'fuel_used': log.fuel_used, 'fuel_cb': log.fuel_balance,
                     'status': log.status} for log in logs]

        totals = {'mileage': sum(logs.values_list('mileage', flat=True)),
                  'fuel_used': sum(logs.values_list('fuel_used', flat=True))}

        tran_dict[vehicle.vehicle] = {'transactions': transactions, 'totals': totals, 'make': vehicle.make_n_model}

    if request.POST.get('report', None) and filter_form.is_valid():
        date_from = filter_form.cleaned_data.get('start_date', filter_form.initial.get('start_date')).replace(day=1)
        date_to = filter_form.cleaned_data.get('end_date', filter_form.initial.get('end_date'))
        response = HttpResponse(content_type='text/csv')
        filename = "rpt_vehicle_mileage.csv"
        response['Content-Disposition'] = 'attachment; filename='+filename
        writer = csv.writer(response)

        writer.writerow(["Vehicle Mileage Report"])
        writer.writerow(["Date From:",date_from,"Date To:",date_to])


        for vehicle, values in tran_dict.items():
            writer.writerow([values.get('make'),vehicle])
            headers = ["Log Date","Driver","Region","Starting Km","Current KM","Mileage","Fuel OB","Fuel Used","Fuel CB","Status"]
            writer.writerow(headers)

            for val in values.get('transactions'):
                writer.writerow([val.get('log_date'), val.get('driver') ,val.get('region'), val.get('starting_km'), val.get('current_km'),
                                 val.get('mileage'), val.get('fuel_ob'), val.get('fuel_used'),  val.get('fuel_cb'),  val.get('status')])

            writer.writerow(["Totals","","","","",values.get('totals').get('amount'),"",values.get('totals').get('fuel_used'),"",""])

        return response

    context ={
        'vehicles': vehicles,
        'filter_form': filter_form,
        'title': title,
        'tran_dict':tran_dict
    }

    return render(request, "rpt_vehicle_mileages.html", context)


@login_required
@permission_required('fleet.view_reports', raise_exception=True)
def rpt_vehicle_fuel_allocations(request):

    title='Vehicle Fuel Allocations Report'
    filter_form = TransactionsFilterForm(request.POST or None)

    vehicles = None

    if filter_form.is_valid():
        date_from = filter_form.cleaned_data.get('start_date', filter_form.initial.get('start_date')).replace(day=1)
        date_to = filter_form.cleaned_data.get('end_date', filter_form.initial.get('end_date'))
        term = filter_form.cleaned_data.get('vehicle', None)

        vehicles = Vehicle.objects
        if term:
            vehicles = vehicles.filter(vehicle=term)

        vehicles = vehicles.filter(vehicle_fuelAllocations__allocation_date__range=[date_from, date_to])


    if vehicles is None:
        date_from = filter_form.initial.get('start_date').replace(day=1)
        date_to = filter_form.initial.get('end_date')
        vehicles = Vehicle.objects.filter(vehicle_fuelAllocations__allocation_date__range=[date_from, date_to])

    tran_dict = {}
    for vehicle in vehicles:
        if not tran_dict.get(vehicle.vehicle, None):
            tran_dict[vehicle.vehicle] = {}

        logs = vehicle.vehicle_fuelAllocations.filter(allocation_date__range=[date_from, date_to]).order_by('allocation_date')

        transactions = [{'allocation_date': log.allocation_date, 'driver': log.driver.full_name,
                     'type': log.transaction_type, 'fuel_card': log.fuel_card,
                     'balance_bf': log.balance, 'amount_allocated': log.amount_allocated,
                     'new_balance': log.new_balance, } for log in logs]

        totals = {'amount': sum(logs.values_list('amount_allocated', flat=True))}

        tran_dict[vehicle.vehicle] = {'transactions': transactions, 'totals': totals, 'make': vehicle.make_n_model}

    if request.POST.get('report', None) and filter_form.is_valid():
        date_from = filter_form.cleaned_data.get('start_date', filter_form.initial.get('start_date')).replace(day=1)
        date_to = filter_form.cleaned_data.get('end_date', filter_form.initial.get('end_date'))
        response = HttpResponse(content_type='text/csv')
        filename = "rpt_vehicle_fuel_allocations.csv"
        response['Content-Disposition'] = 'attachment; filename='+filename
        writer = csv.writer(response)

        writer.writerow(["Vehicle Fuel Allocations Report"])
        writer.writerow(["Date From:",date_from,"Date To:",date_to])


        for vehicle, values in tran_dict.items():
            writer.writerow([values.get('make'),vehicle])
            headers = ["Allocation Date","Type","Driver","Fuel Card","Balance BF","Amount ALlocated","New Balance"]
            writer.writerow(headers)

            for val in values.get('transactions'):
                writer.writerow([val.get('allocation_date'), val.get('type'), val.get('driver'), val.get('fuel_card'),
                                 val.get('balance_bf'), val.get('amount_allocated'), val.get('new_balance')])

            writer.writerow(["","","","","Totals",values.get('totals').get('amount'),""])

        return response
    context ={
        'vehicles': vehicles,
        'title': title,
        "filter_form": filter_form,
        'tran_dict':tran_dict,

    }

    return render(request, "rpt_vehicle_fuel_allocations.html", context)


@login_required
@permission_required('fleet.view_reports', raise_exception=True)
def rpt_driver_fuel_allocations(request):

    title='Driver Fuel Allocations Report'
    filter_form = TransactionsFilterForm(request.POST or None)

    employees = None

    if filter_form.is_valid():
        date_from = filter_form.cleaned_data.get('start_date', filter_form.initial.get('start_date'))
        date_to = filter_form.cleaned_data.get('end_date', filter_form.initial.get('end_date'))
        f_term = filter_form.cleaned_data.get('driver', None)
        r_term = filter_form.cleaned_data.get('region', None)
        employees = Employee.objects
        if f_term:
            employees = employees.filter(first_name__icontains=f_term).order_by('branch__region', 'first_name')            
        if r_term:
            region = Region.objects.filter(region__icontains=r_term)
            employees = employees.filter(branch__region=region).order_by('branch__region', 'first_name')

        employees = employees.filter(driver_fuelAllocations__allocation_date__range=[date_from, date_to])


    if employees is None:
        date_from = filter_form.initial.get('start_date')
        date_to = filter_form.initial.get('end_date')
        employees = Employee.objects.filter(driver_fuelAllocations__allocation_date__range=[date_from, date_to])

    tran_dict = {}
    for employee in employees:
        if not tran_dict.get(employee.full_name, None):
            tran_dict[employee.full_name] = {}

        logs = employee.driver_fuelAllocations.filter(allocation_date__range=[date_from, date_to]).order_by('allocation_date')

        transactions = [{'allocation_date': log.allocation_date, 'vehicle': log.vehicle.vehicle,
                         'fuel_card': log.fuel_card,
                         'fuel_ob': log.balance,'allocated': log.amount_allocated, 'fuel_cb': log.new_balance,
                         'make_n_model': log.vehicle.make_n_model, 'allocation_type': log.transaction_type,} for log in logs]

        totals = {'allocated': sum(logs.values_list('amount_allocated', flat=True)) }

        tran_dict[employee.full_name] = {'transactions': transactions, 'totals': totals}

    if request.POST.get('report', None) and filter_form.is_valid():
        date_from = filter_form.cleaned_data.get('start_date', filter_form.initial.get('start_date')).replace(day=1)
        date_to = filter_form.cleaned_data.get('end_date', filter_form.initial.get('end_date'))
        response = HttpResponse(content_type='text/csv')
        filename = "rpt_driver_fuel_allocations.csv"
        response['Content-Disposition'] = 'attachment; filename='+filename
        writer = csv.writer(response)

        writer.writerow(["Driver Fuel Allocations Report"])
        writer.writerow(["Date From:",date_from,"Date To:",date_to])


        for employee, values in tran_dict.items():
            writer.writerow([employee])
            headers = ["Allocation Date","Allocation Type","Vehicle","Make and Model","Fuel Card","Fuel OB","Fuel Amount","Fuel CB"]
            writer.writerow(headers)

            for val in values.get('transactions'):
                writer.writerow([val.get('allocation_date'), val.get('allocation_type'), val.get('vehicle'), val.get('make_n_model'),
                                 val.get('fuel_card'), val.get('fuel_ob'), val.get('allocated'), val.get('fuel_cb')])

            writer.writerow(["Totals","","","","","",values.get('totals').get('allocated'),""])

        return response


    context ={
        'employees': employees,
        'filter_form': filter_form,
        'title': title,
        'tran_dict':tran_dict
    }

    return render(request, "rpt_driver_fuel_allocations.html", context)


@login_required
@permission_required('fleet.view_reports', raise_exception=True)
def rpt_vehicle_allocations(request):
    title='Vehicle Fuel Allocations Report'
    filter_form = TransactionsFilterForm(request.POST or None)

    vehicles = None

    if filter_form.is_valid():
        date_from = filter_form.cleaned_data.get('start_date', filter_form.initial.get('start_date')).replace(day=1)
        date_to = filter_form.cleaned_data.get('end_date', filter_form.initial.get('end_date'))
        term = filter_form.cleaned_data.get('vehicle', None)

        vehicles = Vehicle.objects
        if term:
            vehicles = vehicles.filter(vehicle=term)

        vehicles = vehicles.filter(vehicle_vehicleAllocations__allocation_date__range=[date_from, date_to])


    if vehicles is None:
        date_from = filter_form.initial.get('start_date').replace(day=1)
        date_to = filter_form.initial.get('end_date')
        vehicles = Vehicle.objects.filter(vehicle_vehicleAllocations__allocation_date__range=[date_from, date_to])

    tran_dict = {}
    for vehicle in vehicles:
        if not tran_dict.get(vehicle.vehicle, None):
            tran_dict[vehicle.vehicle] = {}

        logs = vehicle.vehicle_vehicleAllocations.filter(allocation_date__range=[date_from, date_to]).order_by('allocation_date')

        transactions = [{'allocation_date': log.allocation_date, 'driver': log.driver.full_name,
                         'fuel_card': log.fuel_card, 'cycle_limit': log.cycle_limit,'status': log.status, 'authorizer': log.authorizer,
                         'mileage': log.mileage, 'allocation_type': log.transaction_type} for log in logs]


        tran_dict[vehicle.vehicle] = {'transactions': transactions, 'make': vehicle.make_n_model}

    if request.POST.get('report', None) and filter_form.is_valid():
        date_from = filter_form.cleaned_data.get('start_date', filter_form.initial.get('start_date')).replace(day=1)
        date_to = filter_form.cleaned_data.get('end_date', filter_form.initial.get('end_date'))
        response = HttpResponse(content_type='text/csv')
        filename = "rpt_vehicle_fuel_allocations.csv"
        response['Content-Disposition'] = 'attachment; filename='+filename
        writer = csv.writer(response)

        writer.writerow(["Vehicle Fuel Allocations Report"])
        writer.writerow(["Date From:",date_from,"Date To:",date_to])


        for vehicle, values in tran_dict.items():
            writer.writerow([values.get('make'),vehicle])
            headers = ["Allocation Date","Type","Driver","Current Mileage","Fuel Card","Cycle Limit","Status","Authorizer"]
            writer.writerow(headers)

            for val in values.get('transactions'):

                writer.writerow([val.get('allocation_date'), val.get('allocation_type'), val.get('driver'), val.get('mileage'),val.get('fuel_card'),
                                 val.get('cycle_limit'), val.get('status'), val.get('authorizer')])



        return response

    context ={
        'vehicles': vehicles,
        'title': title,
        "filter_form": filter_form,
        'tran_dict':tran_dict,

    }
    return render(request, "rpt_vehicle_allocations.html", context)


@login_required
@permission_required('fleet.view_reports', raise_exception=True)
def rpt_driver_vehicle_allocations(request):

    title='Driver Vehicle Allocations Report'
    filter_form = TransactionsFilterForm(request.POST or None)

    employees = None

    if filter_form.is_valid():
        date_from = filter_form.cleaned_data.get('start_date', filter_form.initial.get('start_date'))
        date_to = filter_form.cleaned_data.get('end_date', filter_form.initial.get('end_date'))
        f_term = filter_form.cleaned_data.get('driver', None)
        r_term = filter_form.cleaned_data.get('region', None)
        employees = Employee.objects
        if f_term:
            employees = employees.filter(first_name__icontains=f_term).order_by('branch__region', 'first_name')            
        if r_term:
            region = Region.objects.filter(region__icontains=r_term)
            employees = employees.filter(branch__region=region).order_by('branch__region', 'first_name')

        employees = employees.filter(driver_VehicleAllocations__allocation_date__range=[date_from, date_to])


    if employees is None:
        date_from = filter_form.initial.get('start_date')
        date_to = filter_form.initial.get('end_date')
        employees = Employee.objects.filter(driver_VehicleAllocations__allocation_date__range=[date_from, date_to])

    tran_dict = {}
    for employee in employees:
        if not tran_dict.get(employee.full_name, None):
            tran_dict[employee.full_name] = {}

        logs = employee.driver_VehicleAllocations.filter(allocation_date__range=[date_from, date_to]).order_by('allocation_date')

        transactions = [{'allocation_date': log.allocation_date, 'vehicle': log.vehicle.vehicle,
                         'model_year': log.vehicle.model_year,'color': log.vehicle.color,'mileage': log.mileage, 'region': log.driver.branch.region,'status': log.status,
                         'make_n_model': log.vehicle.make_n_model, 'o_type': log.vehicle.ownership_type, 'allocation_type': log.transaction_type} for log in logs]

        tran_dict[employee.full_name] = {'transactions': transactions}


    if request.POST.get('report', None) and filter_form.is_valid():
        date_from = filter_form.cleaned_data.get('start_date', filter_form.initial.get('start_date')).replace(day=1)
        date_to = filter_form.cleaned_data.get('end_date', filter_form.initial.get('end_date'))
        response = HttpResponse(content_type='text/csv')
        filename = "rpt_driver_vehicle_allocations.csv"
        response['Content-Disposition'] = 'attachment; filename='+filename
        writer = csv.writer(response)

        writer.writerow(["Driver Vehicle Allocations Report"])
        writer.writerow(["Date From:",date_from,"Date To:",date_to])

        for employee, values in tran_dict.items():
            writer.writerow([employee])
            headers = ["Allocation Date","Allocation Type","Vehicle","Make and Model","Fuel Card","Cycle Limit","Status","Authorizer"]
            writer.writerow(headers)

            for val in values.get('transactions'):
                writer.writerow([val.get('allocation_date'), val.get('allocation_type'), val.get('vehicle'), val.get('make_n_model'),
                                 val.get('model_year'), val.get('region'),  val.get('o_type'),  val.get('color'),  val.get('mileage'), val.get('status')])


        return response


    context ={
        'employees': employees,
        'filter_form': filter_form,
        'title': title,
        'tran_dict':tran_dict
    }


    return render(request, "rpt_driver_vehicle_allocations.html", context)


@login_required
@permission_required('fleet.view_reports', raise_exception=True)
def rpt_current_drivers(request):

    title="Current Vehicle Drivers Report"
    vehicles = Vehicle.objects.all()

    date = 'purchase_date'
    filter_form = TransactionsFilterForm(request.GET or None)   
    active_report = vehicles.filter(active=True).order_by('current_driver__branch__region', 'licence_plate')
    historical_report = vehicles.filter(active=False).order_by('current_driver__branch__region', 'licence_plate')
    if u'filter_list' in request.GET and filter_form.is_valid():
        active_report = filter_form.filter(active_report, date)   
        historical_report = filter_form.filter(historical_report, date)

    if request.POST.get('report', None):

        response = HttpResponse(content_type='text/csv')
        filename = "rpt_vehicle_current_driver.csv"
        response['Content-Disposition'] = 'attachment; filename='+filename
        writer = csv.writer(response)

        writer.writerow(["Vehicle Current Driver Report"])
        headers = ["Driver","Vehicle","Make And Model","Model Year","Ownership","Color","Current Mileage","Fuel Balance","Status"]
        writer.writerow(headers)

        for vehicle in active_report:
            writer.writerow([vehicle.get_current_driver(), vehicle.vehicle, vehicle.make_n_model,vehicle.model_year,
                             vehicle.ownership_type,vehicle.color, vehicle.get_current_mileage(),vehicle.fuel_balance, vehicle.status])
        
        writer.writerow(["Historical Vehicles Report"])
        headers = ["Driver","Vehicle","Make And Model","Model Year","Ownership","Color","Current Mileage","Fuel Balance","Status"]
        writer.writerow(headers)

        for vehicle in historical_report:
            writer.writerow([vehicle.get_current_driver(), vehicle.vehicle, vehicle.make_n_model,vehicle.model_year,
                             vehicle.ownership_type,vehicle.color, vehicle.get_current_mileage(),vehicle.fuel_balance, vehicle.status])
        return response

    context = {
        "title": title,
        "active_report":active_report,
        "historical_report": historical_report,
        "filter_form":filter_form,
    }
    return render(request, "rpt_current_drivers.html", context)


@login_required
def get_vehicle(request):
    term = request.GET.get('term', '')
    car = Vehicle.objects.filter(licence_plate__icontains=term).distinct()[:20]

    data = []

    for n in car:
        vcl = {}
        vcl['id'] = n.id
        vcl['label'] = n.vehicle
        vcl['value'] = n.vehicle
        data.append(vcl)

    results = json.dumps(data)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)

@login_required
def get_region(request):
    term = request.GET.get('term', '')
    reg = Region.objects.filter(region__icontains=term).distinct()[:20]

    data = []

    for n in reg:
        vcl = {}
        vcl['id'] = n.id
        vcl['label'] = n.region
        vcl['value'] = n.region
        data.append(vcl)       

    results = json.dumps(data)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)

@login_required
def get_employee(request):
    term = request.GET.get('term', '')
    employee = Employee.objects.filter(first_name__icontains=term ).distinct()[:20]

    data = []

    for n in employee:
        emp = {}
        emp['id'] = n.id
        emp['label'] = n.first_name
        emp['value'] = n.first_name
        data.append(emp)

    results = json.dumps(data)
    mimetype = 'application/json'

    return HttpResponse(results, mimetype)


@login_required
def get_fuel_card(request):
    term = request.GET.get('term', '')
    cards = FuelCard.objects.filter(card_number__icontains=term).distinct()[:20]

    data = []

    for n in cards:
        cn = {}
        cn['id'] = n.id
        cn['label'] = n.card_number
        cn['value'] = n.card_number
        data.append(cn)

    results = json.dumps(data)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)


@login_required
@permission_required('fleet.create_trip')
def tripLogImports(request, vehicle_id):
    title = 'Trip Log Imports'
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    import_file = FileUpload()
    import_file.vehicle = vehicle
    upload_file_form = tripImportUploadForm(request.POST or None, request.FILES or None, prefix='doc', instance=import_file)
    uploads = FileUpload.objects.filter(vehicle=vehicle, transaction='Trip Log Imports')
    trip = Trip.objects.filter(vehicle=vehicle)
    date = 'log_date'
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_log' in request.GET and filter_form.is_valid():
        trip = filter_form.filter(trip, date)

    page = request.GET.get('page', 1)
    trip_paginator = Paginator(trip, 6)
    try:
        trip = trip_paginator.page(page)
    except PageNotAnInteger:
        trip = trip_paginator.page(1)
    except EmptyPage:
        trip = trip_paginator.page(trip_paginator.num_pages)


    context = {
        'title': title,
        'upload_file_form': upload_file_form,
        'uploads': uploads,
        'trip': trip,
        # 'trip_log': trip_log,
        'filter_form': filter_form,
    }
    post = request.POST
    if request.POST:
        if u'save' in post:
            validated = upload_file_form.is_valid()
            if validated:
                uploaded = upload_file_form.save(commit=False)
                uploaded.file_name = uploaded.file.name
                uploaded.transaction = "Trip Log Imports"
                uploaded.save()
                # import pdb; pdb.set_trace()
                file = '%s/%s'% (settings.MEDIA_ROOT, uploaded.file)
                process_trip_log_import(request, file)

            return HttpResponseRedirect(reverse('fleet:viewvehicle', kwargs={'vehicle_id':vehicle.id}))
    return render(request, "tripLogImports.html", context)



@login_required
@permission_required('fleet.create_triplog', raise_exception=True)
def process_trip_log_import(request, import_file):
    upload_list = []
    dataReader = csv.reader(open(import_file), delimiter=',', quotechar='"')
    reg_number = ""
    log_date = date.today()
    flag = False


    for row in dataReader:
        if u"Vehicle Registration" in row[0]:
            vehicle = row[0].replace("Vehicle Registration : ","")
            driver = row[5].replace("Vehicle Alias : ","")
            vehicles = Vehicle.objects.filter(vehicle=vehicle)
            if len(vehicles) > 0:
                vehicle = vehicles.first()
                if vehicle.get_current_driver() != "Not Allocated":
                    employee = vehicle.get_current_driver()

        if row[2] == "Location":
            log_date = datetime.strptime(row[0], "%Y/%m/%d").date()
            trip = Trip()
            trip.save()
            trip = Trip.objects.all().order_by('-id')[0]


        status = ""
        try:
            status = row[9]
        except IndexError:
            flag = False


        if status == "Ignition On":
            flag = True

        if u"Trip Nr" in row[0]:
            trip.vehicle = vehicle
            trip.driver = employee
            trip.log_date = log_date
            # trip.duration = row[2].replace(r'.*? Duration : ', '')

            avarage_speed = row[5].replace("Avg : ","")
            avarage_speed = avarage_speed.replace(" km/h","")
            trip.avarage_speed = avarage_speed

            max_speed =row[7].replace("Max : ","")
            max_speed =max_speed.replace(" km/h","")
            trip.max_speed = max_speed

            distance = row[9].replace("Distance : ","")
            distance= distance.replace(" km","")
            trip.distance = distance
            trip.save()

            print(trip)
            flag =  False


        if flag:
            log_time = datetime.strptime(row[0], "%H:%M:%S").time()
            trip_log = TripLog()
            trip_log.log_date = datetime.combine(log_date, log_time)
            trip_log.trip_number = trip
            trip_log.location = row[2]
            trip_log.road_speed = row[6]
            trip_log.speed = row[7]
            trip_log.odometer = row[8]
            trip_log.status = row[9]
            trip_log.save()
            upload_list.append(trip_log)

        if status == "Ignition Off":
            flag = False


    return upload_list

def comments(request):
    title = "Comments"
    comments = Comment.objects.all()

    date = 'commented'
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'search' in request.GET and filter_form.is_valid():
        comments = filter_form.filter(comments, date)

    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context = {
        'title': title,
        'comments': comments,
        'filter_form': filter_form,
    }

    return render(request, "comments.html", context)



@csrf_exempt
@login_required
@permission_required('fleet.view_triplog', 'fleet.view_trip', raise_exception=True)
def load_trip_log(request, trip_id):
    trip = Trip.objects.get(pk=trip_id)
    if trip:
        trip_log = TripLog.objects.filter(trip_number=trip)
    else:
        trip_log = TripLog.objects.filter(trip_number=1)

    context = {"trip_log": trip_log}
    response = render(request, "_trip_log.html", context)

    return HttpResponse(response)

@login_required
@permission_required('fleet.authorize_vehiclemaintenance', raise_exception=True)
def authorizations(request):
    title = "Transaction Authorizations"

    claims = InsuranceClaim.objects.filter(accept=1, authorize='Pending').order_by('-id')
    date = 'claims'
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_claims' in request.GET and filter_form.is_valid():
        claims = filter_form.filter(claims, date)
    page = request.GET.get('page', 1)
    claims_paginator = Paginator(claims, 14)
    try:
        claims = claims_paginator.page(page)
    except PageNotAnInteger:
        claims = claims_paginator.page(1)
    except EmptyPage:
        claims = claims_paginator.page(claims_paginator.num_pages)

    maintenance_list = VehicleMaintenance.objects.filter(accept=1, authorize='Pending').order_by('-id')
    date = 'maint_date'
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_maintenance' in request.GET and filter_form.is_valid():
        maintenance_list = filter_form.filter(maintenance_list, date)
    page = request.GET.get('page', 1)
    maintenance_list_paginator = Paginator(maintenance_list, 14)
    try:
        maintenance_list = maintenance_list_paginator.page(page)
    except PageNotAnInteger:
        maintenance_list = maintenance_list_paginator.page(1)
    except EmptyPage:
        maintenance_list = maintenance_list_paginator.page(maintenance_list_paginator.num_pages)


    traffic_fines = Trafficfine.objects.filter(accept=1, authorize='Pending').order_by('-id')
    date = 'tf_due_date'
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_tf' in request.GET and filter_form.is_valid():
        traffic_fines = filter_form.filter(traffic_fines, date)
    page = request.GET.get('page', 1)
    traffic_fines_paginator = Paginator(traffic_fines, 14)
    try:
        traffic_fines = traffic_fines_paginator.page(page)
    except PageNotAnInteger:
        traffic_fines = traffic_fines_paginator.page(1)
    except EmptyPage:
        traffic_fines = traffic_fines_paginator.page(traffic_fines_paginator.num_pages)


    allocations_list = VehicleAllocation.objects.filter(accept=1, authorize='Pending').order_by('-id')
    date = 'allocation_date'
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter' in request.GET and filter_form.is_valid():
        allocations_list = filter_form.filter(allocations_list, date)
    page = request.GET.get('page', 1)
    paginator = Paginator(allocations_list, 14)
    try:
        allocations_list = paginator.page(page)
    except PageNotAnInteger:
        allocations_list = paginator.page(1)
    except EmptyPage:
        allocations_list = paginator.page(paginator.num_pages)


    fuel_allocations_list = FuelAllocation.objects.filter(accept=1, authorize='Pending').order_by('-id')
    if u'filter_fuel' in request.GET and filter_form.is_valid():
        date = 'allocation_date'
        fuel_allocations_list = filter_form.filter(fuel_allocations_list, date)
    fuel_allocations_list_paginator = Paginator(fuel_allocations_list, 14)
    try:
        fuel_allocations_list = fuel_allocations_list_paginator.page(page)
    except PageNotAnInteger:
        fuel_allocations_list = fuel_allocations_list_paginator.page(1)
    except EmptyPage:
        fuel_allocations_list = fuel_allocations_list_paginator.page(fuel_allocations_list_paginator.num_pages)


    licence_disk_list = RenewLicenceDisk.objects.filter(accept=1, authorize='Pending').order_by('-id')
    date = 'renewal_date'
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_list' in request.GET and filter_form.is_valid():
        licence_disk_list = filter_form.filter(licence_disk_list, date)
    page = request.GET.get('page', 1)
    licence_disk_list_paginator = Paginator(licence_disk_list, 14)
    try:
        licence_disk_list = licence_disk_list_paginator.page(page)
    except PageNotAnInteger:
        licence_disk_list = licence_disk_list_paginator.page(1)
    except EmptyPage:
        licence_disk_list = licence_disk_list_paginator.page(licence_disk_list_paginator.num_pages)

    context ={
        "claims": claims,
        "maintenance_list": maintenance_list,
        "traffic_fines": traffic_fines,
        "allocations_list": allocations_list,
        "fuel_allocations_list": fuel_allocations_list,
        "licence_disk_list": licence_disk_list,
        "filter_form": filter_form,
        "title": title,

    }
    return render(request, "authorizations.html", context)


@login_required
@permission_required('fleet.view_insuranceclaim', raise_exception=True)
def vehicleClaimsList(request):
    fleet =  Vehicle.objects.all()
    insurance_claims = InsuranceClaim.objects.all()
    if request.user.regional_staff:
        fleet =  Vehicle.objects.filter(current_driver__branch__region=request.user.employee.branch.region)
        insurance_claims = InsuranceClaim.objects.filter(driver__branch__region=request.user.employee.branch.region)

    title = "Vehicles Insurance Claims List"
    claims = insurance_claims.order_by('-id')
    date = 'claims'
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_claims' in request.GET and filter_form.is_valid():
        claims = filter_form.filter(claims, date)
    page = request.GET.get('page', 1)
    claims_paginator = Paginator(claims, 14)
    try:
        claims = claims_paginator.page(page)
    except PageNotAnInteger:
        claims = claims_paginator.page(1)
    except EmptyPage:
        claims = claims_paginator.page(claims_paginator.num_pages)

    pending_claims = insurance_claims.filter(claim_status='Pending').order_by('-id')
    if u'filter_pending' in request.GET and filter_form.is_valid():
        pending_claims = filter_form.filter(pending_claims, date)
    pending_claims_paginator = Paginator(pending_claims, 14)
    try:
        pending_claims = pending_claims_paginator.page(page)
    except PageNotAnInteger:
        pending_claims = pending_claims_paginator.page(1)
    except EmptyPage:
        pending_claims = pending_claims_paginator.page(pending_claims_paginator.num_pages)

    finalized_claims = insurance_claims.filter(claim_status='Finalized').order_by('-id')
    if u'filter_finalized' in request.GET and filter_form.is_valid():
        date = 'claims_finalized'
        finalized_claims = filter_form.filter(finalized_claims, date)
    finalized_claims_paginator = Paginator(finalized_claims, 14)
    try:
        finalized_claims = finalized_claims_paginator.page(page)
    except PageNotAnInteger:
        finalized_claims = finalized_claims_paginator.page(1)
    except EmptyPage:
        finalized_claims = finalized_claims_paginator.page(finalized_claims_paginator.num_pages)

    rejected_claims = insurance_claims.filter(claim_status='Rejected').order_by('-id')
    if u'filter_rejected' in request.GET and filter_form.is_valid():
        date = 'claims_finalized'
        rejected_claims = filter_form.filter(rejected_claims, date)
    rejected_claims_paginator = Paginator(rejected_claims, 14)
    try:
        rejected_claims = rejected_claims_paginator.page(page)
    except PageNotAnInteger:
        rejected_claims = rejected_claims_paginator.page(1)
    except EmptyPage:
        rejected_claims = rejected_claims_paginator.page(rejected_claims_paginator.num_pages)

    vehicles = fleet.order_by('licence_plate')
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_stats' in request.GET and filter_form.is_valid():
        date = 'purchase_date'
        vehicles = filter_form.filter(vehicles, date)
    page = request.GET.get('page', 1)
    vehicles_paginator = Paginator(vehicles, 14)
    try:
        vehicles = vehicles_paginator.page(page)
    except PageNotAnInteger:
        vehicles = vehicles_paginator.page(1)
    except EmptyPage:
        vehicles = vehicles_paginator.page(vehicles_paginator.num_pages)

    context ={
        "title": title,
        "claims": claims,
        "pending_claims": pending_claims,
        "finalized_claims": finalized_claims,
        "rejected_claims": rejected_claims,
        "filter_form": filter_form,
        "vehicles": vehicles,
        }
    return render(request, "vehicleClaimsList.html", context)


@login_required
@permission_required('fleet.edit_insuranceclaim', raise_exception=True)

def editVehicleClaim(request, trans_id):
    title = "Edit Vehicle Insurance Claim"
    read_only = False

    transaction = InsuranceClaim.objects.get(pk=trans_id)
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)
    trans_key = transaction.id
    vehicle = transaction.vehicle
    vehicle_id = Vehicle.objects.filter(licence_plate=vehicle)
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    try:
        requisition = Requisition.objects.get(obj_id=trans_id, requisition_type="InsuranceClaim")
    except Requisition.DoesNotExist:
        requisition = None

    uploads = FileUpload.objects.filter(vehicle=vehicle).filter(transaction="InsuranceClaim").filter(transaction_id=trans_key)
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]
    form = AddInsuranceClaimForm(request.POST or None, instance=transaction, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')

    comments = Comment.objects.filter(vehicle = vehicle).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
        "title": title,
        "form": form,
        "comment_form": comment_form,
        "vehicle": vehicle,
        "upload_file_form":upload_file_form,
        "uploads":uploads,
        "sliders":images,
        "comments":comments,


        }

    post = request.POST
    if request.POST:
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by = creator
                save_form.modified_by = request.user
                save_form.save()

                if request.user.has_perm('authorize_insuranceclaim'):
                    incident_id = save_form.incidence_number
                    if save_form.authorize=="Aproved"and incident_id:
                        incident = Incident.objects.get(pk=incident_id.id)
                        incident.claimed = 1
                        incident.save()


                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.vehicle = vehicle
                    new_comment.comment_type = "InsuranceClaim"
                    new_comment.obj_id = transaction.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = FileUpload.objects.create(file=f)
                        uploaded.transaction_id = transaction.id
                        uploaded.vehicle = vehicle
                        uploaded.file_name = uploaded.file.name
                        uploaded.transaction = "InsuranceClaim"
                        uploaded.save()

                if request.user.has_perm('authorize_insuranceclaim'):
                    if requisition:
                        return HttpResponseRedirect(reverse('fleet:view_requisition', kwargs={'obj_id':requisition.id}))
                    else:
                        return HttpResponseRedirect(reverse('fleet:authorizations'))
                else:
                    if not requisition:
                        excess = form.cleaned_data.get('excess', None)
                        if excess > 0 and excess:
                            return HttpResponseRedirect(reverse('fleet:requisition_insuranceclaimexcess', kwargs={'obj_id':transaction.id}))
                        else:
                            return HttpResponseRedirect(reverse('fleet:viewvehicle', kwargs={'vehicle_id':vehicle.id}))
    return render(request, "vehicles.html", context)

@login_required
@permission_required('fleet.view_insuranceclaim', raise_exception=True)
def viewVehicleClaim(request, trans_id):
    title = "View Vehicle Insurance Claim"
    read_only = False

    transaction = InsuranceClaim.objects.get(pk=trans_id)
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)
    trans_key = transaction.id
    vehicle = transaction.vehicle
    vehicle_id = Vehicle.objects.filter(licence_plate=vehicle)
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    try:
        requisition = Requisition.objects.get(obj_id=trans_id, requisition_type="InsuranceClaim")
    except Requisition.DoesNotExist:
        requisition = None

    uploads = FileUpload.objects.filter(vehicle=vehicle).filter(transaction="InsuranceClaim").filter(transaction_id=trans_key)
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]
    form = AddInsuranceClaimForm(request.POST or None, instance=transaction, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')

    comments = Comment.objects.filter(vehicle = vehicle).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
        "title": title,
        "form": form,
        "comment_form": comment_form,
        "vehicle": vehicle,
        "upload_file_form":upload_file_form,
        "uploads":uploads,
        "sliders":images,
        "comments":comments,
        "view_transaction":True,

        }

    return render(request, "vehicles.html", context)


@login_required
def page_carousel(request):

    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.all().values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]
    print images

    context = {
        "sliders":images
        }

    return render(request, "requisition.html", context)



@login_required
@permission_required('fleet.create_insuranceclaim', raise_exception=True)
def addVehicleClaim(request, vehicle_id):
    title = "Add Vehicle Insurance Claim"

    vehicle = Vehicle.objects.get(pk=vehicle_id)
    claim = InsuranceClaim()
    claim.vehicle = vehicle

    if vehicle.get_current_driver() != "Not Allocated":
        claim.driver = vehicle.get_current_driver()

    form = AddInsuranceClaimForm(request.POST or None, instance=claim, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUpload.objects.filter(vehicle=vehicle, transaction="InsuranceClaim")
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = Comment.objects.filter(vehicle = vehicle).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)


    context ={
        "title": title,
        "form": form,
        "comment_form": comment_form,
        "vehicle": vehicle,
        "upload_file_form": upload_file_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,

        }

    post = request.POST
    if request.POST:
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by = request.user
                save_form.save()
                latest_trans = InsuranceClaim.objects.order_by('-id')[0]


                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.vehicle = latest_trans.vehicle
                    new_comment.comment_type = "InsuranceClaim"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = FileUpload.objects.create(file=f)
                        uploaded.transaction_id = latest_trans.id
                        uploaded.vehicle = latest_trans.vehicle
                        uploaded.file_name = uploaded.file.name
                        uploaded.transaction = "InsuranceClaim"
                        uploaded.save()

                excess = form.cleaned_data.get('excess', None)
                if not excess == 0 and excess:
                    return HttpResponseRedirect(reverse('fleet:requisition_insuranceclaimexcess', kwargs={'obj_id':latest_trans.id}))
                else:
                    return HttpResponseRedirect(reverse('fleet:viewvehicle', kwargs={'vehicle_id':vehicle.id}))


    return render(request, "vehicles.html", context)

@login_required
@permission_required('fleet.view_vehicle',raise_exception=True)
def viewvehicle (request, vehicle_id):
    title = "Vehicle Details"
    filter_form = TransactionsFilterForm(request.POST or None)
    vehicle = None
    if filter_form.is_valid():
        term = filter_form.cleaned_data.get('vehicle')

        vehicle = Vehicle.objects.all()
        if term:
            vehicle = Vehicle.objects.filter(licence_plate=term).first()
        else:
            vehicle = Vehicle.objects.get(pk=vehicle_id)

    if vehicle is None:
        vehicle = Vehicle.objects.get(pk=vehicle_id)

    allocations_list = VehicleAllocation.objects.filter(vehicle=vehicle).order_by("-id")
    traffic_fines = Trafficfine.objects.filter(vehicle=vehicle).order_by("-id")
    maintenance_list = VehicleMaintenance.objects.filter(vehicle=vehicle).order_by("-id")
    insurance_list = InsuranceClaim.objects.filter(vehicle=vehicle).order_by("-id")
    inspections = MileageLog.objects.filter(vehicle=vehicle).order_by("-id")
    incidences = Incident.objects.filter(vehicle=vehicle).order_by("-id")

    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUpload.objects.filter(vehicle=vehicle, transaction_id=vehicle.id, transaction="Vehicle")
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]
    comment_form = CommentsForm(request.POST or None)
    comments = Comment.objects.filter(vehicle = vehicle).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
        "title": title,
        "vehicle": vehicle,
        "upload_file_form": upload_file_form,
        "uploads": uploads,
        "sliders": images,
        'filter_form': filter_form,
        "comments": comments,
        "comment_form": comment_form,
        "allocations_list":allocations_list,
        "traffic_fines":trafficfines,
        "maintenance_list":maintenance_list,
        "claims":insurance_list,
        "mileage_log":inspections,
        "incidences_list":incidences,
        "view_vehicle":True,
        }
    post = request.POST
    if request.POST:
        if u'save' in post:

            comment = comment_form.is_valid()
            if comment:
                new_comment = comment_form.save(commit=False)
                new_comment.vehicle = vehicle
                new_comment.comment_type = "Vehicle"
                new_comment.obj_id = vehicle.id
                new_comment.created_by = request.user
                new_comment.save()

            validated = upload_file_form.is_valid()
            if validated:
                files = request.FILES.getlist('doc-file')
                for f in files:
                    uploaded = FileUpload.objects.create(file=f)
                    uploaded.transaction_id = vehicle.id
                    uploaded.vehicle = vehicle
                    uploaded.file_name = uploaded.file.name
                    uploaded.transaction = "Vehicle"
                    uploaded.save()
            return HttpResponseRedirect(reverse('fleet:viewvehicle', kwargs={'vehicle_id':vehicle.id}))
    return render(request, "vehicles.html", context)


@login_required
@permission_required('fleet.view_vehicle',raise_exception=True)
def viewDriverProfile (request, driver_id):
    title = "Driver Profile"
    filter_form = TransactionsFilterForm(request.POST or None)
    driver = None
    if filter_form.is_valid():
        term = filter_form.cleaned_data.get('driver')
        driver = Employee.objects.all()
        if term:
            driver = Employee.objects.filter(first_name__icontains=term).first()
        else:
            driver = Employee.objects.get(pk=driver_id)
    if driver is None:
        driver = Employee.objects.get(pk=driver_id)

    allocations_list = VehicleAllocation.objects.filter(driver=driver).order_by("-id")
    count_allocations = allocations_list.filter(transaction_type="Allocated").aggregate(ac=Count('id'))['ac'] or 0
    vehicle = allocations_list.first().vehicle

    driving_licence = DrivingLicence.objects.filter(driver=driver).order_by('-id').first()

    traffic_fines = Trafficfine.objects.filter(driver=driver).order_by("-id")
    count_traffic_fines = traffic_fines.aggregate(ac=Count('id'))['ac'] or 0
    total_traffic_fines = traffic_fines.aggregate(ac=Sum('amount'))['ac'] or 0
    count_court_appearences = traffic_fines.filter(court_appearance=True).aggregate(ac=Count('id'))['ac'] or 0
    count_serious_offences = traffic_fines.filter(serious_offence=True).aggregate(ac=Count('id'))['ac'] or 0

    maintenance_list = VehicleMaintenance.objects.filter(driver=driver).order_by("-id")
    total_maintenance = maintenance_list.aggregate(ac=Sum('actual_cost'))['ac'] or 0
    total_service = maintenance_list.filter(maint_type="Service").aggregate(ac=Sum('actual_cost'))['ac'] or 0
    total_tyres = maintenance_list.filter(maint_type="Tires").aggregate(ac=Sum('actual_cost'))['ac'] or 0
    total_repairs = maintenance_list.filter(~Q(Q(maint_type="Tires") | Q(maint_type="Service"))).aggregate(ac=Sum('actual_cost'))['ac'] or 0

    insurance_list = InsuranceClaim.objects.filter(driver=driver).order_by("-id")
    count_insurance_claims = insurance_list.aggregate(ac=Count('id'))['ac'] or 0
    count_pending_insurance_claims = insurance_list.aggregate(ac=Count('id'))['ac'] or 0
    total_excess_insurance_claims = insurance_list.aggregate(ac=Sum('excess'))['ac'] or 0
    total_insurance_claims = insurance_list.aggregate(ac=Sum('payout_amount'))['ac'] or 0

    inspections = MileageLog.objects.filter(driver=driver).order_by("-id")
    incidences = Incident.objects.filter(driver=driver).order_by("-id")
    count_incidences = incidences.aggregate(ac=Count('id'))['ac'] or 0

    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUpload.objects.filter(vehicle=vehicle, transaction_id=vehicle.id, transaction="Vehicle")
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]
    comment_form = CommentsForm(request.POST or None)
    comments = Comment.objects.filter(vehicle = vehicle).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
        "title": title,
        "driver": driver,
        "vehicle": vehicle,
        "driving_licence":driving_licence,
        "upload_file_form": upload_file_form,
        "uploads": uploads,
        "sliders": images,
        'filter_form': filter_form,
        "comments": comments, 
        "comment_form": comment_form,           
        "allocations_list":allocations_list,
        "count_allocations":count_allocations,      
        "traffic_fines":traffic_fines,
        "count_traffic_fines":count_traffic_fines,
        "count_court_appearences":count_court_appearences,
        "count_serious_offences":count_serious_offences,
        "total_traffic_fines":total_traffic_fines,
        "maintenance_list":maintenance_list,
        "total_maintenance":total_maintenance,
        "total_service":total_service,
        "total_tyres":total_tyres,
        "total_repairs":total_repairs,
        "claims":insurance_list,
        "count_insurance_claims":count_insurance_claims,
        "count_pending_insurance_claims":count_pending_insurance_claims,
        "total_excess_insurance_claims":total_excess_insurance_claims,
        "total_insurance_claims":total_insurance_claims,
        "mileage_log":inspections,
        "incidences_list":incidences,
        }
    post = request.POST
    if request.POST:        
        if u'save' in post:      
                              
            comment = comment_form.is_valid()
            if comment:
                new_comment = comment_form.save(commit=False)
                new_comment.vehicle = vehicle
                new_comment.comment_type = "Vehicle"
                new_comment.obj_id = vehicle.id
                new_comment.created_by = request.user
                new_comment.save()

            validated = upload_file_form.is_valid()
            if validated:                   
                files = request.FILES.getlist('doc-file')
                for f in files:
                    uploaded = FileUpload.objects.create(file=f)
                    uploaded.transaction_id = vehicle.id
                    uploaded.vehicle = vehicle
                    uploaded.file_name = uploaded.file.name
                    uploaded.transaction = "Vehicle"                          
                    uploaded.save()
            return HttpResponseRedirect(reverse('fleet:viewvehicle', kwargs={'vehicle_id':vehicle.id}))
    return render(request, "viewDriverProfile.html", context)


@login_required
@permission_required('fleet.view_vehicle',raise_exception=True)
def editDrivingLicence (request, trans_id):
    title = "Driver Profile" 
    transaction =  DrivingLicence.objects.get(pk=trans_id)
    filter_form = TransactionsFilterForm(request.POST or None)
    driver = None
    if filter_form.is_valid():       
        term = filter_form.cleaned_data.get('driver')
        if term:            
            driver = Employee.objects.filter(first_name__icontains=term).first()
        else:
            driver = Employee.objects.get(pk=transaction.driver.id)
    if driver is None:
        driver = Employee.objects.get(pk=transaction.driver.id)

    allocations_list = VehicleAllocation.objects.filter(driver=driver).order_by("-id")
    count_allocations = allocations_list.filter(transaction_type="Allocated").aggregate(ac=Count('id'))['ac'] or 0
    vehicle = allocations_list.first().vehicle

    traffic_fines = Trafficfine.objects.filter(driver=driver).order_by("-id")
    count_traffic_fines = traffic_fines.aggregate(ac=Count('id'))['ac'] or 0
    total_traffic_fines = traffic_fines.aggregate(ac=Sum('amount'))['ac'] or 0
    count_court_appearences = traffic_fines.filter(court_appearance=True).aggregate(ac=Count('id'))['ac'] or 0
    count_serious_offences = traffic_fines.filter(serious_offence=True).aggregate(ac=Count('id'))['ac'] or 0

    maintenance_list = VehicleMaintenance.objects.filter(driver=driver).order_by("-id")
    total_maintenance = maintenance_list.aggregate(ac=Sum('actual_cost'))['ac'] or 0
    total_service = maintenance_list.filter(maint_type="Service").aggregate(ac=Sum('actual_cost'))['ac'] or 0
    total_tyres = maintenance_list.filter(maint_type="Tires").aggregate(ac=Sum('actual_cost'))['ac'] or 0
    total_repairs = maintenance_list.filter(~Q(Q(maint_type="Tires") | Q(maint_type="Service"))).aggregate(ac=Sum('actual_cost'))['ac'] or 0

    insurance_list = InsuranceClaim.objects.filter(driver=driver).order_by("-id")
    count_insurance_claims = insurance_list.aggregate(ac=Count('id'))['ac'] or 0
    count_pending_insurance_claims = insurance_list.aggregate(ac=Count('id'))['ac'] or 0
    total_excess_insurance_claims = insurance_list.aggregate(ac=Sum('excess'))['ac'] or 0
    total_insurance_claims = insurance_list.aggregate(ac=Sum('payout_amount'))['ac'] or 0

    inspections = MileageLog.objects.filter(driver=driver).order_by("-id")
    incidences = Incident.objects.filter(driver=driver).order_by("-id")
    count_incidences = incidences.aggregate(ac=Count('id'))['ac'] or 0

    form = DrivingLicenceForm(request.POST or None, instance=transaction)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')    
    uploads = FileUpload.objects.filter(vehicle=vehicle, transaction_id=vehicle.id, transaction="Vehicle")
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]
    comment_form = CommentsForm(request.POST or None)
    comments = Comment.objects.filter(vehicle = vehicle).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    
    context ={
        "title": title, 
        "form":form,       
        "driver": driver,
        "driving_licence":transaction,        
        "vehicle": vehicle,
        "upload_file_form": upload_file_form,
        "uploads": uploads,
        "sliders": images,
        'filter_form': filter_form,
        "comments": comments,
        "comment_form": comment_form,
        "allocations_list":allocations_list,
        "count_allocations":count_allocations,
        "traffic_fines":traffic_fines,
        "count_traffic_fines":count_traffic_fines,
        "count_court_appearences":count_court_appearences,
        "count_serious_offences":count_serious_offences,
        "total_traffic_fines":total_traffic_fines,
        "maintenance_list":maintenance_list,
        "total_maintenance":total_maintenance,
        "total_service":total_service,
        "total_tyres":total_tyres,
        "total_repairs":total_repairs,
        "claims":insurance_list,
        "count_insurance_claims":count_insurance_claims,
        "count_pending_insurance_claims":count_pending_insurance_claims,
        "total_excess_insurance_claims":total_excess_insurance_claims,
        "total_insurance_claims":total_insurance_claims,
        "mileage_log":inspections,
        "incidences_list":incidences,
        "edit_licence":True,
        }
    post = request.POST
    if request.POST:
        if u'save' in post:

            comment = comment_form.is_valid()
            if comment:
                new_comment = comment_form.save(commit=False)
                new_comment.vehicle = vehicle
                new_comment.comment_type = "Vehicle"
                new_comment.obj_id = vehicle.id
                new_comment.created_by = request.user
                new_comment.save()

            validated = upload_file_form.is_valid()
            if validated:
                files = request.FILES.getlist('doc-file')
                for f in files:
                    uploaded = FileUpload.objects.create(file=f)
                    uploaded.transaction_id = vehicle.id
                    uploaded.vehicle = vehicle
                    uploaded.file_name = uploaded.file.name
                    uploaded.transaction = "Vehicle"
                    uploaded.save()
            return HttpResponseRedirect(reverse('fleet:viewvehicle', kwargs={'vehicle_id':vehicle.id}))
    return render(request, "viewDriverProfile.html", context)

@login_required
@permission_required('fleet.view_insuranceclaim', raise_exception=True)
def drivingLicencesList(request):
    licences =  DrivingLicence.objects.all().order_by('driver__branch__region', 'driver__first_name')
    if request.user.regional_staff:
        licences =  licences.filter(driver__branch__region=request.user.employee.branch.region)

    title = "Driving Licences List"    
    driving_licences = licences
    date = 'expiry_date' 
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_driving_licences' in request.GET and filter_form.is_valid():
        driving_licences = filter_form.filter(driving_licences, date)   
    page = request.GET.get('page', 1)
    driving_licences_paginator = Paginator(driving_licences, 14)
    try:
        driving_licences = driving_licences_paginator.page(page)
    except PageNotAnInteger:
        driving_licences = driving_licences_paginator.page(1)
    except EmptyPage:
        driving_licences = driving_licences_paginator.page(driving_licences_paginator.num_pages)

    due_expiry_date = datetime.now() + timedelta(+30)
    expired_date = datetime.now() + timedelta(-1)
    todays_date = datetime.now()+ timedelta()

    expiring_driving_licences = licences.filter(expiry_date__range=[todays_date, due_expiry_date]).order_by('-id')
    if u'filter_expiring_driving_licences' in request.GET and filter_form.is_valid():
        expiring_driving_licences = filter_form.filter(expiring_driving_licences, date)   
    expiring_driving_licences_paginator = Paginator(expiring_driving_licences, 14)
    try:
        expiring_driving_licences = expiring_driving_licences_paginator.page(page)
    except PageNotAnInteger:
        expiring_driving_licences = expiring_driving_licences_paginator.page(1)
    except EmptyPage:
        expiring_driving_licences = expiring_driving_licences_paginator.page(expiring_driving_licences_paginator.num_pages)

    expired_driving_licences = licences.filter(expiry_date__lte=expired_date).order_by('-id')
    if u'filter_expired_driving_licences' in request.GET and filter_form.is_valid():
        date = 'claims_finalized'   
        expired_driving_licences = filter_form.filter(expired_driving_licences, date)
    expired_driving_licences_paginator = Paginator(expired_driving_licences, 14)
    try:
        expired_driving_licences = expired_driving_licences_paginator.page(page)
    except PageNotAnInteger:
        expired_driving_licences = expired_driving_licences_paginator.page(1)
    except EmptyPage:
        expired_driving_licences = expired_driving_licences_paginator.page(expired_driving_licences_paginator.num_pages)

    
    context ={
        "title": title,
        "driving_licences": driving_licences,
        "expiring_driving_licences": expiring_driving_licences,
        "expired_driving_licences": expired_driving_licences,
        "filter_form": filter_form,
        }       
    return render(request, "drivingLicencesList.html", context)


@login_required
@permission_required('fleet.create_vehicle', raise_exception=True)
def addvehicle(request):
    title = "Add New Vehicle"
    form = addNewVehicleForm(request.POST or None)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    context ={
        "title": title,
        "form": form,
        "comment_form": comment_form,
        "upload_file_form": upload_file_form,
        "addvehicle":True

        }

    post = request.POST
    if request.POST:
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by = request.user
                save_form.save()

                latest_trans = Vehicle.objects.order_by('-id')[0]

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.vehicle = latest_trans
                    new_comment.comment_type = "Vehicle"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = FileUpload.objects.create(file=f)
                        uploaded.transaction_id = latest_trans.id
                        uploaded.vehicle = latest_trans
                        uploaded.file_name = uploaded.file.name
                        uploaded.transaction = "Vehicle"
                        uploaded.save()

                return HttpResponseRedirect(reverse('fleet:viewvehicle', kwargs={'vehicle_id':latest_trans.id}))

    return render(request, "vehicles.html", context)




@login_required
@permission_required('fleet.edit_vehicle', raise_exception=True)
def editvehicle(request, vehicle_id):

    title = "Edit Vehicle"
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    creator = ElopsysUser.objects.get(pk=vehicle.created_by_id)
    form = addNewVehicleForm(request.POST or None, instance=vehicle)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUpload.objects.filter(vehicle=vehicle, transaction_id=vehicle.id, transaction="Vehicle")
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = Comment.objects.filter(vehicle = vehicle).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
        "title": title,
        "form": form,
        "comment_form": comment_form,
        "vehicle": vehicle,
        "upload_file_form": upload_file_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,

        }
    post = request.POST
    if request.POST:
        if u'save' in post:
            valid_form = form.is_valid()

            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by = creator
                save_form.modified_by = request.user
                save_form.save()

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.vehicle = vehicle
                    new_comment.comment_type = "Vehicle"
                    new_comment.obj_id = vehicle.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = FileUpload.objects.create(file=f)
                        uploaded.transaction_id = vehicle.id
                        uploaded.vehicle = vehicle
                        uploaded.file_name = f.name
                        uploaded.transaction = "Vehicle"
                        uploaded.save()
                return HttpResponseRedirect(reverse('fleet:viewvehicle', kwargs={'vehicle_id':vehicle.id}))
    return render(request, "vehicles.html", context)


@login_required
@permission_required('fleet.edit_vehicle', raise_exception=True)
def viewvehicleDetails(request, vehicle_id):

    title = "View Vehicle"
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    creator = ElopsysUser.objects.get(pk=vehicle.created_by_id)
    form = addNewVehicleForm(request.POST or None, instance=vehicle)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUpload.objects.filter(vehicle=vehicle, transaction_id=vehicle.id, transaction="Vehicle")
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = Comment.objects.filter(vehicle = vehicle).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
        "title": title,
        "form": form,
        "comment_form": comment_form,
        "vehicle": vehicle,
        "upload_file_form": upload_file_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,
        "view_transaction":True,

        }

    return render(request, "vehicles.html", context)

@login_required
@permission_required('fleet.view_vehicle', raise_exception=True)
def vehiclesList(request):

    fleet =  Vehicle.objects.all().order_by('current_driver__branch__region', 'current_driver__first_name')
    if request.user.regional_staff:
        fleet =  Vehicle.objects.filter(current_driver__branch__region=request.user.employee.branch.region)

    title = "Vehicles List"
    all_fleet = fleet.filter(available=0, active=1).select_related()
    date = 'purchase_date'
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_fleet' in request.GET and filter_form.is_valid():

        all_fleet = filter_form.filter(all_fleet, date)
    page = request.GET.get('page', 1)
    all_fleet_paginator = Paginator(all_fleet, 14)

    try:
        all_fleet = all_fleet_paginator.page(page)
    except PageNotAnInteger:
        all_fleet = all_fleet_paginator.page(1)
    except EmptyPage:
        all_fleet = all_fleet_paginator.page(all_fleet_paginator.num_pages)

    drivers_licence = DrivingLicence()
    licence_form = DrivingLicenceForm(request.POST or None, instance=drivers_licence)

    el_fleet = fleet.filter(ownership_type="EL Fleet", available=0, active=1).select_related()
    date = 'purchase_date'
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_fleet' in request.GET and filter_form.is_valid():
        el_fleet = filter_form.filter(el_fleet, date)
    page = request.GET.get('page', 1)
    fleet_paginator = Paginator(el_fleet, 14)
    try:
        el_fleet = fleet_paginator.page(page)
    except PageNotAnInteger:
        el_fleet = fleet_paginator.page(1)
    except EmptyPage:
        el_fleet = fleet_paginator.page(fleet_paginator.num_pages)

    el_leased = fleet.filter(ownership_type="EL Leased", available=0, active=1).select_related()
    date = 'purchase_date'
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_leased' in request.GET and filter_form.is_valid():
        el_leased = filter_form.filter(el_leased, date)
    page = request.GET.get('page', 1)
    fleet_paginator = Paginator(el_leased, 14)
    try:
        el_leased = fleet_paginator.page(page)
    except PageNotAnInteger:
        el_leased = fleet_paginator.page(1)
    except EmptyPage:
        el_leased = fleet_paginator.page(fleet_paginator.num_pages)

    el_rentals = fleet.filter(ownership_type="EL Rental", available=0, active=1)
    if u'filter_rentals' in request.GET and filter_form.is_valid():
        el_rentals = filter_form.filter(el_rentals, date)
    rentals_paginator = Paginator(el_rentals, 14)
    try:
        el_rentals = rentals_paginator.page(page)
    except PageNotAnInteger:
        el_rentals = rentals_paginator.page(1)
    except EmptyPage:
        el_rentals = rentals_paginator.page(rentals_paginator.num_pages)

    el_staff = fleet.filter(ownership_type="EL Staff", available=0, active=1)
    if u'filter_staff' in request.GET and filter_form.is_valid():
        el_staff = filter_form.filter(el_staff, date)
    staff_paginator = Paginator(el_staff, 14)
    try:
        el_staff = staff_paginator.page(page)
    except PageNotAnInteger:
        el_staff = staff_paginator.page(1)
    except EmptyPage:
        el_staff = staff_paginator.page(staff_paginator.num_pages)

    available_fleet = fleet.filter(available=1, active=1)
    if u'filter_available' in request.GET and filter_form.is_valid():
        available_fleet = filter_form.filter(available_fleet, date)
    available_fleet_paginator = Paginator(available_fleet, 14)
    try:
        available_fleet = available_fleet_paginator.page(page)
    except PageNotAnInteger:
        available_fleet = available_fleet_paginator.page(1)
    except EmptyPage:
        available_fleet = available_fleet_paginator.page(available_fleet_paginator.num_pages)


    inactive_fleet = fleet.filter(active=0)
    if u'filter_inactive' in request.GET and filter_form.is_valid():
        inactive_fleet = filter_form.filter(inactive_fleet, date)
    inactive_fleet_paginator = Paginator(inactive_fleet, 14)
    try:
        inactive_fleet = inactive_fleet_paginator.page(page)
    except PageNotAnInteger:
        inactive_fleet = inactive_fleet_paginator.page(1)
    except EmptyPage:
        inactive_fleet = inactive_fleet_paginator.page(inactive_fleet_paginator.num_pages)


    out_of_smp_fleet = fleet.filter(Q(on_service_plan=True) | Q(on_maintenance_plan=True),
                                              plan_ending__lte=datetime.now()+timedelta(),
                                              active=True)
    if u'filter_out_of_smp' in request.GET and filter_form.is_valid():
        out_of_smp_fleet = filter_form.filter(out_of_smp_fleet, date)
    out_of_smp_fleet_paginator = Paginator(out_of_smp_fleet, 14)
    try:
        out_of_smp_fleet = out_of_smp_fleet_paginator.page(page)
    except PageNotAnInteger:
        out_of_smp_fleet = out_of_smp_fleet_paginator.page(1)
    except EmptyPage:
        out_of_smp_fleet = out_of_smp_fleet_paginator.page(out_of_smp_fleet_paginator.num_pages)


    written_off_fleet = fleet.filter(status="Write Off")
    if u'filter_writeoffs' in request.GET and filter_form.is_valid():
        written_off_fleet = filter_form.filter(written_off_fleet, date)
    written_off_fleet_fleet_paginator = Paginator(written_off_fleet, 14)
    try:
        written_off_fleet = written_off_fleet_fleet_paginator.page(page)
    except PageNotAnInteger:
        written_off_fleet = written_off_fleet_fleet_paginator.page(1)
    except EmptyPage:
        written_off_fleet = written_off_fleet_fleet_paginator.page(written_off_fleet_fleet_paginator.num_pages)

    context ={
        "title": title,
        "all_fleet":all_fleet,
        "licence_form":licence_form,
        "el_fleet": el_fleet,
        "el_leased": el_leased,
        "el_rentals": el_rentals,
        "el_staff": el_staff,
        'available_fleet': available_fleet,
        "out_of_smp_fleet": out_of_smp_fleet,
        "inactive_fleet": inactive_fleet,
        "written_off_fleet": written_off_fleet,
        "filter_form": filter_form,
        }

    post = request.POST
    if request.POST:
        if u'save_modal' in post:
            valid_licence = licence_form.is_valid()
            if valid_licence:
                save_licence_form = licence_form.save(commit=False)
                save_licence_form.created_by = request.user
                save_licence_form.save()
                return HttpResponseRedirect(reverse('fleet:vehiclesList'))
    return render(request, "vehiclesList.html", context)


@login_required
@permission_required('fleet.create_fuelcard', raise_exception=True)
def fuelcard (request):
    title = "Fuel Cards"
    form = FuelCardForm(request.POST or None)
    comment_form = CommentsForm(request.POST or None)
    context = {
     'title': title,
     'form': form,
    }

    post = request.POST
    if request.POST:
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by = request.user
                save_form.save()


    return render(request, "adhocform.html", context)



@login_required
@permission_required('fleet.create_fuelallocation', raise_exception=True)
def allocatefuel(request, vehicle_id):
    title = "Allocate Fuel"

    vehicle = Vehicle.objects.get(pk=vehicle_id)
    filter_options =['Allocate Sim And Fuel Card','Allocate Fuel Card']
    fuel_allocation = FuelAllocation()
    fuel_allocation.vehicle = vehicle
    fuel_allocation.mileage = vehicle.get_current_mileage()
    if vehicle.get_current_driver() != "Not Allocated":
        fuel_allocation.driver = vehicle.get_current_driver()
        card_allocation=CardAllocation.objects.filter(employee=fuel_allocation.driver, allocation_type__in=filter_options).order_by('-id').first()
        if card_allocation:
            fuel_allocation.fuel_card = card_allocation.fuel_card
            fuel_allocation.amount_allocated = card_allocation.fuel_cycle_limit
        fuel_allocation.balance = vehicle.fuel_balance



    form = FuelAllocationForm(request.POST or None, instance=fuel_allocation, user=request.user)
    comment_form = CommentsForm(request.POST or None)

    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUpload.objects.filter(vehicle=vehicle).filter(transaction="FuelAllocation")
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = Comment.objects.filter(vehicle = vehicle).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
        "title": title,
        "form": form,
        "comment_form": comment_form,
        "vehicle": vehicle,
        "upload_file_form":upload_file_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,
    }
    post = request.POST
    if request.POST:
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by = request.user
                save_form.save()
                if fuel_allocation.transaction_type =="Top up":
                    vehicle.fuel_balance = fuel_allocation.new_balance
                else:
                    vehicle.fuel_balance = fuel_allocation.amount_allocated
                vehicle.save()
                latest_trans = FuelAllocation.objects.order_by('-id')[0]

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.vehicle = latest_trans.vehicle
                    new_comment.comment_type = "FuelAllocation"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = FileUpload.objects.create(file=f)
                        uploaded.transaction_id = latest_trans.id
                        uploaded.vehicle = latest_trans.vehicle
                        uploaded.file_name = uploaded.file.name
                        uploaded.transaction = "FuelAllocation"
                        uploaded.save()
                return HttpResponseRedirect(reverse('fleet:requisition_vehiclefuelallocation', kwargs={'obj_id':latest_trans.id}))
    return render(request, "vehicles.html", context)



@login_required
@permission_required('fleet.edit_fuelallocation', raise_exception=True)
def editallocatefuel(request, trans_id):
    title = "Allocate Vehicle"
    transaction = FuelAllocation.objects.get(pk=trans_id)
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)
    vehicle = transaction.vehicle
    trans_key = transaction.id
    vehicle_id = Vehicle.objects.filter(licence_plate=vehicle)
    vehicle = Vehicle.objects.get(pk=vehicle_id)

    try:
        requisition = Requisition.objects.get(obj_id=trans_id, requisition_type="FuelAllocation")
    except Requisition.DoesNotExist:
        requisition = None

    form = FuelAllocationForm(request.POST or None, instance=transaction, user=request.user)
    comment_form = CommentsForm(request.POST or None)

    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUploads.objects.filter(vehicle=vehicle, transaction="FuelAllocation", transaction_id=trans_key)
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUploads.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = Comment.objects.filter(vehicle = vehicle).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
        "title": title,
        "form": form,
        "comment_form": comment_form,
        "vehicle": vehicle,
        "upload_file_form":upload_file_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,

    }

    post = request.POST
    if request.POST:
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by = creator
                save_form.modified_by = request.user
                save_form.save()
                vehicle.current_driver = transaction.driver
                vehicle.save()

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.vehicle = vehicle
                    new_comment.comment_type = "FuelAllocation"
                    new_comment.obj_id = transaction.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = FileUpload.objects.create(file=f)
                        uploaded.transaction_id = transaction.id
                        uploaded.vehicle = vehicle
                        uploaded.file_name = uploaded.file.name
                        uploaded.transaction = "FuelAllocation"
                        uploaded.save()
                if request.user.has_perm('authorize_fuelallocation'):
                    if requisition:
                        return HttpResponseRedirect(reverse('fleet:view_requisition', kwargs={'obj_id':requisition.id}))
                    else:
                        return HttpResponseRedirect(reverse('fleet:authorizations'))
                else:
                    return HttpResponseRedirect(reverse('fleet:viewvehicle', kwargs={'vehicle_id':vehicle.id}))
    return render(request, "vehicles.html", context)


@csrf_exempt
def validateDriver(request):
    t_driver = request.GET.get('driver', None)
    driver = Employee.objects.get(id=t_driver)
    valid_drivers = DrivingLicence.objects.filter(driver_id=driver).order_by('-id')
    has_no_licence = False
    if len(valid_drivers)==0:
        has_no_licence = True

    data = {
            'driver':driver.id,
            'driver_name':driver.first_name,
            'has_no_licence':has_no_licence,
         }

    results = json.dumps(data)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)


@csrf_exempt
def getFromFuelTrfDetails(request):

    f_driver = request.GET.get('from_driver', None)
    f_vehicle = request.GET.get('from_vehicle', None)
    filter_options =['Allocate Sim And Fuel Card','Allocate Fuel Card']

    if f_driver:
        from_driver=Employee.objects.get(id=f_driver).id
        va = VehicleAllocation.objects.filter(driver=f_driver).order_by('-allocation_date', '-id').first()
        if va:
            vehicle = Vehicle.objects.get(pk=va.vehicle_id)
            from_vehicle=vehicle.id
            from_balance = vehicle.fuel_balance
        else:
            from_vehicle=None
            from_balance=0

        card_allocation = CardAllocation.objects.filter(employee=from_driver, allocation_type__in=filter_options).order_by('-id').first()
        if card_allocation:
            from_fuel_card = card_allocation.fuel_card.id
        else:
            from_fuel_card=None

    elif f_vehicle:
        vehicle = Vehicle.objects.get(id=f_vehicle)
        from_vehicle=vehicle.id
        driver = vehicle.get_current_driver()
        from_driver=driver.id
        from_balance = from_vehicle.fuel_balance
        card_allocation = CardAllocation.objects.filter(employee=from_driver, allocation_type__in=filter_options).order_by('-id').first()
        if card_allocation:
            from_fuel_card = card_allocation.fuel_card.id
        else:
            from_fuel_card=None



        # do whatever processing you need
        # user.some_property = whatever

        # send back whatever properties you have updated
    data = {
             'from_vehicle': from_vehicle,
             'from_driver': from_driver,
             'from_fuel_card': from_fuel_card,
             'from_balance': from_balance,

            }
    print data
    results = json.dumps(data)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)
    # return HttpResponse(json.dumps(json_response),
    #                     content_type='application/json')
    #return render(request, 'vehicles.html', {'from_driver': '','from_driver': '','from_fuel_card': '','from_balance': ''})


@csrf_exempt
def getToFuelTrfDetails(request):

    t_driver = request.GET.get('driver', None)
    t_vehicle = request.GET.get('vehicle', None)
    filter_options =['Allocate Sim And Fuel Card','Allocate Fuel Card']

    if t_driver:
        driver=Employee.objects.get(id=t_driver).id
        va = VehicleAllocation.objects.filter(driver=t_driver).order_by('allocation_date','-id').first()
        if va:
            vcl = Vehicle.objects.get(pk=va.vehicle_id)
            vehicle=vcl.id
            to_balance = vcl.fuel_balance
        else:
            vehicle=None
            to_balance=0

        card_allocation = CardAllocation.objects.filter(employee=driver, allocation_type__in=filter_options).order_by('-id').first()
        if card_allocation:
            to_fuel_card = card_allocation.fuel_card.id
        else:
            to_fuel_card=None

    elif t_vehicle:
        vcl = Vehicle.objects.get(id=t_vehicle)
        vehicle = vehicle.id
        drv = vcl.get_current_driver()
        driver = drv.id
        to_balance = vcl.fuel_balance
        card_allocation = CardAllocation.objects.filter(employee=driver, allocation_type__in=filter_options).order_by('-id').first()
        if card_allocation:
            to_fuel_card = card_allocation.fuel_card.id
        else:
            to_fuel_card = None



        # do whatever processing you need
        # user.some_property = whatever

        # send back whatever properties you have updated
    data = {
             'vehicle': vehicle,
             'driver': driver,
             'to_fuel_card': to_fuel_card,
             'to_balance': to_balance,

            }
    results = json.dumps(data)
    mimetype = 'application/json'
    return HttpResponse(results, mimetype)

    # return HttpResponse(json.dumps(json_response),
    #                     content_type='application/json')
    #return render(request, 'vehicles.html', {'driver': '','driver': '','from_fuel_card': '','from_balance': ''})


@login_required
@permission_required('fleet.create_fueltransfer', raise_exception=True)
def fuelTransfer(request):
    title = "Fuel Transfer"
    form = FuelTransferForm(request.POST or None, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')


    context ={
        "title": title,
        "form": form,
        "comment_form": comment_form,
        "upload_file_form":upload_file_form,
        "addvehicle":True
    }

    post = request.POST
    if request.POST:
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by = request.user
                save_form.save()

                latest_trans = FuelTransfer.objects.order_by('-id')[0]
                fv=Vehicle.objects.get(id=latest_trans.from_vehicle.id)
                fv.fuel_balance = latest_trans.from_new_balance
                fv.save()

                tv=Vehicle.objects.get(id=latest_trans.vehicle.id)
                tv.fuel_balance = latest_trans.to_new_balance
                tv.save()

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.vehicle = latest_trans.vehicle
                    new_comment.comment_type = "FuelTransfer"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = FileUpload.objects.create(file=f)
                        uploaded.transaction_id = latest_trans.id
                        uploaded.vehicle = latest_trans.vehicle
                        uploaded.file_name = uploaded.file.name
                        uploaded.transaction = "FuelTransfer"
                        uploaded.save()
                return HttpResponseRedirect(reverse('fleet:requisition_vehiclefueltransfer', kwargs={'obj_id':latest_trans.id}))
    return render(request, "vehicles.html", context)

@login_required
@permission_required('fleet.create_vehicleallocation', raise_exception=True)
def allocatevehicle_redirected(request, vehicle_id, driver_id):

    title = "Allocate Vehicle"

    vehicle = Vehicle.objects.get(pk=vehicle_id)
    vehicle_allocation = VehicleAllocation()
    vehicle_allocation.vehicle = vehicle
    vehicle_allocation.mileage = vehicle.get_current_mileage()
    if vehicle.get_current_driver() != "Not Allocated":
        vehicle_allocation.driver = Employee.objects.get(pk=driver_id)

    form = VehicleAllocationForm(request.POST or None, instance=vehicle_allocation, user=request.user)
    # driver = Employee.objects.filter(id=int(river_id)).first()
    comment_form = CommentsForm(request.POST or None)
    drivers_licence = DrivingLicence(driver=vehicle_allocation.driver)
    licence_form = DrivingLicenceForm(request.POST or None, instance=drivers_licence)
    has_no_licence = False
    dr_licence = DrivingLicence.objects.filter(driver=vehicle_allocation.driver)
    if len(dr_licence)==0:
        has_no_licence = True
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUpload.objects.filter(vehicle=vehicle, transaction="VehicleAllocation")
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]
    allocations_list = VehicleAllocation.objects.filter(vehicle=vehicle).order_by("-id")
    page = request.GET.get('page', 1)
    paginator = Paginator(allocations_list, 14)
    try:
        allocations_list = paginator.page(page)
    except PageNotAnInteger:
        allocations_list = paginator.page(1)
    except EmptyPage:
        allocations_list = paginator.page(paginator.num_pages)
    comments = Comment.objects.filter(vehicle = vehicle).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    # import pdb; pdb.set_trace()
    context ={
        "title": title,
        "form": form,
        "licence_form": licence_form,
        "has_no_licence":has_no_licence,
        "comment_form": comment_form,
        "vehicle": vehicle,
        "upload_file_form":upload_file_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,
        "allocations_list":allocations_list,
    }
    # import pdb; pdb.set_trace()

    post = request.POST
    if request.POST:

        if u'save_modal' in post:
            valid_licence = licence_form.is_valid()
            if valid_licence:
                save_licence_form = licence_form.save(commit=False)
                save_licence_form.created_by = request.user
                save_licence_form.save()

                return HttpResponseRedirect(reverse('fleet:allocatevehicle_redirected', kwargs={'vehicle_id':vehicle.id, 'driver_id':save_licence_form.driver.id, }))
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by = request.user
                save_form.save()

                latest_trans = VehicleAllocation.objects.order_by('-id')[0]

                vehicle.status = latest_trans.status
                vehicle.current_driver = latest_trans.driver
                if latest_trans.transaction_type == "Returned":
                    vehicle.available = 1
                if latest_trans.transaction_type == "Returned_To_SP" or vehicle_allocation.status == "Write Off":
                    vehicle.active = 0
                if latest_trans.transaction_type == "Allocated":
                    vehicle.available = 0
                vehicle.save()

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.vehicle = latest_trans.vehicle
                    new_comment.comment_type = "VehicleAllocation"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = FileUpload.objects.create(file=f)
                        uploaded.transaction_id = latest_trans.id
                        uploaded.vehicle = latest_trans.vehicle
                        uploaded.file_name = uploaded.file.name
                        uploaded.transaction = "VehicleAllocation"
                        uploaded.save()
                return HttpResponseRedirect(reverse('fleet:viewvehicle', kwargs={'vehicle_id':vehicle.id}))
    return render(request, "vehicles.html", context)

@login_required
@permission_required('fleet.create_vehicleallocation', raise_exception=True)
def allocatevehicle(request, vehicle_id):

    title = "Allocate Vehicle"

    vehicle = Vehicle.objects.get(pk=vehicle_id)
    vehicle_allocation = VehicleAllocation()
    vehicle_allocation.vehicle = vehicle
    vehicle_allocation.mileage = vehicle.get_current_mileage()
    if vehicle.get_current_driver() != "Not Allocated":

        driver_id = request.POST.get("driver_id", "")
        if driver_id !="":
            vehicle_allocation.driver = Employee.objects.get(id=int(driver_id))
        else:
            vehicle_allocation.driver = vehicle.get_current_driver()

    form = VehicleAllocationForm(request.POST or None, instance=vehicle_allocation, user=request.user)
    # driver = Employee.objects.filter(id=int(river_id)).first()
    comment_form = CommentsForm(request.POST or None)
    drivers_licence = DrivingLicence(driver=vehicle_allocation.driver)
    licence_form = DrivingLicenceForm(request.POST or None, instance=drivers_licence)
    has_no_licence = False
    dr_licence = DrivingLicence.objects.filter(driver=vehicle_allocation.driver)
    if len(dr_licence)==0:
        has_no_licence = True
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUpload.objects.filter(vehicle=vehicle, transaction="VehicleAllocation")
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]
    allocations_list = VehicleAllocation.objects.filter(vehicle=vehicle).order_by("-id")
    page = request.GET.get('page', 1)
    paginator = Paginator(allocations_list, 14)
    try:
        allocations_list = paginator.page(page)
    except PageNotAnInteger:
        allocations_list = paginator.page(1)
    except EmptyPage:
        allocations_list = paginator.page(paginator.num_pages)
    comments = Comment.objects.filter(vehicle = vehicle).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    # import pdb; pdb.set_trace()
    context ={
        "title": title,
        "form": form,
        "licence_form": licence_form,
        "has_no_licence":has_no_licence,
        "comment_form": comment_form,
        "vehicle": vehicle,
        "upload_file_form":upload_file_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,
        "allocations_list":allocations_list,
    }
    # import pdb; pdb.set_trace()

    post = request.POST
    if request.POST:

        if u'save_modal' in post:
            valid_licence = licence_form.is_valid()
            if valid_licence:
                save_licence_form = licence_form.save(commit=False)
                save_licence_form.created_by = request.user
                save_licence_form.save()

                return HttpResponseRedirect(reverse('fleet:allocatevehicle_redirected',
                                                     kwargs={'vehicle_id':vehicle.id,
                                                             'driver_id':save_licence_form.driver.id, }))
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by = request.user
                save_form.save()

                latest_trans = VehicleAllocation.objects.order_by('-id')[0]

                vehicle.status = latest_trans.status
                vehicle.current_driver = latest_trans.driver
                if latest_trans.transaction_type == "Returned":
                    vehicle.available = 1
                if latest_trans.transaction_type == "Returned_To_SP" or vehicle_allocation.status == "Write Off":
                    vehicle.active = 0
                if latest_trans.transaction_type == "Allocated":
                    vehicle.available = 0
                vehicle.save()

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.vehicle = latest_trans.vehicle
                    new_comment.comment_type = "VehicleAllocation"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = FileUpload.objects.create(file=f)
                        uploaded.transaction_id = latest_trans.id
                        uploaded.vehicle = latest_trans.vehicle
                        uploaded.file_name = uploaded.file.name
                        uploaded.transaction = "VehicleAllocation"
                        uploaded.save()
                return HttpResponseRedirect(reverse('fleet:viewvehicle', kwargs={'vehicle_id':vehicle.id}))
    return render(request, "vehicles.html", context)


@login_required
@permission_required('fleet.edit_vehicleallocation', raise_exception=True)
def editallocatevehicle(request, trans_id):
    title = "Allocate Vehicle"
    transaction = VehicleAllocation.objects.get(pk=trans_id)
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)
    vehicle = transaction.vehicle
    trans_key = transaction.id
    vehicle_id = Vehicle.objects.filter(licence_plate=vehicle)
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    form = VehicleAllocationForm(request.POST or None, instance=transaction, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    allocations_list = VehicleAllocation.objects.filter(vehicle=vehicle).order_by("-id")
    page = request.GET.get('page', 1)
    paginator = Paginator(allocations_list, 14)
    try:
        allocations_list = paginator.page(page)
    except PageNotAnInteger:
        allocations_list = paginator.page(1)
    except EmptyPage:
        allocations_list = paginator.page(paginator.num_pages)

    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUpload.objects.filter(vehicle=vehicle, transaction="VehicleAllocation", transaction_id=trans_key)
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = Comment.objects.filter(vehicle = vehicle).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
        "title": title,
        "form": form,
        "comment_form": comment_form,
        "vehicle": vehicle,
        "upload_file_form":upload_file_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,
        "allocations_list":allocations_list,
    }

    post = request.POST
    if request.POST:
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by = creator
                save_form.modified_by=request.user
                save_form.save()

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.vehicle = vehicle
                    new_comment.comment_type = "VehicleAllocation"
                    new_comment.obj_id = transaction.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = FileUpload.objects.create(file=f)
                        uploaded.transaction_id = transaction.id
                        uploaded.vehicle = vehicle
                        uploaded.file_name = uploaded.file.name
                        uploaded.transaction = "VehicleAllocation"
                        uploaded.save()
                if request.user.has_perm('authorize_vehicleallocation'):
                    return HttpResponseRedirect(reverse('fleet:authorizations'))
                else:
                    return HttpResponseRedirect(reverse('fleet:viewvehicle', kwargs={'vehicle_id':vehicle.id}))
    return render(request, "vehicles.html", context)

@login_required
@permission_required('fleet.view_vehicleallocation', raise_exception=True)
def viewallocatevehicle(request, trans_id):
    title = "View Vehicle Allocation"
    transaction = VehicleAllocation.objects.get(pk=trans_id)
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)
    vehicle = transaction.vehicle
    trans_key = transaction.id
    vehicle_id = Vehicle.objects.filter(licence_plate=vehicle)
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    form = VehicleAllocationForm(request.POST or None, instance=transaction, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    allocations_list = VehicleAllocation.objects.filter(vehicle=vehicle).order_by("-id")
    page = request.GET.get('page', 1)
    paginator = Paginator(allocations_list, 14)
    try:
        allocations_list = paginator.page(page)
    except PageNotAnInteger:
        allocations_list = paginator.page(1)
    except EmptyPage:
        allocations_list = paginator.page(paginator.num_pages)

    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUpload.objects.filter(vehicle=vehicle, transaction="VehicleAllocation", transaction_id=trans_key)
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = Comment.objects.filter(vehicle = vehicle).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
        "title": title,
        "form": form,
        "comment_form": comment_form,
        "vehicle": vehicle,
        "upload_file_form":upload_file_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,
        "allocations_list":allocations_list,
        "view_transaction":True,
    }
    return render(request, "vehicles.html", context)


@login_required
@permission_required('fleet.view_vehicleallocation', raise_exception=True)
def fleetAllocationsList(request):
    fleet =  Vehicle.objects.all()
    allocations = VehicleAllocation.objects.all()
    fuel_allocations = FuelAllocation.objects.all()
    fuel_transfers = FuelTransfer.objects.all()
    if request.user.regional_staff:
        fleet =  Vehicle.objects.filter(current_driver__branch__region=request.user.employee.branch.region)
        allocations = VehicleAllocation.objects.filter(driver__branch__region=request.user.employee.branch.region)
        fuel_allocations = FuelAllocation.objects.filter(driver__branch__region=request.user.employee.branch.region)
        fuel_transfers = FuelTransfer.objects.filter(driver__branch__region=request.user.employee.branch.region)

    title = "Vehicle Allocations List"
    allocations_list = allocations.order_by("-id")

    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter' in request.GET and filter_form.is_valid():
        date = 'allocation_date'
        allocations_list = filter_form.filter(allocations_list, date)

    page = request.GET.get('page', 1)
    paginator = Paginator(allocations_list, 14)
    try:
        allocations_list = paginator.page(page)
    except PageNotAnInteger:
        allocations_list = paginator.page(1)
    except EmptyPage:
        allocations_list = paginator.page(paginator.num_pages)


    available_fleet = fleet.filter(available=1, active=1)
    if u'filter_available' in request.GET and filter_form.is_valid():
        date = "purchase_date"
        available_fleet = filter_form.filter(available_fleet, date)
    available_fleet_paginator = Paginator(available_fleet, 14)
    try:
        available_fleet = available_fleet_paginator.page(page)
    except PageNotAnInteger:
        available_fleet = available_fleet_paginator.page(1)
    except EmptyPage:
        available_fleet = available_fleet_paginator.page(available_fleet_paginator.num_pages)

    fuel_allocations_list = fuel_allocations.order_by('-id')
    if u'filter_fuel' in request.GET and filter_form.is_valid():
        date = 'allocation_date'
        fuel_allocations_list = filter_form.filter(fuel_allocations_list, date)
    fuel_allocations_list_paginator = Paginator(fuel_allocations_list, 14)
    try:
        fuel_allocations_list = fuel_allocations_list_paginator.page(page)
    except PageNotAnInteger:
        fuel_allocations_list = fuel_allocations_list_paginator.page(1)
    except EmptyPage:
        fuel_allocations_list = fuel_allocations_list_paginator.page(fuel_allocations_list_paginator.num_pages)

    fueltransfers = fuel_transfers.order_by('-id')
    if u'filter_fueltransfers' in request.GET and filter_form.is_valid():
        date = 'transfer_date'
        fueltransfers = filter_form.filter(fueltransfers, date)
    fueltransfers_paginator = Paginator(fueltransfers, 14)
    try:
        fueltransfers = fueltransfers_paginator.page(page)
    except PageNotAnInteger:
        fueltransfers = fueltransfers_paginator.page(1)
    except EmptyPage:
        fueltransfers = fueltransfers_paginator.page(fueltransfers_paginator.num_pages)

    post = request.POST
    if request.POST:
        if u'reload_fuel' in post:
            vehicles = Vehicle.objects.filter(active=True, available=False)
            for v in vehicles:
                fuel_allocation = FuelAllocation()
                fuel_allocation.vehicle = v
                fuel_allocation.allocation_date = datetime.now()
                fuel_allocation.transaction_type = "Monthly Allocation"
                fuel_allocation.driver = v.get_current_driver()
                fuel_allocation.fuel_card = v.get_fuel_card()
                fuel_allocation.balance = v.fuel_balance
                fuel_allocation.amount_allocated = v.get_cycle_limit()
                fuel_allocation.new_balance = fuel_allocation.balance + fuel_allocation.amount_allocated
                fuel_allocation.save()
                v.fuel_balance = fuel_allocation.amount_allocated
                v.save()

    context ={
        "title": title,
        "allocations_list": allocations_list,
        "filter_form":filter_form,
        "available_fleet": available_fleet,
        "fuel_allocations_list": fuel_allocations_list,
        "fueltransfers": fueltransfers,
        }
    return render(request, "fleetAllocationsList.html", context)


@login_required
@permission_required('fleet.create_servicebooking', raise_exception=True)
def bookservice(request, vehicle_id):
    title = "Add Vehicle Service Booking"
    vehicle = Vehicle.objects.get(pk=vehicle_id)

    booking = ServiceBooking()
    booking.vehicle = vehicle
    booking.mileage = vehicle.get_current_mileage()
    if vehicle.get_current_driver() != "Not Allocated":
        booking.driver = vehicle.get_current_driver()

    form = ServiceBookingForm(request.POST or None, instance=booking)
    comment_form = CommentsForm(request.POST or None)

    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUpload.objects.filter(vehicle=vehicle).filter(transaction="ServiceBooking")

    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = Comment.objects.filter(vehicle = vehicle).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
        "title": title,
        "form": form,
        "comment_form": comment_form,
        "vehicle": vehicle,
        "upload_file_form": upload_file_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,

    }

    post = request.POST
    if request.POST:
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by=request.user
                save_form.save()

                latest_trans = ServiceBooking.objects.order_by('-id')[0]

                subject = [latest_trans.vehicle, ' service booking']

                from_email = settings.EMAIL_HOST_USER
                to_email = ['elfleet@emeraldlife.co.za']
                # to_email = ['theresaa@emeraldlife.co.za']
                booking_message = "Vehicle: %s %s %s on %s at %s"%(
                    latest_trans.vehicle,
                    latest_trans.driver,
                    latest_trans.service_description,
                    latest_trans.service_date,
                    latest_trans.garage
                    )
                CRLF = "\r\n"

                if settings.SEND_COMMS:
                    login = settings.EMAIL_HOST_USER
                    password = settings.EMAIL_HOST_PASSWORD
                    attendees = to_email
                    organizer = "lewisk@emeraldlife.co.za"
                    fro = "Fleet_Services<"+from_email+">"
                    ddtstart = latest_trans.service_date
                    dtstamp = datetime.now().strftime("%Y%m%dT%H%M%SZ")
                    dtstart = latest_trans.service_date.strftime("%Y%m%dT%H%M%SZ")
                    dtend = latest_trans.service_date.strftime("%Y%m%dT%H%M%SZ")
                    location = latest_trans.garage

                    description = "DESCRIPTION: Vehicle service booking "+booking_message+CRLF
                    attendee = ""
                    for att in attendees:
                        attendee += "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-    PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE"+CRLF+" ;CN="+att+";X-NUM-GUESTS=0:"+CRLF+" mailto:"+att+CRLF
                    ical = "BEGIN:VCALENDAR"+CRLF+"PRODID:pyICSParser"+CRLF+"VERSION:2.0"+CRLF+"CALSCALE:GREGORIAN"+CRLF
                    ical+="METHOD:REQUEST"+CRLF+"BEGIN:VEVENT"+CRLF+"DTSTART:"+dtstart+CRLF+"DTEND:"+dtend+CRLF+"DTSTAMP:"+dtstamp+CRLF+organizer+CRLF
                    ical+= "UID:FIXMEUID"+dtstamp+CRLF
                    ical+= attendee+"CREATED:"+dtstamp+CRLF+description+"LAST-MODIFIED:"+dtstamp+CRLF+"LOCATION:"+location+CRLF+"SEQUENCE:0"+CRLF+"STATUS:CONFIRMED"+CRLF
                    ical+= "SUMMARY:test "+ddtstart.strftime("%Y%m%d @ %H:%M")+CRLF+"TRANSP:OPAQUE"+CRLF+"END:VEVENT"+CRLF+"END:VCALENDAR"+CRLF

                    eml_body = booking_message
                    eml_body_bin = "This is the email body in binary - two steps"
                    msg = MIMEMultipart('mixed')
                    msg['Reply-To']=fro
                    msg['Date'] = formatdate(localtime=True)
                    msg['Subject'] = "Service Booking for %s: %s"%(latest_trans.driver, latest_trans.vehicle)
                    msg['From'] = fro
                    msg['To'] = ",".join(attendees)

                    part_email = MIMEText(eml_body,"html")
                    part_cal = MIMEText(ical,'calendar;method=REQUEST')

                    msgAlternative = MIMEMultipart('alternative')
                    msg.attach(msgAlternative)

                    ical_atch = MIMEBase('application/ics',' ;name="%s"'%("invite.ics"))
                    ical_atch.set_payload(ical)
                    Encoders.encode_base64(ical_atch)
                    ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"'%("invite.ics"))
                    eml_atch = MIMEBase('text/plain','')
                    Encoders.encode_base64(eml_atch)
                    eml_atch.add_header('Content-Transfer-Encoding', "")

                    msgAlternative.attach(part_email)
                    msgAlternative.attach(part_cal)

                    mailServer = smtplib.SMTP('smtp.office365.com', 587)
                    mailServer.ehlo()
                    mailServer.starttls()
                    mailServer.ehlo()
                    mailServer.login(login, password)
                    mailServer.sendmail(fro, attendees, msg.as_string())
                    mailServer.close()

                    queue_service_booking_sms(vehicle)

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.vehicle = latest_trans.vehicle
                    new_comment.comment_type = "ServiceBooking"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = FileUpload.objects.create(file=f)
                        uploaded.transaction_id = latest_trans.id
                        uploaded.vehicle = latest_trans.vehicle
                        uploaded.file_name = uploaded.file.name
                        uploaded.transaction = "ServiceBooking"
                        uploaded.save()
                return HttpResponseRedirect(reverse('fleet:viewvehicle', kwargs={'vehicle_id':vehicle.id}))
    return render(request, "vehicles.html", context)


@login_required
@permission_required('fleet.edit_servicebooking', raise_exception=True)
def editbookservice(request, trans_id):
    title = "Edit Vehicle Service Booking"
    transaction = ServiceBooking.objects.get(pk=trans_id)
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)
    vehicle = transaction.vehicle
    trans_key = transaction.id
    vehicle_id = Vehicle.objects.filter(licence_plate=vehicle)
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    form = ServiceBookingForm(request.POST or None, instance=transaction)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUpload.objects.filter(vehicle=vehicle).filter(transaction='ServiceBooking').filter(transaction_id=trans_key)

    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = Comment.objects.filter(vehicle = vehicle).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
    "title": title,
    "form": form,
        "comment_form": comment_form,
    "vehicle": vehicle,
    "upload_file_form": upload_file_form,
    "uploads": uploads,
    "sliders": images,
    "comments": comments,

    }

    post = request.POST
    if request.POST:
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by=creator
                save_form.modified_by=request.user
                save_form.save()

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.vehicle = vehicle
                    new_comment.comment_type = "ServiceBooking"
                    new_comment.obj_id = transaction.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = FileUpload.objects.create(file=f)
                        uploaded.transaction_id = transaction.id
                        uploaded.vehicle = vehicle
                        uploaded.file_name = uploaded.file.name
                        uploaded.transaction = "ServiceBooking"
                        uploaded.save()
                return HttpResponseRedirect(reverse('fleet:viewvehicle', kwargs={'vehicle_id':vehicle.id}))
    return render(request, "vehicles.html", context)


@login_required
@permission_required('fleet.view_servicebooking', raise_exception=True)
def viewbookservice(request, trans_id):
    title = "View Vehicle Service Booking"
    transaction = ServiceBooking.objects.get(pk=trans_id)
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)
    vehicle = transaction.vehicle
    trans_key = transaction.id
    vehicle_id = Vehicle.objects.filter(licence_plate=vehicle)
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    form = ServiceBookingForm(request.POST or None, instance=transaction)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUpload.objects.filter(vehicle=vehicle).filter(transaction='ServiceBooking').filter(transaction_id=trans_key)

    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = Comment.objects.filter(vehicle = vehicle).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
    "title": title,
    "form": form,
    "comment_form": comment_form,
    "vehicle": vehicle,
    "upload_file_form": upload_file_form,
    "uploads": uploads,
    "sliders": images,
    "comments": comments,
    "view_transaction":True,

    }
    return render(request, "vehicles.html", context)


@login_required
@permission_required('fleet.view_servicebooking', raise_exception=True)
def servicebookingsList(request):
    fleet =  Vehicle.objects.all()
    bookings = ServiceBooking.objects.all()
    if request.user.regional_staff:
        fleet =  Vehicle.objects.filter(current_driver__branch__region=request.user.employee.branch.region)
        bookings = ServiceBooking.objects.filter(driver__branch__region=request.user.employee.branch.region)

    title = "Service Bookings"
    service_list = bookings.order_by('-id')
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_bookings' in request.GET and filter_form.is_valid():
        date = 'service_date'
        service_list = filter_form.filter(service_list, date)

    page = request.GET.get('page', 1)
    service_list_paginator = Paginator(service_list, 14)
    try:
        service_list = service_list_paginator.page(page)
    except PageNotAnInteger:
        service_list = service_list_paginator.page(1)
    except EmptyPage:
        service_list = service_list_paginator.page(service_list_paginator.num_pages)

    vehicles =fleet.filter(Q(ownership_type="EL Fleet") | Q(ownership_type="EL Leased"), active=True)

    service_due = []
    for v in vehicles:
        if v.get_next_service_mileage() - v.get_current_mileage() < 1400 and v.get_next_service_mileage() > v.get_current_mileage():
            service_due.append(v)

    if u'filter_due' in request.GET and filter_form.is_valid():
        date = 'purchase_date'
        service_due = filter_form.filter(service_due, date)
    service_due_paginator = Paginator(service_due, 14)
    try:
        service_due = service_due_paginator.page(page)
    except PageNotAnInteger:
        service_due = service_due_paginator.page(1)
    except EmptyPage:
        service_due = service_due_paginator.page(service_due_paginator.num_pages)

    service_over_due =[]
    for vkl in vehicles:
        if vkl.get_next_service_mileage() < vkl.get_current_mileage():
            service_over_due.append(vkl)

    if u'filter_overdue' in request.GET and filter_form.is_valid():
        date = 'purchase_date'  #to search from vehicle Details
        service_over_due = filter_form.filter(service_over_due, date)
    service_over_due_paginator = Paginator(service_over_due, 14)
    try:
        service_over_due = service_over_due_paginator.page(page)
    except PageNotAnInteger:
        service_over_due = service_over_due_paginator.page(1)
    except EmptyPage:
        service_over_due = service_over_due_paginator.page(service_over_due_paginator.num_pages)

    context ={
        "title": title,
        "service_list": service_list,
        "vehicles_due_service":service_due,
        "vehicles_over_due_service":service_over_due,
        "filter_form": filter_form,
        }
    return render(request, "servicebookingsList.html", context)

@login_required
@permission_required('fleet.create_trafficfine', raise_exception=True)
def trafficfines(request, vehicle_id):
    title = "Add Vehicle Traffic Fine"
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    fine = Trafficfine()
    fine.vehicle = vehicle
    if vehicle.get_current_driver() != "Not Allocated":
        fine.driver = vehicle.get_current_driver()
    form = TrafficfineForm(request.POST or None, instance=fine, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUpload.objects.filter(vehicle=vehicle).filter(transaction="Trafficfine")
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id','-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = Comment.objects.filter(vehicle = vehicle).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
        "title": title,
        "form": form,
        "comment_form": comment_form,
        "vehicle": vehicle,
        "upload_file_form": upload_file_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,

    }

    post = request.POST
    if request.POST:
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by=request.user
                save_form.save()
                latest_trans = Trafficfine.objects.order_by('-id')[0]

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.vehicle = latest_trans.vehicle
                    new_comment.comment_type = "Trafficfine"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = FileUpload.objects.create(file=f)
                        uploaded.transaction_id = latest_trans.id
                        uploaded.vehicle = latest_trans.vehicle
                        uploaded.file_name = uploaded.file.name
                        uploaded.transaction = "Trafficfine"
                        uploaded.save()

                return HttpResponseRedirect(reverse('fleet:requisition_vehicletrafficfine', kwargs={'obj_id':latest_trans.id}))
    return render(request, "vehicles.html", context)


@login_required
@permission_required('fleet.edit_trafficfine', raise_exception=True)
def edittrafficfines(request, trans_id):
    title = "Edit Vehicle Traffic Fine"
    transaction = Trafficfine.objects.get(pk=trans_id)
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)
    vehicle = transaction.vehicle
    trans_key = transaction.id
    vehicle_id = Vehicle.objects.filter(licence_plate=vehicle)
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    try:
        requisition = Requisition.objects.get(obj_id=trans_id, requisition_type="Trafficfines")
    except Requisition.DoesNotExist:
        requisition = None


    form = TrafficfineForm(request.POST or None, instance=transaction, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUpload.objects.filter(vehicle=vehicle).filter(transaction="Trafficfine").filter(transaction_id=trans_key)

    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = Comment.objects.filter(vehicle = vehicle).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
        "title": title,
        "form": form,
        "comment_form": comment_form,
        "vehicle": vehicle,
        "upload_file_form": upload_file_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,

    }

    post = request.POST
    if request.POST:
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by = creator
                save_form.modified_by=request.user
                save_form.save()

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.vehicle = vehicle
                    new_comment.comment_type = "Trafficfine"
                    new_comment.obj_id = transaction.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = FileUpload.objects.create(file=f)
                        uploaded.transaction_id = transaction.id
                        uploaded.vehicle = vehicle
                        uploaded.file_name = uploaded.file.name
                        uploaded.transaction = "Trafficfine"
                        uploaded.save()

                if request.user.has_perm('authorize_trafficfines'):
                    if requisition:
                        return HttpResponseRedirect(reverse('fleet:view_requisition', kwargs={'obj_id':requisition.id}))
                    else:
                        return HttpResponseRedirect(reverse('fleet:authorizations'))
                else:
                    return HttpResponseRedirect(reverse('fleet:viewvehicle', kwargs={'vehicle_id':vehicle.id}))
    return render(request, "vehicles.html", context)


@login_required
@permission_required('fleet.view_trafficfine', raise_exception=True)
def viewtrafficfines(request, trans_id):
    title = "View Vehicle Traffic Fine"
    transaction = Trafficfine.objects.get(pk=trans_id)
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)
    vehicle = transaction.vehicle
    trans_key = transaction.id
    vehicle_id = Vehicle.objects.filter(licence_plate=vehicle)
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    try:
        requisition = Requisition.objects.get(obj_id=trans_id, requisition_type="Trafficfines")
    except Requisition.DoesNotExist:
        requisition = None


    form = TrafficfineForm(request.POST or None, instance=transaction, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUpload.objects.filter(vehicle=vehicle).filter(transaction="Trafficfine").filter(transaction_id=trans_key)

    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = Comment.objects.filter(vehicle = vehicle).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
        "title": title,
        "form": form,
        "comment_form": comment_form,
        "vehicle": vehicle,
        "upload_file_form": upload_file_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,
        "view_transaction":True,

    }
    return render(request, "vehicles.html", context)


@login_required
@permission_required('fleet.view_trafficfine', raise_exception=True)
def trafficfinesList(request):
    fleet =  Vehicle.objects.all()
    fines = Trafficfine.objects.all()
    if request.user.regional_staff:
        fleet =  Vehicle.objects.filter(current_driver__branch__region=request.user.employee.branch.region)
        fines = Trafficfine.objects.filter(driver__branch__region=request.user.employee.branch.region)

    title = "Traffic Fines List"
    traffic_fines = fines.order_by('-offence_date')
    date = 'tf_due_date'
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_tf' in request.GET and filter_form.is_valid():
        traffic_fines = filter_form.filter(traffic_fines, date)
    page = request.GET.get('page', 1)
    traffic_fines_paginator = Paginator(traffic_fines, 14)
    try:
        traffic_fines = traffic_fines_paginator.page(page)
    except PageNotAnInteger:
        traffic_fines = traffic_fines_paginator.page(1)
    except EmptyPage:
        traffic_fines = traffic_fines_paginator.page(traffic_fines_paginator.num_pages)

    pending_fines = fines.filter(paid=False)
    date = 'tf_due_date'
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_ptf' in request.GET and filter_form.is_valid():
        pending_fines = filter_form.filter(pending_fines, date)
    page = request.GET.get('page', 1)
    pending_fines_paginator = Paginator(pending_fines, 14)
    try:
        pending_fines = pending_fines_paginator.page(page)
    except PageNotAnInteger:
        pending_fines = pending_fines_paginator.page(1)
    except EmptyPage:
        pending_fines = pending_fines_paginator.page(pending_fines_paginator.num_pages)

    vehicles = fleet.filter(active=True).order_by('licence_plate')
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_stats' in request.GET and filter_form.is_valid():
        date = 'purchase_date'
        vehicles = filter_form.filter(vehicles, date)
    page = request.GET.get('page', 1)
    vehicles_paginator = Paginator(vehicles, 14)
    try:
        vehicles = vehicles_paginator.page(page)
    except PageNotAnInteger:
        vehicles = vehicles_paginator.page(1)
    except EmptyPage:
        vehicles = vehicles_paginator.page(vehicles_paginator.num_pages)

    context ={
        "title": title,
        "traffic_fines": traffic_fines,
        "pending_fines": pending_fines,
        "filter_form": filter_form,
        "vehicles": vehicles,
        }
    return render(request, "trafficFinesList.html", context)



@login_required
@permission_required('fleet.create_mileagelog', raise_exception=True)
def mileagelog(request, vehicle_id):
    title = "Add Vehicle Inspection"
    vehicle = Vehicle.objects.get(pk=vehicle_id)

    mileage_log = MileageLog()
    mileage_log.vehicle = vehicle
    mileage_log.starting_mileage = vehicle.get_current_mileage()
    mileage_log.fuel_balance_bf = vehicle.fuel_balance
    if vehicle.get_current_driver() != "Not Allocated":
        mileage_log.driver = vehicle.get_current_driver()

    form = MileageLogForm(request.POST or None, instance=mileage_log)
    comment_form = CommentsForm(request.POST or None)

    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUpload.objects.filter(vehicle=vehicle).filter(transaction='MileageLog')

    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = Comment.objects.filter(vehicle = vehicle).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
        "title": title,
        "form": form,
        "comment_form": comment_form,
        "vehicle": vehicle,
        "upload_file_form": upload_file_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,

    }

    post = request.POST
    if request.POST:
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by=request.user
                save_form.save()

                latest_trans = MileageLog.objects.order_by('-id')[0]
                vehicle.fuel_balance = latest_trans.fuel_balance
                vehicle.status = latest_trans.status
                vehicle.last_inspected = latest_trans.log_date
                vehicle.inspected = True
                if latest_trans.status == "Write Off":
                    vehicle.active = False
                vehicle.save()

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.vehicle = latest_trans.vehicle
                    new_comment.comment_type = "MileageLog"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = FileUpload.objects.create(file=f)
                        uploaded.transaction_id = latest_trans.id
                        uploaded.vehicle = latest_trans.vehicle
                        uploaded.file_name = uploaded.file.name
                        uploaded.transaction = "MileageLog"
                        uploaded.save()
                return HttpResponseRedirect(reverse('fleet:viewvehicle', kwargs={'vehicle_id':vehicle.id}))
    return render(request, "vehicles.html", context)




@login_required
@permission_required('fleet.edit_mileagelog', raise_exception=True)
def editmileagelog(request, trans_id):
    title = "Edit Vehicle Inspection"
    transaction = MileageLog.objects.get(pk=trans_id)
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)
    vehicle = transaction.vehicle
    trans_key = transaction.id
    vehicle_id = Vehicle.objects.filter(licence_plate=vehicle)
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    form = MileageLogForm(request.POST or None, instance=transaction)
    comment_form = CommentsForm(request.POST or None)

    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUpload.objects.filter(vehicle=vehicle).filter(transaction='MileageLog').filter(transaction_id=trans_key)
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = Comment.objects.filter(vehicle = vehicle).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
        "title": title,
        "form": form,
        "comment_form": comment_form,
        "vehicle": vehicle,
        "upload_file_form": upload_file_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,

    }

    post = request.POST
    if request.POST:
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by=creator
                save_form.modified_by=request.user
                save_form.save()

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.vehicle = vehicle
                    new_comment.comment_type = "MileageLog"
                    new_comment.obj_id = transaction.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = FileUpload.objects.create(file=f)
                        uploaded.transaction_id = transaction.id
                        uploaded.vehicle = vehicle
                        uploaded.file_name = uploaded.file.name
                        uploaded.transaction = "MileageLog"
                        uploaded.save()
                return HttpResponseRedirect(reverse('fleet:viewvehicle', kwargs={'vehicle_id':vehicle.id}))
    return render(request, "vehicles.html", context)


@login_required
@permission_required('fleet.view_mileagelog', raise_exception=True)
def viewmileagelog(request, trans_id):
    title = "View Vehicle Inspection"
    transaction = MileageLog.objects.get(pk=trans_id)
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)
    vehicle = transaction.vehicle
    trans_key = transaction.id
    vehicle_id = Vehicle.objects.filter(licence_plate=vehicle)
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    form = MileageLogForm(request.POST or None, instance=transaction)
    comment_form = CommentsForm(request.POST or None)

    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUpload.objects.filter(vehicle=vehicle).filter(transaction='MileageLog').filter(transaction_id=trans_key)
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = Comment.objects.filter(vehicle = vehicle).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
        "title": title,
        "form": form,
        "comment_form": comment_form,
        "vehicle": vehicle,
        "upload_file_form": upload_file_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,
        "view_transaction":True,

    }
    return render(request, "vehicles.html", context)


@login_required
@permission_required('fleet.view_mileagelog', raise_exception=True)
def mileagelogList(request):
    fleet =  Vehicle.objects.all()
    inspections = MileageLog.objects.all()
    if request.user.regional_staff:
        fleet =  Vehicle.objects.filter(current_driver__branch__region=request.user.employee.branch.region)
        inspections = MileageLog.objects.filter(driver__branch__region=request.user.employee.branch.region)

    title = "Vehicle Inspections"
    mileage_log = inspections.order_by('-id')
    date = 'log_date'
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_mileagelog' in request.GET and filter_form.is_valid():
        mileage_log = filter_form.filter(mileage_log, date)
    page = request.GET.get('page', 1)
    mileage_log_paginator = Paginator(mileage_log, 16)
    try:
        mileage_log = mileage_log_paginator.page(page)
    except PageNotAnInteger:
        mileage_log = mileage_log_paginator.page(1)
    except EmptyPage:
        mileage_log = mileage_log_paginator.page(mileage_log_paginator.num_pages)

    vehicles = fleet.filter(active=True).order_by('licence_plate')
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_stats' in request.GET and filter_form.is_valid():
        date = 'purchase_date'
        vehicles = filter_form.filter(vehicles, date)
    page = request.GET.get('page', 1)
    vehicles_paginator = Paginator(vehicles, 16)
    try:
        vehicles = vehicles_paginator.page(page)
    except PageNotAnInteger:
        vehicles = vehicles_paginator.page(1)
    except EmptyPage:
        vehicles = vehicles_paginator.page(vehicles_paginator.num_pages)
    last_month = datetime.now().replace(day=1)- timedelta(days=1)

    context ={
        "title": title,
        "mileage_log": mileage_log,
        "filter_form": filter_form,
        'vehicles': vehicles,
        'month': datetime.now().strftime('%B'),
        'last_month':last_month.strftime('%B'),

        }
    return render(request, "mileagelogList.html", context)




@login_required
@permission_required('fleet.create_vehiclemaintenance', raise_exception=True)
def vehiclemaintenance(request, vehicle_id):
    title = "Add Vehicle Maintenance"

    vehicle = Vehicle.objects.get(pk=vehicle_id)
    maintenance = VehicleMaintenance()
    maintenance.vehicle = vehicle
    maintenance.current_mileage = vehicle.get_current_mileage()
    if vehicle.get_current_driver() != "Not Allocated":
        maintenance.driver = vehicle.get_current_driver()

    form = MaintenanceForm(request.POST or None, instance=maintenance, user=request.user)
    comment_form = CommentsForm(request.POST or None)

    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUpload.objects.filter(vehicle=vehicle).filter(transaction='VehicleMaintenance')
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = Comment.objects.filter(vehicle = vehicle).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
        "title": title,
        "form": form,
        "comment_form": comment_form,
        "vehicle": vehicle,
        "upload_file_form": upload_file_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,

    }

    post = request.POST
    if request.POST:
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by=request.user
                save_form.save()
                vehicle.status = maintenance.status
                if maintenance.status == "Write Off":
                    vehicle.active = 0
                vehicle.save()
                latest_trans = VehicleMaintenance.objects.order_by('-id')[0]

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.vehicle = latest_trans.vehicle
                    new_comment.comment_type = "VehicleMaintenance"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = FileUpload.objects.create(file=f)
                        uploaded.transaction_id = latest_trans.id
                        uploaded.vehicle = latest_trans.vehicle
                        uploaded.file_name = uploaded.file.name
                        uploaded.transaction = "VehicleMaintenance"
                        uploaded.save()

                return HttpResponseRedirect(reverse('fleet:requisition_vehiclemaintenance', kwargs={'obj_id': latest_trans.id}))
    return render(request, "vehicles.html", context)


@login_required
@permission_required('fleet.edit_vehiclemaintenance', raise_exception=True)
def editvehiclemaintenance(request, trans_id):

    title = "Edit Vehicle Maintenance"
    transaction = VehicleMaintenance.objects.get(pk=trans_id)
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)
    vehicle = transaction.vehicle
    trans_key = transaction.id
    vehicle_id = Vehicle.objects.filter(licence_plate=vehicle)
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    try:
        requisition = Requisition.objects.get(obj_id=trans_id, requisition_type="VehicleMaintenance")
    except Requisition.DoesNotExist:
        requisition = None

    form = MaintenanceForm(request.POST or None, instance=transaction, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUpload.objects.filter(vehicle=vehicle).filter(transaction='VehicleMaintenance').filter(transaction_id=trans_key)
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = Comment.objects.filter(vehicle=vehicle)
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context={
        "title": title,
        "form": form,
        "comment_form": comment_form,
        "vehicle": vehicle,
        "upload_file_form": upload_file_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,
    }

    post = request.POST
    if request.POST:
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by=creator
                save_form.modified_by=request.user
                save_form.save()

                if request.user.has_perm('authorize_vehiclemaintenance'):
                    booking_id = save_form.service_booking_number
                    if save_form.authorize=="Aproved" and booking_id:
                        service_booking = ServiceBooking.objects.get(pk=booking_id.id)
                        service_booking.serviced = True
                        service_booking.save()

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.vehicle = vehicle
                    new_comment.comment_type = "VehicleMaintenance"
                    new_comment.obj_id = transaction.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = FileUpload.objects.create(file=f)
                        uploaded.transaction_id = transaction.id
                        uploaded.vehicle = vehicle
                        uploaded.file_name = uploaded.file.name
                        uploaded.transaction = "VehicleMaintenance"
                        uploaded.save()

                if request.user.has_perm('authorize_vehiclemaintenance'):
                    if requisition:
                        return HttpResponseRedirect(reverse('fleet:view_requisition', kwargs={'obj_id':requisition.id}))
                    else:
                        return HttpResponseRedirect(reverse('fleet:authorizations'))
                else:
                    return HttpResponseRedirect(reverse('fleet:viewvehicle', kwargs={'vehicle_id':vehicle.id}))

    return render(request, "vehicles.html", context)


@login_required
@permission_required('fleet.view_vehiclemaintenance', raise_exception=True)
def viewvehiclemaintenance(request, trans_id):
    title = "View Vehicle Maintenance"
    transaction = VehicleMaintenance.objects.get(pk=trans_id)
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)
    vehicle = transaction.vehicle
    trans_key = transaction.id
    vehicle_id = Vehicle.objects.filter(licence_plate=vehicle)
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    try:
        requisition = Requisition.objects.get(obj_id=trans_id, requisition_type="VehicleMaintenance")
    except Requisition.DoesNotExist:
        requisition = None

    form = MaintenanceForm(request.POST or None, instance=transaction, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUpload.objects.filter(vehicle=vehicle).filter(transaction='VehicleMaintenance').filter(transaction_id=trans_key)
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = Comment.objects.filter(vehicle=vehicle)
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context={
        "title": title,
        "form": form,
        "comment_form": comment_form,
        "vehicle": vehicle,
        "upload_file_form": upload_file_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,
        "view_transaction":True,
    }
    return render(request, "vehicles.html", context)


@login_required
@permission_required('fleet.view_vehiclemaintenance', raise_exception=True)
def vehiclemaintenanceList(request):
    fleet =  Vehicle.objects.all()
    vehicle_maintenance = VehicleMaintenance.objects.all()
    if request.user.regional_staff:
        fleet =  Vehicle.objects.filter(current_driver__branch__region=request.user.employee.branch.region)
        vehicle_maintenance = VehicleMaintenance.objects.filter(driver__branch__region=request.user.employee.branch.region)

    title = "Vehicle Maintenance List"
    maintenance_list = vehicle_maintenance.order_by('-maint_date')
    date = 'maint_date'
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_maintenance' in request.GET and filter_form.is_valid():
        maintenance_list = filter_form.filter(maintenance_list, date)
    page = request.GET.get('page', 1)
    maintenance_list_paginator = Paginator(maintenance_list, 14)
    try:
        maintenance_list = maintenance_list_paginator.page(page)
    except PageNotAnInteger:
        maintenance_list = maintenance_list_paginator.page(1)
    except EmptyPage:
        maintenance_list = maintenance_list_paginator.page(maintenance_list_paginator.num_pages)

    vehicles = fleet.order_by('licence_plate')
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_stats' in request.GET and filter_form.is_valid():
        date = 'purchase_date'
        vehicles = filter_form.filter(vehicles, date)
    page = request.GET.get('page', 1)
    vehicles_paginator = Paginator(vehicles, 14)
    try:
        vehicles = vehicles_paginator.page(page)
    except PageNotAnInteger:
        vehicles = vehicles_paginator.page(1)
    except EmptyPage:
        vehicles = vehicles_paginator.page(vehicles_paginator.num_pages)

    minor_damages = fleet.filter(status="Minor Damages", active=True)
    if u'filter_minor' in request.GET and filter_form.is_valid():
        date="purchase_date"
        minor_damages = filter_form.filter(minor_damages, date)
    minor_damages_paginator = Paginator(minor_damages, 14)
    try:
        minor_damages = minor_damages_paginator.page(page)
    except PageNotAnInteger:
        minor_damages = minor_damages_paginator.page(1)
    except EmptyPage:
        minor_damages = minor_damages_paginator.page(minor_damages_paginator.num_pages)

    major_damages = fleet.filter(status="Major Damages", active=True)
    if u'filter_major' in request.GET and filter_form.is_valid():
        date="purchase_date"
        major_damages = filter_form.filter(major_damages, date)
    major_damages_paginator = Paginator(major_damages, 14)
    try:
        major_damages = major_damages_paginator.page(page)
    except PageNotAnInteger:
        major_damages = major_damages_paginator.page(1)
    except EmptyPage:
        major_damages = major_damages_paginator.page(major_damages_paginator.num_pages)
    context ={
        "title": title,
        "maintenance_list": maintenance_list,
        "minor_damages": minor_damages,
        "major_damages": major_damages,
        "filter_form": filter_form,
        "vehicles": vehicles,
        }
    return render(request, "vehiclemaintenanceList.html", context)



@login_required
# @permission_required('fleet.create_vehiclemaintenance', raise_exception=True)
def requisition(request, obj_id, obj_type=None):
    title = "Process Requisition"
    obj = obj_type.objects.get(pk=obj_id)

    Type = obj_type
    if "VehicleMaintenance" in str(Type):
        o_type = "VehicleMaintenance"
    if "Trafficfine" in str(Type):
        o_type = "Trafficfine"
    if "InsuranceClaim" in str(Type):
        o_type = "InsuranceClaim"
    if "RenewLicenceDisk" in str(Type):
        o_type = "RenewLicenceDisk"
    if "VehicleAllocation" in str(Type):
        o_type = "VehicleAllocation"
    if "FuelAllocation" in str(Type):
        o_type = "FuelAllocation"
    if "FuelTransfer" in str(Type):
        o_type = "FuelTransfer"


    vehicle = Vehicle.objects.get(pk=obj.vehicle_id)
    req = Requisition()
    req.obj_id = obj.id
    req.vehicle = obj.vehicle
    req.driver = obj.driver
    req.requisition_type = o_type
    form = RequisitionForm(request.POST or None, instance=req)

    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUpload.objects.filter(vehicle=obj.vehicle).filter(transaction=o_type)
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=obj.vehicle).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]
    comment_form = CommentsForm(request.POST or None)
    comments = Comment.objects.filter(vehicle = obj.vehicle)
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
        "title": title,
        "form": form,
        "comment_form": comment_form,
        "vehicle": vehicle,
        "upload_file_form": upload_file_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,

    }

    post = request.POST
    if request.POST:
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.obj_id = obj.id
                save_form.created_by = request.user
                save_form.save()

                latest_trans = Requisition.objects.order_by('-id')[0]

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.vehicle = obj.vehicle
                    new_comment.comment_type = o_type
                    new_comment.obj_id = obj.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = FileUpload.objects.create(file=f)
                        uploaded.transaction_id = obj.id
                        uploaded.vehicle = obj.vehicle
                        uploaded.file_name = uploaded.file.name
                        uploaded.transaction = o_type
                        uploaded.save()
                return HttpResponseRedirect(reverse('fleet:view_requisition', kwargs={'obj_id':latest_trans.id}))
    return render(request, "vehicles.html", context)


@login_required
# @permission_required('fleet.create_vehiclemaintenance', raise_exception=True)
def requisition_item(request, obj_id):
    title = "Process Requisition Items"

    obj = Requisition.objects.get(pk=obj_id)
    req = RequisitionItem()
    req.requisition_no = obj
    vehicle = Vehicle.objects.get(pk=obj.vehicle_id)
    form = RequisitionItemForm(request.POST or None, instance=req)
    comment_form = CommentsForm(request.POST or None)

    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUpload.objects.filter(vehicle=obj.vehicle).filter(transaction='Requisition')
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=obj.vehicle).values_list('file', flat=True).order_by('-date_uploaded')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    requisition_items = RequisitionItem.objects.filter(requisition_no=obj_id)

    comments = Comment.objects.filter(vehicle = obj.vehicle)
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
        "title": title,
        "form": form,
        "comment_form": comment_form,
        "vehicle": vehicle,
        "upload_file_form": upload_file_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,
        "requisition_items": requisition_items,
        "requisition": obj,

    }

    post = request.POST
    if request.POST:
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by=request.user
                save_form.obj_id = obj.id
                save_form.save()
                return HttpResponseRedirect(reverse('fleet:requisition_item', kwargs={'obj_id':obj.id}))

        if u'addClose' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.obj_id = obj.id
                save_form.save()

                return HttpResponseRedirect(reverse('fleet:view_requisition', kwargs={'obj_id':obj.id}))
    return render(request, "vehicles.html", context)

@login_required
# @permission_required('fleet.create_vehiclemaintenance', raise_exception=True)
def view_requisition(request, obj_id):
    title = "Requistion"
    try:
        obj = Requisition.objects.get(pk=obj_id)
        employee = Employee.objects.get(pk=obj.requested_by_id)
        branch_id = employee.branch.id
        branch = Branch.objects.get(pk=branch_id)
        region = Region.objects.get(pk=branch.region_id)

        subject = 'Requisition for %s vehicle %s '%(obj.driver, obj.vehicle)
        body = '%s for %s  vehicle %s'%(obj.description, obj.driver, obj.vehicle)
    except Requisition.DoesNotExist:
        obj = None
        employee = None
        branch = None
        region = None
        subject = ''
        body = ''

    context ={
        'title': title,
        'requisition': obj,
        'branch': branch,
        'employee': employee,
        'region': region,
        'budgeted':obj.budgeted,
        'http_origin': "http://%s" % request.get_host(),  # settings.BASE_URL
        }

    if u'send' in request.POST:
        send_pdf("requisition.html", context,  ['callien@emeraldlife.co.za', 'lewisk@emeraldlife.co.za'], body, subject, 'Requisition.pdf')

        return HttpResponseRedirect(reverse('fleet:authorizations'))

    if u'close' in request.POST:
        if request.user.has_perm('authorize_vehiclemaintenance'):
            return HttpResponseRedirect(reverse('fleet:authorizations'))
        else:
            return HttpResponseRedirect(reverse('fleet:viewvehicle', kwargs={'vehicle_id':obj.vehicle.id}))

    if u'download' in request.POST:
        return download_pdf("req.html", context, 'Requisition.pdf')
    print context

    return render(request, "view_requisition.html", context)


def send_pdf(template_src, context_dict, to_email_address, email_body, email_subject, filename=None ):

    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO.StringIO()

    # links = lambda uri, rel: os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ''))


    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), dest=result)

    email = EmailMessage(email_subject, email_body, settings.EMAIL_HOST_USER, to_email_address)
    email.attach(filename, result.getvalue(), 'application/pdf')
    email.send()

    result.close()

def get_full_path_x(request):
    full_path = ('http', ('', 's')[request.is_secure()], '://',
    request.META['HTTP_HOST'], request.path)
    return ''.join(full_path)

def fetch_resources(uri, rel):

    path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))

    return path


def download_pdf(template_src, context_dict, filename=None):
    DEBUG = False

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename="%s"' % filename
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO.StringIO()

    # links = lambda uri, rel: os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, '/img/'))

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), dest=result)

    response.write(result.getvalue())
    result.close()

    if not pdf.err:
        if DEBUG is True:
            return http.HttpResponse(html)
        else:

            return response
    return http.HttpResponse('Error while creating the pdf! %s' % cgi.escae(html))



@login_required
@permission_required('fleet.create_renewlicencedisk', raise_exception=True)
def renewlicencedisk(request, vehicle_id):
    title = "Vehicle Licence Disk Renewal"

    vehicle = Vehicle.objects.get(pk=vehicle_id)

    disk_renewal = RenewLicenceDisk()
    disk_renewal.vehicle = vehicle
    disk_renewal.expiry_date = vehicle.licence_disk_expiry
    if vehicle.get_current_driver() != "Not Allocated":
        disk_renewal.driver = vehicle.get_current_driver()

    form = RenewLicenceDiskForm(request.POST or None, instance=disk_renewal, user=request.user)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUpload.objects.filter(vehicle=vehicle).filter(transaction="RenewLicenceDisk")

    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = Comment.objects.filter(vehicle = vehicle).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
        "title": title,
        "form": form,
        "comment_form": comment_form,
        "vehicle": vehicle,
        "upload_file_form": upload_file_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,
    }

    post = request.POST
    if request.POST:
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by=request.user
                save_form.save()
                vehicle.licence_disk_expiry = disk_renewal.new_expiry_date
                vehicle.save()
                latest_trans = RenewLicenceDisk.objects.order_by('-id')[0]

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.vehicle = latest_trans.vehicle
                    new_comment.comment_type = "RenewLicenceDisk"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = FileUpload.objects.create(file=f)
                        uploaded.transaction_id = latest_trans.id
                        uploaded.vehicle = latest_trans.vehicle
                        uploaded.file_name = uploaded.file.name
                        uploaded.transaction = "RenewLicenceDisk"
                        uploaded.save()

                return HttpResponseRedirect(reverse('fleet:requisition_vehiclelicencing', kwargs={'obj_id':latest_trans.id}))
    return render(request, "vehicles.html", context)



@login_required
@permission_required('fleet.edit_renewlicencedisk', raise_exception=True)
def editrenewlicencedisk(request, trans_id):
    title = "Edit Licence Disk Renewal"
    transaction = RenewLicenceDisk.objects.get(pk=trans_id)
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)
    vehicle = transaction.vehicle
    trans_key = transaction.id
    vehicle_id = Vehicle.objects.filter(licence_plate=vehicle)
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    try:
        requisition = Requisition.objects.get(obj_id=trans_id, requisition_type="RenewLicenceDisk")
    except Requisition.DoesNotExist:
        requisition = None

    form = RenewLicenceDiskForm(request.POST or None, instance=transaction, user=request.user)
    comment_form = CommentsForm(request.POST or None)

    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUpload.objects.filter(vehicle=vehicle).filter(transaction="RenewLicenceDisk").filter(transaction_id=trans_key)
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = Comment.objects.filter(vehicle = vehicle).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
        "title": title,
        "form": form,
        "comment_form": comment_form,
        "vehicle": vehicle,
        "upload_file_form": upload_file_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments

    }

    post = request.POST
    if request.POST:
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by=creator
                save_form.modified_by=request.user
                save_form.save()

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.vehicle = vehicle
                    new_comment.comment_type = "RenewLicenceDisk"
                    new_comment.obj_id = transaction.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = FileUpload.objects.create(file=f)
                        uploaded.transaction_id = transaction.id
                        uploaded.vehicle = vehicle
                        uploaded.file_name = uploaded.file.name
                        uploaded.transaction = "RenewLicenceDisk"
                        uploaded.save()

                if request.user.has_perm('authorize_renewlicencedisk'):
                    if requisition:
                        return HttpResponseRedirect(reverse('fleet:view_requisition', kwargs={'obj_id':requisition.id}))
                    else:
                        return HttpResponseRedirect(reverse('fleet:authorizations'))
                else:
                    return HttpResponseRedirect(reverse('fleet:viewvehicle', kwargs={'vehicle_id':vehicle.id}))

    return render(request, "vehicles.html", context)


@login_required
@permission_required('fleet.view_renewlicencedisk', raise_exception=True)
def viewrenewlicencedisk(request, trans_id):
    title = "View Licence Disk Renewal"
    transaction = RenewLicenceDisk.objects.get(pk=trans_id)
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)
    vehicle = transaction.vehicle
    trans_key = transaction.id
    vehicle_id = Vehicle.objects.filter(licence_plate=vehicle)
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    try:
        requisition = Requisition.objects.get(obj_id=trans_id, requisition_type="RenewLicenceDisk")
    except Requisition.DoesNotExist:
        requisition = None

    form = RenewLicenceDiskForm(request.POST or None, instance=transaction, user=request.user)
    comment_form = CommentsForm(request.POST or None)

    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUpload.objects.filter(vehicle=vehicle).filter(transaction="RenewLicenceDisk").filter(transaction_id=trans_key)
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = Comment.objects.filter(vehicle = vehicle).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
        "title": title,
        "form": form,
        "comment_form": comment_form,
        "vehicle": vehicle,
        "upload_file_form": upload_file_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,
        "view_transaction":True,

    }
    return render(request, "vehicles.html", context)


@login_required
@permission_required('fleet.view_renewlicencedisk', raise_exception=True)
def licenceDiskRenewalList(request):
    fleet =  Vehicle.objects.all()
    renewals = RenewLicenceDisk.objects.all()
    if request.user.regional_staff:
        fleet =  Vehicle.objects.filter(current_driver__branch__region=request.user.employee.branch.region)
        renewals = RenewLicenceDisk.objects.filter(driver__branch__region=request.user.employee.branch.region)

    title = "Licence Disk Renewals List"
    licence_disk_list = renewals.order_by('-id')
    date = 'renewal_date'
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_list' in request.GET and filter_form.is_valid():
        licence_disk_list = filter_form.filter(licence_disk_list, date)
    page = request.GET.get('page', 1)
    licence_disk_list_paginator = Paginator(licence_disk_list, 14)
    try:
        licence_disk_list = licence_disk_list_paginator.page(page)
    except PageNotAnInteger:
        licence_disk_list = licence_disk_list_paginator.page(1)
    except EmptyPage:
        licence_disk_list = licence_disk_list_paginator.page(licence_disk_list_paginator.num_pages)

    due_expiry_date = datetime.now() + timedelta(+30)
    expired_date = datetime.now() + timedelta(-1)
    todays_date = datetime.now()+ timedelta()

    vehicles_due = fleet.filter(licence_disk_expiry__range=[todays_date, due_expiry_date], ownership_type='EL Fleet', active=1)
    if u'filter_due' in request.GET and filter_form.is_valid():
        date = 'licence_disk_expiry'
        vehicles_due = filter_form.filter(vehicles_due, date)
    vehicles_due_paginator = Paginator(vehicles_due, 14)
    try:
        vehicles_due = vehicles_due_paginator.page(page)
    except PageNotAnInteger:
        vehicles_due = vehicles_due_paginator.page(1)
    except EmptyPage:
        vehicles_due = vehicles_due_paginator.page(vehicles_due_paginator.num_pages)

    vehicles_expired = fleet.filter(licence_disk_expiry__lte=expired_date, ownership_type='EL Fleet', active=1)
    if u'filter_expired' in request.GET and filter_form.is_valid():
        date = 'licence_disk_expiry'
        vehicles_expired = filter_form.filter(vehicles_expired, date)
    vehicles_expired_paginator = Paginator(vehicles_expired, 14)
    try:
        vehicles_expired = vehicles_expired_paginator.page(page)
    except PageNotAnInteger:
        vehicles_expired = vehicles_expired_paginator.page(1)
    except EmptyPage:
        vehicles_expired = vehicles_expired_paginator.page(vehicles_expired_paginator.num_pages)

    context = {
        "title": title,
        "licence_disk_list": licence_disk_list,
        "vehicles_with_disks_due_expiry":vehicles_due,
        "vehicles_with_expired_disks":vehicles_expired,
        "filter_form": filter_form,
        }
    return render(request, "licenceDiskRenewalList.html", context)




@login_required
@permission_required('fleet.create_incident', raise_exception=True)
def vehicleincidences(request, vehicle_id):
    title = "Add Vehicle Incidence"

    vehicle = Vehicle.objects.get(pk=vehicle_id)

    incident = Incident()
    incident.vehicle = vehicle
    incident.current_mileage = vehicle.get_current_mileage()
    if vehicle.get_current_driver() != "Not Allocated":
        incident.driver = vehicle.get_current_driver()


    form = IncidentForm(request.POST or None, instance=incident)
    comment_form = CommentsForm(request.POST or None)
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUpload.objects.filter(vehicle=vehicle, transaction="Incident")

    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]

    comments = Comment.objects.filter(vehicle = vehicle).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
        "title": title,
        "form": form,
        "comment_form": comment_form,
        "vehicle": vehicle,
        "upload_file_form": upload_file_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,

    }

    post = request.POST
    if request.POST:
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by=request.user
                save_form.save()
                vehicle.status = incident.damage_extent
                if incident.damage_extent == "Write Off":
                    vehicle.active = 0
                vehicle.save()
                latest_trans = Incident.objects.order_by('-id')[0]

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.vehicle = latest_trans.vehicle
                    new_comment.comment_type = "Incident"
                    new_comment.obj_id = latest_trans.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = FileUpload.objects.create(file=f)
                        uploaded.transaction_id = latest_trans.id
                        uploaded.vehicle = latest_trans.vehicle
                        uploaded.file_name = uploaded.file.name
                        uploaded.transaction = "Incident"
                        uploaded.save()
                return HttpResponseRedirect(reverse('fleet:viewvehicle', kwargs={'vehicle_id':vehicle.id}))

    return render(request, "vehicles.html", context)




@login_required
@permission_required('fleet.edit_incident', raise_exception=True)
def editvehicleincidences(request, trans_id):
    title = "Edit Vehicle Incidence"
    transaction = Incident.objects.get(pk=trans_id)
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)
    vehicle = transaction.vehicle
    trans_key = transaction.id
    vehicle_id = Vehicle.objects.filter(licence_plate=vehicle)
    vehicle = Vehicle.objects.get(pk=vehicle_id)

    form = IncidentForm(request.POST or None, instance=transaction)

    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUpload.objects.filter(vehicle=vehicle, transaction="Incident", transaction_id=trans_key)
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]
    comment_form = CommentsForm(request.POST or None)
    comments = Comment.objects.filter(vehicle = vehicle).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
        "title": title,
        "form": form,
        "comment_form": comment_form,
        "vehicle": vehicle,
        "upload_file_form": upload_file_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,

    }
    post = request.POST
    if request.POST:
        if u'save' in post:
            valid_form = form.is_valid()
            if valid_form:
                save_form = form.save(commit=False)
                save_form.created_by= creator
                save_form.modified_by=request.user
                save_form.save()

                comment = comment_form.is_valid()
                if comment:
                    new_comment = comment_form.save(commit=False)
                    new_comment.vehicle = vehicle
                    new_comment.comment_type = "Incident"
                    new_comment.obj_id = transaction.id
                    new_comment.created_by = request.user
                    new_comment.save()

                validated = upload_file_form.is_valid()
                if validated:
                    files = request.FILES.getlist('doc-file')
                    for f in files:
                        uploaded = FileUpload.objects.create(file=f)
                        uploaded.transaction_id = transaction.id
                        uploaded.vehicle = vehicle
                        uploaded.file_name = uploaded.file.name
                        uploaded.transaction = "Incident"
                        uploaded.save()
                return HttpResponseRedirect(reverse('fleet:viewvehicle', kwargs={'vehicle_id':vehicle.id}))
    return render(request, "vehicles.html", context)


@login_required
@permission_required('fleet.view_incident', raise_exception=True)
def viewvehicleincidences(request, trans_id):
    title = "View Vehicle Incident"
    transaction = Incident.objects.get(pk=trans_id)
    creator = ElopsysUser.objects.get(pk=transaction.created_by_id)
    vehicle = transaction.vehicle
    trans_key = transaction.id
    vehicle_id = Vehicle.objects.filter(licence_plate=vehicle)
    vehicle = Vehicle.objects.get(pk=vehicle_id)

    form = IncidentForm(request.POST or None, instance=transaction)

    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    uploads = FileUpload.objects.filter(vehicle=vehicle, transaction="Incident", transaction_id=trans_key)
    file_extension = ['.png', '.jpg', '.jpeg']
    sliders = FileUpload.objects.filter(vehicle=vehicle).values_list('file', flat=True).order_by('-id')
    images = ["/media/%s" % fn for fn in sliders if fn[-4:] in file_extension]
    images = images[:4]
    comment_form = CommentsForm(request.POST or None)
    comments = Comment.objects.filter(vehicle = vehicle).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 8)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context ={
        "title": title,
        "form": form,
        "comment_form": comment_form,
        "vehicle": vehicle,
        "upload_file_form": upload_file_form,
        "uploads": uploads,
        "sliders": images,
        "comments": comments,
        "view_transaction":True,

    }
    return render(request, "vehicles.html", context)


@login_required
@permission_required('fleet.view_incident', raise_exception=True)
def incidencesList(request):
    vehicle_incidences = Incident.objects.all()
    if request.user.regional_staff:
        vehicle_incidences = Incident.objects.filter(driver__branch__region=request.user.employee.branch.region)

    title = "Vehicle Incidences List"
    incidences_list = vehicle_incidences.order_by('-id')
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_incidences' in request.GET and filter_form.is_valid():
        date = 'incident_date'
        incidences_list = filter_form.filter(incidences_list, date)
    page = request.GET.get('page', 1)
    incidences_list_paginator = Paginator(incidences_list, 14)
    try:
        incidences_list = incidences_list_paginator.page(page)
    except PageNotAnInteger:
        incidences_list = incidences_list_paginator.page(1)
    except EmptyPage:
        incidences_list = incidences_list_paginator.page(incidences_list_paginator.num_pages)

    unclaimed_list = vehicle_incidences.filter(no_claim=False, claimed=False).order_by('-id')
    filter_form = TransactionsFilterForm(request.GET or None)
    if u'filter_unclaimed' in request.GET and filter_form.is_valid():
        date = 'incident_date'
        unclaimed_list = filter_form.filter(unclaimed_list, date)
    page = request.GET.get('page', 1)
    unclaimed_list_paginator = Paginator(unclaimed_list, 14)
    try:
        unclaimed_list = unclaimed_list_paginator.page(page)
    except PageNotAnInteger:
        unclaimed_list = unclaimed_list_paginator.page(1)
    except EmptyPage:
        unclaimed_list = unclaimed_list_paginator.page(unclaimed_list_paginator.num_pages)


    context ={
        "title": title,
        "unclaimed_list": unclaimed_list,
        "incidences_list": incidences_list,
        "filter_form": filter_form,
        }
    return render(request, "incidencesList.html", context)

@login_required
@permission_required('fleet.view_vehicle', raise_exception=True)
@csrf_exempt
def redirect_from_comment(req):
    obj_id = req.POST.get('id', None)
    obj_type = req.POST.get('type', None)

    redirect_url = ''

    if obj_type == 'Vehicle':
        redirect_url =  HttpResponseRedirect(reverse('fleet:editvehicle', kwargs={'vehicle_id':obj_id}))
    if obj_type == 'RenewLicenceDisk':
        redirect_url =  HttpResponseRedirect(reverse('fleet:editrenewlicencedisk', kwargs={'trans_id':obj_id}))
    if obj_type == 'Incidences':
        redirect_url =  HttpResponseRedirect(reverse('fleet:editrenewlicencedisk', kwargs={'trans_id':obj_id}))
    if obj_type == 'VehicleMaintenance':
        redirect_url =  HttpResponseRedirect(reverse('fleet:editvehiclemaintenance', kwargs={'trans_id':obj_id}))
    if obj_type == 'Trafficfine':
        redirect_url =  HttpResponseRedirect(reverse('fleet:edittrafficfines', kwargs={'trans_id':obj_id}))
    if obj_type == 'VehicleAllocation':
        redirect_url =  HttpResponseRedirect(reverse('fleet:editallocatevehicle', kwargs={'trans_id':obj_id}))
    if obj_type == 'FuelAllocation':
        redirect_url =  HttpResponseRedirect(reverse('fleet:editallocatefuel', kwargs={'trans_id':obj_id}))
    # if obj_type == 'FuelTransfer':
    #     redirect_url =  HttpResponseRedirect(reverse('fleet:editrenewlicencedisk', kwargs={'trans_id':obj_id}))
    if obj_type == 'MileageLog':
        redirect_url =  HttpResponseRedirect(reverse('fleet:editmileagelog', kwargs={'trans_id':obj_id}))
    if obj_type == 'ServiceBooking':
        redirect_url =  HttpResponseRedirect(reverse('fleet:editbookservice', kwargs={'trans_id':obj_id}))
    if obj_type == 'InsuranceClaim':
        redirect_url =  HttpResponseRedirect(reverse('fleet:editrenewlicencedisk', kwargs={'trans_id':obj_id}))

    return JsonResponse({'url': redirect_url['location']})

