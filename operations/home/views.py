#from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from django.core.mail import send_mail
from django.shortcuts import render
from django.core.urlresolvers import reverse
from .forms import ContactForm, SignUpForm
from fleet.models import *
from fleet.forms import *
from offices.models import *
from employees.models import *
from datetime import datetime, timedelta, date
from django.db.models import Count, Sum, Q
import calendar
# import datetime
import time
import json
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse

"""def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

"""
@login_required
def home(request): 
	title = "Welcome"	
	form = SignUpForm(request.POST or None)
	context ={
		"title": title,
		"form": form,
	}

	if form.is_valid():  
		#instance = form.save(commit=False)
		instance.save()
		context ={
			"title": "Thank you"
		}
	
	return render(request, "home.html", context)



def contact(request):
	form = ContactForm(request.POST or None)
	if form.is_valid():
		# for key, value in form.cleaned_data.iteritems():
		# 	print key, value
			#print form.cleaned_data.get(key)
		form_email = form.cleaned_data.get("email")
		form_message = form.cleaned_data.get("message")
		form_full_name = form.cleaned_data.get("full_name")
		#print email,message,full_name
		subject = 'Site contact form'
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email, 'lewisk@emeraldlife.co.za']
		contact_message = "%s: %s via %s"%(
			form_full_name,
			form_message,
			from_email)

		send_mail(subject,
			contact_message,
			from_email,
			to_email,
			fail_silently=False)

	context ={
		"form": form,
	}
	return render(request, "forms.html", context)



def dash(request):
	regions = Region.objects.all()
	all_fleet =  Vehicle.objects.filter(~Q(ownership_type="EL Staff"))
	insurance_claims = InsuranceClaim.objects.all()
	vehicle_maintenance = VehicleMaintenance.objects.all()
	all_traffic_fines =  Trafficfine.objects.all()
	all_incidences =  Incident.objects.all()
	if request.user.regional_staff:
		all_fleet = Vehicle.objects.filter(~Q(ownership_type="EL Staff"),current_driver__branch__region=request.user.employee.branch.region)
		insurance_claims = InsuranceClaim.objects.filter(driver__branch__region=request.user.employee.branch.region)
		vehicle_maintenance = VehicleMaintenance.objects.filter(driver__branch__region=request.user.employee.branch.region)
		all_traffic_fines = Trafficfine.objects.filter(driver__branch__region=request.user.employee.branch.region)
		all_incidences = Incident.objects.filter(driver__branch__region=request.user.employee.branch.region)

	title="Fleet Dashboard"
	x = 12
	now = time.localtime()
	year_months = [time.localtime(time.mktime((now.tm_year, now.tm_mon - n, 1, 0, 0, 0, 0, 0, 0)))[:2] for n in range(x)]
	maint_stats=[]
	
	for month in year_months:
		num_days= calendar.monthrange(month[0], month[1])
		fd=datetime(month[0], month[1],1)
		ld=datetime(month[0], month[1], num_days[1])
		tires = vehicle_maintenance.filter(maint_type="Tires", maint_date__range=[fd, ld]).aggregate(ac=Sum('actual_cost'))['ac'] or 0
		service = vehicle_maintenance.filter(maint_type="Service", maint_date__range=[fd, ld]).aggregate(ac=Sum('actual_cost'))['ac'] or 0
		total_maint = vehicle_maintenance.filter(maint_date__range=[fd, ld]).aggregate(ac=Sum('actual_cost'))['ac'] or 0
		maintenance = vehicle_maintenance.filter( maint_date__range=[fd, ld]).filter(~Q(Q(maint_type="Tires") | Q(maint_type="Service"))).aggregate(ac=Sum('actual_cost'))['ac'] or 0
		
		data = {
			'period':'{}-{}'.format(month[0], "{0:0=2d}".format(month[1])),
			'tires': '{0:.2f}'.format(tires),			
			'service':'{0:.2f}'.format(service),
			'repairs':'{0:.2f}'.format(maintenance),
		}
		maint_stats.append(data)

	el_fleet = all_fleet.filter(active=True, ownership_type="EL Fleet").aggregate(ac=Count('licence_plate'))['ac'] or 0
	el_leased = all_fleet.filter(active=True, ownership_type="EL Leased").aggregate(ac=Count('licence_plate'))['ac'] or 0

	status = ['Pending', 
			'Awaiting additional information from driver',
			'Awaiting Assessors Report', ]


	due_expiry_date = datetime.now() + timedelta(+30)
	expired_date = datetime.now() + timedelta(-1)
	todays_date = datetime.now()+ timedelta()

	vehicles_licencing_not_expired_count = all_fleet.filter(licence_disk_expiry__gte=expired_date, active=True).aggregate(ac=Count('id'))['ac'] or 0 
	vehicles_licencing_due = all_fleet.filter(licence_disk_expiry__range=[todays_date, due_expiry_date], active=True)
	vehicles_licencing_due_count = all_fleet.filter(licence_disk_expiry__range=[todays_date, due_expiry_date], active=True).aggregate(ac=Count('id'))['ac'] or 0
	vehicles_licencing_expired = all_fleet.filter(licence_disk_expiry__lte=expired_date, active=True)
	vehicles_licencing_expired_count = all_fleet.filter(licence_disk_expiry__lte=expired_date, active=True).aggregate(ac=Count('id'))['ac'] or 0 
	unsubmitted_inspections =  all_fleet.filter(inspected=False, active=True, )
	unsubmitted_inspections_count =  all_fleet.filter(inspected=False, active=True, ).aggregate(ac=Count('id'))['ac'] or 0
	total_amount_claims = insurance_claims.aggregate(ac=Sum('payout_amount'))['ac'] or 0
	total_amount_maintenance = vehicle_maintenance.aggregate(ac=Sum('actual_cost'))['ac'] or 0
	total_amount_excess = insurance_claims.aggregate(ac=Sum('excess'))['ac'] or 0
	finalized = insurance_claims.filter(claim_status='Finalized').aggregate(ac=Count('id'))['ac'] or 0
	pending = insurance_claims.filter(claim_status__in = status).aggregate(ac=Count('id'))['ac'] or 0
	rejected = insurance_claims.filter(claim_status='Rejected').aggregate(ac=Count('id'))['ac'] or 0
	unpaid_claims = insurance_claims.filter(~Q(claim_status='Finalized'))
	unpaid_claims_count = insurance_claims.filter(~Q(claim_status='Finalized')).aggregate(ac=Count('id'))['ac'] or 0

	drivers_licence = DrivingLicence()
	licence_form = DrivingLicenceForm(request.POST or None, instance=drivers_licence)
	vehicles = all_fleet.filter(~Q(ownership_type="EL Staff"),active=True, available=False)
	vehicles_due_service = []
	vehicles_over_due_service = []
	service_due =0
	service_over_due =0
	for v in vehicles:
		if v.get_next_service_mileage() - v.get_current_mileage() < 1400 and v.get_next_service_mileage() > v.get_current_mileage():
			service_due += 1
			vehicles_due_service.append(v)
		if v.get_next_service_mileage() < v.get_current_mileage():
			service_over_due += 1
			vehicles_over_due_service.append(v)
	out_of_smp = all_fleet.filter(Q(on_service_plan=True) | Q(on_maintenance_plan=True), 
											  plan_ending__lte=todays_date, 
											  active=True)
	out_of_smp_count = all_fleet.filter(Q(on_service_plan=True) | Q(on_maintenance_plan=True), 
											  plan_ending__lte=todays_date, 
											  active=True).aggregate(ac=Count('id'))['ac'] or 0 
	in_smp = all_fleet.filter(Q(on_service_plan=True) | Q(on_maintenance_plan=True), 
											  plan_ending__gte=todays_date, 
											  active=True)
	in_smp_count = all_fleet.filter(Q(on_service_plan=True) | Q(on_maintenance_plan=True), 
											  plan_ending__gte=todays_date, 
											  active=True).aggregate(ac=Count('id'))['ac'] or 0
	minor_damages_count = all_fleet.filter(status="Minor Damages", active=True).aggregate(ac=Count('id'))['ac'] or 0
	major_damages_count = all_fleet.filter(status="Major Damages'", active=True).aggregate(ac=Count('id'))['ac'] or 0
	minor_damages = all_fleet.filter(status="Minor Damages", active=True)
	major_damages = all_fleet.filter(status="Major Damages'", active=True)
	unclaimed_incidences_count = all_incidences.filter(no_claim=False, claimed=False).aggregate(ac=Count('id'))['ac'] or 0
	unclaimed_incidences = all_incidences.filter(no_claim=False, claimed=False)	

	vehicle_stats=[]
	regional_stats=[]	
	sl=Department.objects.filter(department="Sales")
	mk=Department.objects.filter(department="Marketing")
	full_fleet =  Vehicle.objects.filter(~Q(ownership_type="EL Staff"))
	full_insurance_claims = InsuranceClaim.objects.all()
	full_vehicle_maintenance = VehicleMaintenance.objects.all()
	full_traffic_fines =  Trafficfine.objects.all()
	full_incidences =  Incident.objects.all()

	for region in regions:
		fleet = full_fleet.filter(current_driver__branch__region=region, active=True, ownership_type="EL Fleet").aggregate(ac=Count('licence_plate'))['ac'] or 0
		leased = full_fleet.filter(current_driver__branch__region=region, active=True, ownership_type="EL Leased").aggregate(ac=Count('licence_plate'))['ac'] or 0
		write_offs = full_fleet.filter(current_driver__branch__region=region, status="Write Off").aggregate(ac=Count('licence_plate'))['ac'] or 0
		available = full_fleet.filter(current_driver__branch__region=region, available=True, active=True).aggregate(ac=Count('licence_plate'))['ac'] or 0
		fleet_count = full_fleet.filter(current_driver__branch__region=region, active=True).aggregate(ac=Count('licence_plate'))['ac'] or 0
		total_claims = full_insurance_claims.filter(driver__branch__region=region).aggregate(ac=Sum('payout_amount'))['ac'] or 0		
		total_maintenance = full_vehicle_maintenance.filter(driver__branch__region=region).aggregate(ac=Sum('actual_cost'))['ac'] or 0
		traffic_fines = full_traffic_fines.filter(driver__branch__region=region).aggregate(ac=Count('id'))['ac'] or 0
		minor_damaged = full_fleet.filter(current_driver__branch__region=region,status="Minor Damages", active=True).aggregate(ac=Count('id'))['ac'] or 0
		major_damaged = full_fleet.filter(current_driver__branch__region=region,status="Major Damages'", active=True).aggregate(ac=Count('id'))['ac'] or 0
		if fleet_count>0:			
			avg_claims = float(float(total_claims)/float(fleet_count))		
			avg_fines = float(float(traffic_fines)/float(fleet_count))
			avg_maintenance = float(float(total_maintenance)/float(fleet_count))
		else:
			avg_fines = 0 
			avg_maintenance = 0 
			avg_claims = 0

		incidences = full_incidences.filter(driver__branch__region=region).aggregate(ac=Count('id'))['ac'] or 0
		sales = full_fleet.filter(current_driver__department=sl, current_driver__branch__region=region, active=True).aggregate(ac=Count('id'))['ac'] or 0
		marketing = full_fleet.filter(current_driver__department=mk, current_driver__branch__region=region, active=True).aggregate(ac=Count('id'))['ac'] or 0
		data ={
				'region': str(region.prefix),
				'fleet':fleet,
				'leased':leased,
		}
		regStats ={
					'region': str(region.prefix)+' - '+str(region) ,
					'fleet_count':fleet_count,
					'write_offs':write_offs,
					'available':available,
					'total_claims':total_claims,
					'avg_claims':avg_claims,
					'total_maintenance':total_maintenance,
					'avg_maintenance':avg_maintenance,
					'minor_damaged':minor_damaged,
					'major_damaged':major_damaged,
					'traffic_fines':traffic_fines,
					'avg_fines':avg_fines,
					'marketing':marketing,
					'sales':sales,
					'incidences':incidences,
		}
		regional_stats.append(regStats)
		vehicle_stats.append(data)


	
	insurance_stats = {
			'pending':pending,
			'finalized': finalized,
			'rejected': rejected,
		}	
	
	context ={
		"vehicles":vehicles,
		"regional_stats": regional_stats,
		"title": title,
		"stats":maint_stats,
		"el_fleet":el_fleet,
		"el_leased":el_leased,
		"vehicle_stats":vehicle_stats,
		"insurance_stats":insurance_stats,
		"service_due":service_due,
		"service_over_due":service_over_due,
		"unsubmitted_inspections":unsubmitted_inspections,
		"unsubmitted_inspections_count":unsubmitted_inspections_count,
		'vehicles_licencing_due':vehicles_licencing_due,
		'vehicles_licencing_not_expired_count':vehicles_licencing_not_expired_count,
		'vehicles_licencing_due_count':vehicles_licencing_due_count,
		'vehicles_licencing_expired':vehicles_licencing_expired,
		'vehicles_licencing_expired_count':vehicles_licencing_expired_count,
		'unpaid_claims':unpaid_claims,
		'unpaid_claims_count':unpaid_claims_count,
		'finalized':finalized,
		'vehicles_due_service':vehicles_due_service,
		'vehicles_over_due_service':vehicles_over_due_service,
		'out_of_smp':out_of_smp,
		'out_of_smp_count':out_of_smp_count,
		'in_smp':in_smp,
		'in_smp_count':in_smp_count,
		'minor_damages_count':minor_damages_count,
		'major_damages_count':major_damages_count,
		'minor_damages':minor_damages,
		'major_damages':major_damages,		
		'unclaimed_incidences_count':unclaimed_incidences_count,
		'unclaimed_incidences':unclaimed_incidences,
		'total_amount_claims':total_amount_claims,
		'total_amount_excess':total_amount_excess,
		"licence_form":licence_form,
	}
	post = request.POST    
	if request.POST:
	    if u'save_modal' in post:
			valid_licence = licence_form.is_valid()
			if valid_licence:
				save_licence_form = licence_form.save(commit=False)
				save_licence_form.created_by = request.user
				save_licence_form.save()
				return HttpResponseRedirect(reverse('dash'))
	return render(request, "fleet_dash.html", context)