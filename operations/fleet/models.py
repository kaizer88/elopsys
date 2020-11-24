from __future__ import unicode_literals
from django.db import models
from django.db.models import Count, Sum, Q
from django.contrib.auth.models import AbstractUser
from employees.models import *
from offices.models import *
from accounts.models import ElopsysUser
from simple_history.models import HistoricalRecords
from datetime import datetime, timedelta
import os

#from dateutil.relativedelta import relativedelta

# Create your models here.
#=========================================================================================================================
#Location Models
#============================================================================================================


#=========================================================================================================================
#Vehicle Make and Models Model
#=========================================================================================================================

class VehicleMakeAndModel(models.Model):
  	make_n_model = models.CharField(max_length=120, null=True, blank=True)
  	vehicle_class = models.CharField(max_length=20, null=True, blank=True,
						choices=(
							('Sedan', 'Sedan'),
							('Hatch', 'Hatch Back'),
							('Single', 'Single Cab'),
							('Double', 'Double Cab'),
							('Club', 'Club Cab'),
							('Sports', 'Sports Utility Vehicle'),
							('Station', 'Station Wagon')
						)) 
  	fuel_type = models.CharField(max_length=20, null=True, blank=True,
						choices=(             
							('Petrol_95_Unleaded', 'Petrol 95 Unleaded'),
							('Petrol_LRP', 'Petrol LRP'),
							('Diesel_50PP', 'Diesel 50PP'),
							('Diesel_500PPM', 'Diesel 500PPM')
						))

  	engine_capacity = models.CharField(max_length=20, null=True, blank=True,
						choices=(
							('1.2_Liter', '1.2 Liter'),   
							('1.4_Liter', '1.4 Liter'),
							('1.5_Liter', '1.5 Liter'),
							('1.6_Liter', '1.6 Liter'),   
							('1.8_Liter', '1.8 Liter'),
							('1.8_Liter', '1.8 Liter'),   
							('2.2_Liter', '2.2 Liter'),
							('2.4_Liter', '2.4 Liter'),   
							('2.5_Liter', '2.5 Liter'),
							('2.7_Liter', '2.7 Liter'),   
							('2.8_Liter', '2.8 Liter'),
							('3.0_Liter', '3.0 Liter'),   
							('3.2_Liter', '3.2 Liter'),
							('3.4_Liter', '3.4 Liter'),   
							('3.6_Liter', '3.6 Liter'),
							('3.8_Liter', '3.8 Liter'),   
							('4.0_Liter', '3.6 Liter')
						))
  	transmission_type = models.CharField(max_length=20, null=True, blank=True,
						choices=(
							('Manual', 'Manaual'),
							('Automatic', 'Automatic')
						))
  	seats = models.CharField(max_length=20, null=False, default='5_seater',
						choices=(
						 	('5_seater', '5 Seater'),
						 	('7_seater', '7 Seater')
						))
  	steering = models.CharField(max_length=20, null=True, blank=True, default='right_hand_drive',
						choices=(
							('right_hand_drive', 'Right Hand Drive'),
							('left_hand_drive', 'Left Hand Drive')
						))
  	doors = models.CharField(max_length=20, null=True, blank=True,
						choices=(
							('2_doors', '2 Doors'),
							('3_doors', '3 Doors'),
							('4_doors', '4 Doors'),
							('5_doors', '5 Doors')
						)) 
  	tank_capacity = models.CharField(max_length=20, null=True, blank=True,
						choices=(
							('45_Liters', '45 Liters'),   
							('50_Liters', '50 Liters'),
							('55_Liters', '55 Liters'),   
							('60_Liters', '60 Liters'),
							('65_Liters', '65 Liters'),   
							('70_Liters', '70 Liters'),
							('75_Liters', '75 Liters'),   
							('80_Liters', '80 Liters'),
							('85_Liters', '85 Liters'),   
							('90_Liters', '90 Liters'),
							('95_Liters', '95 Liters'),   
							('100_Liters', '100 Liters')
						))
  	wheel_size = models.CharField(max_length=20, null=True, blank=True,
						choices=(
							('13_Inch', '13 Inch'), 
							('14_Inch', '14 Inch'),
							('15_inch', '15 Inch'),   
							('16_Inch', '16 Inch'),
							('17_Inch', '17 Inch'),   
							('18_Inch', '18 Inch'),
							('19_Inch', '19 Inch'),   
							('20 _nch', '20 Inch')	                         
						))
  	service_interval = models.IntegerField(null=True, blank=True)
  	history = HistoricalRecords() 
  	def __unicode__(self):
		return self.make_n_model


#=========================================================================================================================
#Vehicle Extras Model
#=========================================================================================================================

class VehicleExtras(models.Model):
	description = models.CharField(max_length=50, null=True, blank=True,)      
	make_n_model = models.ForeignKey(VehicleMakeAndModel, null=True, blank=True)	
	air_conditioner = models.BooleanField(blank=True, default=False)
	turbo = models.BooleanField(blank=True, default=False)
	sunroof = models.BooleanField(blank=True, default=False)
	alloy_wheels = models.BooleanField(blank=True, default=False)
	canopy = models.BooleanField(blank=True, default=False)
	leather_seats = models.BooleanField(blank=True, default=False)
	keyless_entry = models.BooleanField(blank=True, default=False)
	anti_bracking_system = models.BooleanField(blank=True, default=False)
	airbag = models.BooleanField(blank=True, default=False)
	dual_airbag = models.BooleanField(blank=True, default=False)
	long_base = models.BooleanField(blank=True, default=False)
	power_windows = models.BooleanField(blank=True, default=False)
	power_steering = models.BooleanField(blank=True, default=False)
	power_mirros = models.BooleanField(blank=True, default=False)
	anti_theft = models.BooleanField(blank=True, default=False)
	electronic_fuel_injection = models.BooleanField(blank=True, default=False)
	raised_suspension  = models.BooleanField(blank=True, default=False)
	lowerd_suspension  = models.BooleanField(blank=True, default=False)
	height_adjustable_seat = models.BooleanField(blank=True, default=False)
	height_adjustable_steering = models.BooleanField(blank=True, default=False)
	alarm_electronic_immobiliser= models.BooleanField(blank=True, default=False)
	central_locking_system= models.BooleanField(blank=True, default=False)
	radio_cd_4speakers= models.BooleanField(blank=True, default=False)
	usb_bluetooth= models.BooleanField(blank=True, default=False)
	history = HistoricalRecords()

	def __unicode__(self):
			return self.description
	

#========================================================================================================================
#File Numbers and File Uploads
#========================================================================================================================

class FuelCard(models.Model):
	card_number = models.CharField(max_length=120, null=False, blank=False, unique=True)	
	card_type = models.CharField(max_length=20, null=False, choices=(('Absa Fleet', 'Absa Fleet'),
		                                                         ('Eden Red', 'Eden Red') ,))
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_fuelcards')
	history = HistoricalRecords()
        
	def __unicode__(self):
			return self.card_number

# class FileUploads(models.Model):

# 	file_name = models.CharField(max_length=120, default=None, null=True, blank=True)
# 	parent_id = models.ForeignKey()
# 	table_name = models.ForeignKey()

#========================================================================================================================
#Vehicel Description Model
#========================================================================================================================

class Vehicle(models.Model):
	licence_plate = models.CharField(max_length=20, verbose_name="vehicle registration", unique=True, null=False, blank=False)
	ownership_type = models.CharField(max_length=20, null=True, blank=True,
		choices=(
			('EL Fleet', 'Emerald Life Fleet'),
			('EL Leased', 'Emerald Life Leased'),
			('EL Rental', 'Emerald Life Rental'),
			('EL Staff', 'Emerald Life Staff')
		))      
	make_n_model = models.ForeignKey(VehicleMakeAndModel, verbose_name="make &amp model", null=True, blank=True)	
	vin_number = models.CharField(max_length=120, default=None, null=True, blank=True)
	model_year = models.CharField(max_length=4, verbose_name="year model", default=None, null=True, blank=True)
	signing_mileage = models.FloatField(null=True, blank=True, max_length=20, default=0)
	licence_disk_expiry = models.DateField(null=True, blank=True, auto_now=False, editable=True)  
	color = models.CharField(max_length=20, null=False, default='White',
							choices=(
								('Beige', 'Beige'),
								('Black', 'Black') ,     
								('Red', 'Red'),
								('Bronze', 'Bronze'),    
								('Brass', 'Brass'),
								('Brown', 'Brown'),      
								('Charcoal', 'Charcoal'),
								('Cherry', 'Cherry'),    
								('Champaigne', 'Champaigne'),
								('Cream', 'Cream'),      
								('Creamson', 'Creamson'),
								('Coffee', 'Coffee'),    
								('Green', 'Green'),
								('Gold', 'Gold'),      
								('Khaki', 'Khaki'),
								('Light_Blue', 'Light Blue'), 
								('Lime', 'Lime'),
								('Maroon', 'Maroon'),    
								('Orange', 'Orange'),
								('Purple', 'Purple'),    
								('Silver', 'Silver'),
								('Siena', 'Siena'),      
								('Tan', 'Tan'),
								('Turquoise', 'Turquoise'),  
								('Violet', 'Violet'),
								('White', 'White'),      
								('Yellow', 'Yellow')
							)) 
	status = models.CharField(max_length=20, default=None, null=True, blank=True,
							choices=(
								('Good Condition', 'Vehicle in good condition'),
								('Minor Damages', 'Vehicle with minor damage'),
								('Major Damages', 'Vehicle with major damage'),
								('Write Off', 'Vehicle write off')
							))  
	available = models.BooleanField(blank=True, default=True)
	active = models.BooleanField(blank=True, default=True)
	rental_starting = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	rental_ending = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	lease_starting = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	lease_ending = models.DateField(null=True, blank=True, auto_now=False, editable=True)	
	purchase_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	purchase_amount = models.FloatField(null=True, blank=True, max_length=20, default=0)	
	supplier = models.CharField(max_length=120, default=None, null=True, blank=True)
	condition = models.CharField(max_length=20, default=None, null=True, blank=True,
						choices=(
							('Brand_New', 'Brand New'),
							('Pre_Owned', 'Pre Owned')
						))
	invoice_number = models.CharField(max_length=50, default=None, null=True, blank=True)
	account_number = models.CharField(max_length=120, default=None, null=True, blank=True)
	warranty_expiry = models.CharField(max_length=120, default=None, null=True, blank=True)
	financier = models.CharField(max_length=50, default=None, null=True, blank=True,
						choices=(
							('Not_Financed', 'Not Financed'),
							('ABSA_Financial_Serveice', 'ABSA Financial Services'),
							('Wesbank', 'Wesbank'),
							('VW_Financial_Services', 'VW Financial Services'),
							('Toyota_Financial_Services', 'Toyota Financial Services'),
							('Nedbank_Financial_Services', 'Nedbank Financial Services')
						  ))
	has_tracker = models.BooleanField(blank=True, default=False)
	inspected = models.BooleanField(blank=True, default=False)
	last_inspected = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	tracker_provider = models.CharField(max_length=120, default=None, null=True, blank=True)
	insured = models.BooleanField(blank=True, default=False)
	insurer = models.CharField(max_length=120, default=None, null=True, blank=True)
	on_service_plan = models.BooleanField(blank=True, default=False)
	on_maintenance_plan = models.BooleanField(blank=True, default=False)
	plan_provider = models.CharField(max_length=120, default=None, null=True, blank=True)
	period = models.CharField(max_length=20, default=None, null=True, blank=True)
	plan_starting = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	plan_ending = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	mileage_covered = models.FloatField(null=True, blank=True, max_length=20, default=0)
	current_driver = models.ForeignKey('employees.Employee', null=True, blank=True)
	fuel_balance = models.FloatField(null=True, blank=True, max_length=20, default=0)
	division = models.CharField(max_length=20, default=None, null=True, blank=True,
						choices=(
							('Marketing', 'Marketing'),
							('Sales', 'Sales')
						)) 	
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_vehicle')	
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_vehicle')	
	history = HistoricalRecords()

	@property
	def vehicle(self):
		return self.licence_plate

	def get_count_fines(self):       			
		fines_count = Trafficfine.objects.filter(vehicle=self).aggregate(count_fines=Count('vehicle'))["count_fines"]
		if fines_count:
			return fines_count
		else:
			return 0

	def get_count_fines_paid(self):       			
		fines_count = Trafficfine.objects.filter(vehicle=self, paid=1).aggregate(count_fines=Count('vehicle'))["count_fines"]
		if fines_count:
			return fines_count
		else:
			return 0

	def get_count_fines_pending(self):       			
		fines_count = Trafficfine.objects.filter(vehicle=self, paid=0).aggregate(count_fines=Count('vehicle'))["count_fines"]
		if fines_count:
			return fines_count
		else:
			return 0

	def get_count_fines_serious(self):       			
		fines_count = Trafficfine.objects.filter(vehicle=self, serious_offence=1).aggregate(count_fines=Count('vehicle'))["count_fines"]
		if fines_count:
			return fines_count
		else:
			return 0

	def get_count_fines_court(self):       			
		fines_count = Trafficfine.objects.filter(vehicle=self, court_appearance=1).aggregate(count_fines=Count('vehicle'))["count_fines"]
		if fines_count:
			return fines_count
		else:
			return 0

	def get_total_fines(self):       			
		total_fines = Trafficfine.objects.filter(vehicle=self).aggregate(total_fines=Sum('amount'))["total_fines"]
		if total_fines:
			return total_fines
		else:
			return 0

	def get_count_claims(self):       			
		claims_count = InsuranceClaim.objects.filter(vehicle=self).aggregate(count_claims=Count('vehicle'))["count_claims"]
		if claims_count:
			return claims_count
		else:
			return 0

	def get_count_claims_pending(self):       			
		claims_count = InsuranceClaim.objects.filter(vehicle=self, claim_status="Pending").aggregate(count_claims=Count('vehicle'))["count_claims"]
		if claims_count:
			return claims_count
		else:
			return 0

	def get_count_claims_finalized(self):       			
		claims_count = InsuranceClaim.objects.filter(vehicle=self, claim_status="Finalized").aggregate(count_claims=Count('vehicle'))["count_claims"]
		if claims_count:
			return claims_count
		else:
			return 0

	def get_count_claims_rejected(self):       			
		claims_count = InsuranceClaim.objects.filter(vehicle=self, claim_status="Rejected").aggregate(count_claims=Count('vehicle'))["count_claims"]
		if claims_count:
			return claims_count
		else:
			return 0

	def get_total_claims(self):       			
		total_claims = InsuranceClaim.objects.filter(vehicle=self, claim_status="Pending").aggregate(total_claims=Sum('payout_amount'))["total_claims"]
		if total_claims:
			return total_claims 
		else:
			return 0

	def get_total_excess(self):       			
		total_claims = InsuranceClaim.objects.filter(vehicle=self, claim_status="Pending").aggregate(total_claims=Sum('excess'))["total_claims"]
		if total_claims:
			return total_claims 
		else: 
			return 0

	
	def get_count_incidences(self):       			
		incidences_count = Incident.objects.filter(vehicle=self).aggregate(count_incidences=Count('vehicle'))["count_incidences"]
		if incidences_count:
			return incidences_count
		else:
			return 0

	def get_total_maintenance_cost(self):       			
		total_maintenance = VehicleMaintenance.objects.filter(vehicle=self).aggregate(total_maintenance=Sum('actual_cost'))["total_maintenance"]
		if total_maintenance:
			return total_maintenance 
		else:
			return 0

	def get_total_maintenance(self):       			
		total_maintenance = VehicleMaintenance.objects.filter(vehicle=self).filter(~Q(maint_type="Tires")).filter(~Q(maint_type="Service")).aggregate(total_maintenance=Sum('actual_cost'))["total_maintenance"]
		if total_maintenance:
			return total_maintenance 
		else:
			return 0

	def get_total_tyres_cost(self):       			
		total_tyres = VehicleMaintenance.objects.filter(vehicle=self, maint_type="Tires").aggregate(total_tyres_cost=Sum('actual_cost'))["total_tyres_cost"]
		if total_tyres:
			return total_tyres 
		else:
			return 0

	def get_total_service_cost (self):       			
		total_service = VehicleMaintenance.objects.filter(vehicle=self, maint_type="Service").aggregate(total_service_cost=Sum('actual_cost'))["total_service_cost"]
		if total_service:
			return total_service 
		else:
			return 0

	def get_current_mileage(self):
		mileage_log = MileageLog.objects.filter(vehicle=self).order_by("-current_mileage").first()
		if mileage_log:
			return mileage_log.current_mileage
		else:
			return self.signing_mileage

	def get_monthly_mileage(self):
		this_month = datetime.now().month
		this_year = datetime.now().year
		mileage_log = MileageLog.objects.filter(vehicle=self,log_date__month=this_month,log_date__year=this_year).aggregate(current_total_mileage=Sum('mileage'))["current_total_mileage"]
		if mileage_log:
			return mileage_log
		else:
			return 0.0

	def get_monthly_fuel(self):
		this_month = datetime.now().month
		this_year = datetime.now().year
		mileage_log = MileageLog.objects.filter(vehicle=self,log_date__month=this_month,log_date__year=this_year).aggregate(current_total_fuel=Sum('fuel_used'))["current_total_fuel"]
		if mileage_log:
			return mileage_log
		else:
			return 0.0

	def get_monthly_fuel_absa(self):
		this_month = datetime.now().replace(day=1)- timedelta(days=1)
		start_this_month = this_month.replace(day=1)

		this_year = datetime.now().year
		mileage_log = FuelUsage.objects.filter(vehicle=self,transaction_date__range=[start_this_month,this_month]).aggregate(current_total_fuel=Sum('amount'))["current_total_fuel"]
		if mileage_log:
			return mileage_log
		else:
			return 0.0

	def get_total_mileage(self):          		    			
		mileage_log = MileageLog.objects.filter(vehicle=self).aggregate(total_mileage=Sum('mileage'))["total_mileage"]
		if mileage_log:
			return mileage_log
		else:
			return 0.0

	def get_total_fuel(self):       			
		mileage_log = MileageLog.objects.filter(vehicle=self).aggregate(total_fuel=Sum('fuel_used'))["total_fuel"]
		if mileage_log:
			return mileage_log
		else:
			return 0.0

	def get_total_fuel_allocated(self):       			
		mileage_log = FuelAllocations.objects.filter(vehicle=self).aggregate(total_fuel=Sum('amount_allocated'))["total_fuel"]
		if mileage_log:
			return mileage_log
		else:
			return 0.0

	def get_total_fuel_absa(self):       			
		fuel = FuelUsage.objects.filter(vehicle=self).aggregate(total_fuel=Sum('amount'))["total_fuel"]
		if fuel:
			return fuel
		else:
			return 0.0

	def get_next_service_mileage(self):
		service_booking = ServiceBooking.objects.filter(vehicle=self).order_by("-service_date", "-id").first()
		svi = VehicleMakeAndModel.objects.get(pk=self.make_n_model_id)
		if service_booking:
			if self.get_current_mileage() >= 100000:
				return service_booking.mileage + 10000
			else:
				return service_booking.next_service_mileage
		else:  
			booking_mileage = self.signing_mileage 
			if booking_mileage >= 100000:
				booking_mileage += 10000
				return booking_mileage
			else:
				if booking_mileage <= svi.service_interval:
					booking_mileage = svi.service_interval
				else:
					booking_mileage += svi.service_interval	        			
				return booking_mileage  

	def get_last_service_mileage(self):
		service_booking = ServiceBooking.objects.filter(vehicle=self).order_by("-service_date", "-id").first()
		
		if service_booking:
			return service_booking.mileage
		else: 				        			
			return 0   

	def get_last_Licence_renewal_date(self):	
		renewal = RenewLicenceDisk.objects.filter(vehicle=self).order_by("-id")		
		if renewal.exists():
			return renewal.first().renewal_date
		return None
		
	def get_current_driver(self):
		allocation = VehicleAllocation.objects.filter(vehicle=self).order_by("-allocation_date", "-id").first()
		if allocation:
			return allocation.driver
		else:
			return "Not Allocated"

	def driver_has_licence(self):
		licenced = DrivingLicence.objects.filter(driver=self.get_current_driver())
		has_licence = True
		if len(licenced)==0:
			has_licence = False
		return has_licence
	        		
	def __unicode__(self):
		return self.vehicle

class FileUpload(models.Model):
	vehicle = models.ForeignKey(Vehicle, null=True, blank=True, related_name='vehicle_vehicleFileUploads')
	file_name = models.CharField(max_length=255, blank=True)
	file = models.FileField(upload_to='uploads/fleet')
	transaction_id = models.CharField(max_length=20, default=None, null=True, blank=True)
	transaction = models.CharField(max_length=50, default=None, null=True, blank=True)
	date_uploaded = models.DateTimeField(auto_now_add=True)

	@property
	def filename(self):
		return os.path.basename(self.file.name)
	@property
	def relative_path(self):
		return os.path.relpath(self.path, settings.MEDIA_ROOT)

class FuelAllocation(models.Model):
	allocation_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	transaction_type = models.CharField(max_length=20, null=False, default=None,
							choices=(
								('Monthly Allocation', 'Monthly Allocation'),
								('Top up', 'Top up') ,)) 
	vehicle = models.ForeignKey(Vehicle, null=False, blank=False, related_name='vehicle_fuelAllocations')
	driver = models.ForeignKey('employees.Employee', null=False, blank=False, related_name='driver_fuelAllocations')
	fuel_card = models.ForeignKey(FuelCard, null=True, blank=True)
	balance = models.FloatField(null=True, blank=True, max_length=20, default=0)
	amount_allocated = models.FloatField(null=True, blank=True, max_length=20, default=0)
	new_balance = models.FloatField(null=True, blank=True, max_length=20, default=0)
	accept = models.BooleanField(blank=True, default=False)	
	authorize = models.CharField(max_length=20, default='Pending', null=True, blank=True,
							choices=(
								('Pending', 'Pending'),
								('Aproved', 'Authorize'),
								('Declined', 'Decline')
							))
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_fuelAllocations')

	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_fuelAllocations')	
	history = HistoricalRecords()

class FuelUsage(models.Model):
	fleet_node_number = models.CharField(max_length=250, default=None, null=True, blank=True)
	fms_account_number = models.CharField(max_length=250, default=None, null=True, blank=True)
	vehicle = models.ForeignKey(Vehicle, null=False, blank=False, related_name='vehicle_fuelusage')
	fuel_card = models.ForeignKey(FuelCard, null=True, blank=True, related_name='fuel_card_fuelusage')	
	driver = models.ForeignKey('employees.Employee', null=False, blank=False, related_name='driver_fuelusage')
	cost_center_number = models.CharField(max_length=250, default=None, null=True, blank=True)
	cost_centre_name = models.CharField(max_length=250, default=None, null=True, blank=True)
	client_reference_1 = models.CharField(max_length=250, default=None, null=True, blank=True)
	client_reference_2 = models.CharField(max_length=250, default=None, null=True, blank=True)
	transaction_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	transaction_number = models.CharField(max_length=250, default=None, null=True, blank=True)
	merchant_name = models.CharField(max_length=250, default=None, null=True, blank=True)
	transaction_code = models.CharField(max_length=25, default=None, null=True, blank=True)
	transaction_description = models.CharField(max_length=250, default=None, null=True, blank=True)
	odometer_reading = models.FloatField(null=True, blank=True, max_length=20, default=0)
	distance_travelled = models.FloatField(null=True, blank=True, max_length=20, default=0)
	quantity = models.FloatField(null=True, blank=True, max_length=20, default=0)
	amount = models.FloatField(null=True, blank=True, max_length=20, default=0)
	private_usage = models.CharField(max_length=25, default=None, null=True, blank=True)
	inhouse_indicator = models.CharField(max_length=25, default=None, null=True, blank=True)
	current_usage = models.CharField(max_length=250, default=None, null=True, blank=True)
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_fuelusage')
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_fuelusage')	
	history = HistoricalRecords()

class FuelTransfer(models.Model):
	transfer_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	from_vehicle = models.ForeignKey(Vehicle, null=False, blank=False, related_name='fromvehicle_transferss')
	from_driver = models.ForeignKey('employees.Employee', null=False, blank=False, related_name='fromdriver_transfers')
	from_fuel_card = models.ForeignKey(FuelCard, null=True, blank=True, related_name='fromfuelcard_transfers')
	from_balance = models.FloatField(null=True, blank=True, max_length=20, default=0)
	from_amount_allocated = models.FloatField(null=True, blank=True, max_length=20, default=0)
	from_new_balance = models.FloatField(null=True, blank=True, max_length=20, default=0)
	vehicle = models.ForeignKey(Vehicle, null=False, blank=False, related_name='tovehicle_transferss')
	driver = models.ForeignKey('employees.Employee', null=False, blank=False, related_name='todriver_transfers')
	to_fuel_card = models.ForeignKey(FuelCard, null=True, blank=True, related_name='tofuelcard_transfers')
	to_balance = models.FloatField(null=True, blank=True, max_length=20, default=0)
	to_amount_allocated = models.FloatField(null=True, blank=True, max_length=20, default=0)
	to_new_balance = models.FloatField(null=True, blank=True, max_length=20, default=0)
	accept = models.BooleanField(blank=True, default=False)	
	authorize = models.CharField(max_length=20, default='Pending', null=True, blank=True,
							choices=(
								('Pending', 'Pending'),
								('Aproved', 'Authorize'),
								('Declined', 'Decline')
							))
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_transfers')
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_transfers')	
	history = HistoricalRecords()


#=========================================================================================================================
#Vehicle Allocations Model
#=========================================================================================================================

class VehicleAllocation(models.Model):
	vehicle = models.ForeignKey(Vehicle, null=False, blank=False, related_name='vehicle_VehicleAllocations')
	transaction_type = models.CharField(max_length=20, default=None, null=True, blank=True,
						choices=(
							('Allocated', 'Allocate Vehicle'),
							('Returned', 'Return Vehicle'),
							('Returned_To_SP','Return To Service Provider')
						))
	driver = models.ForeignKey('employees.Employee', null=False, blank=False, related_name='driver_VehicleAllocations')
	allocation_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)	
	fuel_card = models.ForeignKey(FuelCard, null=True, blank=True)	
	cycle_limit = models.FloatField(null=True, blank=True, max_length=20, default=0)
	mileage = models.FloatField(null=True, blank=True, max_length=20, default=0)
	status = models.CharField(max_length=20, default=None, null=True, blank=True,
							choices=(
								('Good Condition', 'Vehicle in good condition'),
								('Minor Damages', 'Vehicle with minor damage'),
								('Major Damages', 'Vehicle with major damage'),
								('Write Off', 'Vehicle write off')
							))
		
	accept = models.BooleanField(blank=True, default=False)	
	authorize = models.CharField(max_length=20, default='Pending', null=True, blank=True,
							choices=(
								('Pending', 'Pending'),
								('Aproved', 'Authorize'),
								('Declined', 'Decline')
							))
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_VehicleAllocations')	
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_VehicleAllocations')	
	history = HistoricalRecords()


#=========================================================================================================================
#Vehicle Service Bookings Model
#=========================================================================================================================

class ServiceBooking(models.Model):

	vehicle = models.ForeignKey(Vehicle, null=False, blank=False, related_name='vehicle_serviceBookings')	
	driver = models.ForeignKey('employees.Employee', null=False, blank=False, related_name='driver_serviceBookings')
	service_type = models.CharField(max_length=20, default=None, null=True, blank=True,
							choices=(								
								('Minor', 'Minor Service'),
								('Major', 'Major Service')
							))
	service_description = models.CharField(max_length=2500, default=None, null=True, blank=True)
	booking_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	service_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	garage = models.CharField(max_length=250, default=None, null=True, blank=True)
	mileage = models.FloatField(null=True, blank=True, max_length=20, default=0)
	next_service_mileage = models.FloatField(null=True, blank=True, max_length=20, default=0)
	wheel_alignment = models.BooleanField(blank=True, default=False)
	wheel_balancing = models.BooleanField(blank=True, default=False)
	change_cam_belt = models.BooleanField(blank=True, default=False)
	air_con_regass = models.BooleanField(blank=True, default=False)
	serviced = models.BooleanField(blank=True, default=False)	
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_serviceBookings')	
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_ServiceBookings')		
	history = HistoricalRecords()
	@property
	def maintenance_ref(self):
		return "%s-%s"%(self.vehicle,self.service_date)
		

	def __unicode__(self):
		return self.maintenance_ref

#=========================================================================================================================
#Vehicle Traffic Fines Model
#=========================================================================================================================

class Trafficfine(models.Model):

	vehicle = models.ForeignKey(Vehicle, null=False, blank=False, related_name='vehicle_trafficFines')
	driver = models.ForeignKey('employees.Employee', null=False, blank=False, related_name='driver_trafficFines')
	notice_number = models.CharField(max_length=250, unique=True, null=False, blank=False)
	offence_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	offence_time =  models.TimeField(null=True, blank=True, auto_now=False, editable=True, verbose_name="Time")
	due_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	conversion_date = models.DateField(null=True, blank=True, auto_now=False, editable=True, verbose_name="Date converted to driver")
	description = models.CharField(max_length=250, default=None, null=True, blank=True)
	location = models.CharField(max_length=250, default=None, null=True, blank=True)
	amount = models.FloatField(null=True, blank=True, max_length=20, default=0)
	court_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)	
	serious_offence = models.BooleanField(blank=True, default=False)
	awaiting_summons = models.BooleanField(blank=True, default=False)
	court_appearance = models.BooleanField(blank=True, default=False)	
	court_attended = models.BooleanField(blank=True, default=False)
	paid = models.BooleanField(blank=True, default=False)
	payment_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	
	accept = models.BooleanField(blank=True, default=False)	
	authorize = models.CharField(max_length=20, default='Pending', null=True, blank=True,
							choices=(
								('Pending', 'Pending'),
								('Aproved', 'Authorize'),
								('Declined', 'Decline')
							))
	
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_trafficFines')	
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_trafficFines')	
	history = HistoricalRecords()
	

#=========================================================================================================================
#Vehicle Mileages Model
#=========================================================================================================================
class MileageLog(models.Model):

        INTEGRITY_SCALE = ((1, '5: Excellent'),(2, '4: Very Good'),
                           (3, '3: Good'),(4, '2: Bad'),(5, '1: very Bad'))
                
	log_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)	
	vehicle = models.ForeignKey(Vehicle, null=False, blank=False, related_name="vehicle_mileage_logs")
	driver = models.ForeignKey('employees.Employee', null=False, blank=False,related_name='driver_mileageLogs')
	starting_mileage = models.FloatField(null=True, blank=True, max_length=20, default=0)
	current_mileage = models.FloatField(null=True, blank=True, max_length=20, default=0)	
	mileage = models.FloatField(null=True, blank=True, max_length=20, default=0)
	fuel_balance_bf = models.FloatField(null=True, blank=True, max_length=20, default=0)
	fuel_used = models.FloatField(null=True, blank=True, max_length=20, default=0)
	fuel_balance = models.FloatField(null=True, blank=True, max_length=20, default=0)
	start_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	end_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	status = models.CharField(max_length=20, null=True, blank=True,
				  choices=(('Good Condition', 'Vehicle in good condition'),
					   ('Minor Damages', 'Vehicle with minor damage'),
					   ('Major Damages', 'Vehicle with major damage'),
					   ('Write Off', 'Vehicle write off')))

	doors = models.IntegerField(null=True, blank=True, choices=INTEGRITY_SCALE)
	seats = models.IntegerField(null=True, blank=True, choices=INTEGRITY_SCALE)
	body = models.IntegerField(null=True, blank=True, choices=INTEGRITY_SCALE)
	tires = models.IntegerField(null=True, blank=True, choices=INTEGRITY_SCALE)
	interior = models.IntegerField(null=True, blank=True, choices=INTEGRITY_SCALE)
	boot = models.FloatField(null=True, blank=True, choices=INTEGRITY_SCALE)
	under_hood = models.IntegerField(null=True, blank=True, choices=INTEGRITY_SCALE)
	engine_check = models.IntegerField(null=True, blank=True, choices=INTEGRITY_SCALE)
	exhaust_check = models.IntegerField(null=True, blank=True, choices=INTEGRITY_SCALE)
	feature_check = models.IntegerField(null=True, blank=True, choices=INTEGRITY_SCALE)
	sound_system = models.IntegerField(null=True, blank=True, choices=INTEGRITY_SCALE)
	steering = models.IntegerField(null=True, blank=True, choices=INTEGRITY_SCALE)
	brakes = models.IntegerField(null=True, blank=True, choices=INTEGRITY_SCALE)
	transmission = models.IntegerField(null=True, blank=True, choices=INTEGRITY_SCALE)
	overall_feel = models.IntegerField(null=True, blank=True, choices=INTEGRITY_SCALE)	
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_mileage_logs')	
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_mileage_logs')	
	history = HistoricalRecords()


class Trip(models.Model):
	vehicle = models.ForeignKey(Vehicle, null=True, blank=True, related_name='vehicle_trip')
	driver = models.ForeignKey('employees.Employee', null=True, blank=True, related_name='driver_trip')
	log_date = models.DateTimeField(null=True, blank=True, auto_now=False, editable=True)
	duration = models.DateTimeField(null=True, blank=True, auto_now=False, editable=True)
	avarage_speed = models.IntegerField(null=True, blank=True)
	max_speed = models.IntegerField(null=True, blank=True)
	distance = models.IntegerField(null=True, blank=True)
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_trip')


class TripLog(models.Model):
	trip_number = models.ForeignKey(Trip, null=True, blank=True)		
	log_date = models.DateTimeField(null=True, blank=True, auto_now=False, editable=True)
	location = models.CharField(max_length=2500, default=None, null=True, blank=True)		
	road_speed = models.FloatField(null=True, blank=True, max_length=20, default=0)
	speed = models.FloatField(null=True, blank=True, max_length=20, default=0)
	odometer = models.FloatField(null=True, blank=True, max_length=20, default=0)	
	status = models.CharField(max_length=50, default=None, null=True, blank=True)
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_triplog')
	


#=========================================================================================================================
#Vehicle Maintenance Model
#=========================================================================================================================

class VehicleMaintenance(models.Model):

	maint_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	maint_type = models.CharField(max_length=200, default=None, null=True, blank=True,
							choices=(								
								('Body Works', 'Body Works'),
								('Electrical', 'Eloctronic'),
								('Engine ', 'Engine'),
								('Gearbox', 'Gearbox'),
								('Service', 'Service'),
								('Suspension', 'Suspension'),
								('Tires', 'Tyres'),
								('Towing', 'Towing'),
							))		
	vehicle = models.ForeignKey(Vehicle, null=False, blank=False, related_name='vehicle_vehicleMaintenance')	
	driver = models.ForeignKey('employees.Employee', null=False, blank=False, related_name='driver_vehicleMaintenance')
	current_mileage = models.FloatField(null=True, blank=True, max_length=20, default=0)
	description = models.CharField(max_length=2000, default=None, null=True, blank=True)
	projected_cost = models.FloatField(null=True, blank=True, max_length=20, default=0)
	actual_cost = models.FloatField(null=True, blank=True, max_length=20, default=0)	
	difference = models.FloatField(null=True, blank=True, max_length=20, default=0)
	status = models.CharField(max_length=20, default=None, null=True, blank=True,
							choices=(
								('Good Condition', 'Vehicle in good condition'),
								('Minor Damages', 'Vehicle with minor damage'),
								('Major Damages', 'Vehicle with major damage'),
								('Write Off', 'Vehicle write off')
							))	
	invoice_number = models.CharField(max_length=200, default=None, null=True, blank=True)
	service_provider = models.CharField(max_length=200, default=None, null=True, blank=True)
	service_booking_number = models.ForeignKey(ServiceBooking, null=True, blank=True, related_name='servicebooking_vehicleMaintenance')
	accept = models.BooleanField(blank=True, default=False)	
	authorize = models.CharField(max_length=20, default='Pending', null=True, blank=True,
							choices=(							
								('Pending', 'Pending'),
								('Aproved', 'Authorize'),
								('Declined', 'Decline')
							))
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_vehicleMaintenance')	
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_vehicleMaintenance')	
	history = HistoricalRecords()


#=========================================================================================================================
#Vehicle Renewals Models
#=========================================================================================================================

class RenewLicenceDisk(models.Model):

	vehicle = models.ForeignKey(Vehicle, null=False, blank=False, related_name='vehicle_renewLicenceDisk')
	driver = models.ForeignKey('employees.Employee', null=False, blank=False, related_name='driver_renewLicenceDisk')
	expiry_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	renewal_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	amount = models.FloatField(null=True, blank=True, max_length=20, default=0)
	new_expiry_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)	
	
	accept = models.BooleanField(blank=True, default=False)	
	authorize = models.CharField(max_length=20, default='Pending', null=True, blank=True,
							choices=(	
								('Pending', 'Pending'),													
								('Aproved', 'Authorize'),
								('Declined', 'Decline')
							))
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_liceenceRenewals')	
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_licenceRenewals')	
	history = HistoricalRecords()
	

#=========================================================================================================================
#Vehicle Incidences Models
#=========================================================================================================================

class Incident(models.Model):

	vehicle = models.ForeignKey(Vehicle, null=False, blank=False, related_name='vehicle_incidences')
	driver = models.ForeignKey('employees.Employee', null=False, blank=False, related_name='driver_incidences')	
	incident_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	time_of_incident = models.TimeField(null=True, blank=True, auto_now=False, editable=True)
	incident_type = models.CharField(max_length=200, default=None, null=True, blank=True,
							choices=(								
								('Road Accident', 'Road Accident'),
								('Mechanical Breakdown', 'Mechanical Breakdown'),
								('Tire Puncture', 'Tire Puncture'),
								('Wind Screen Damages', 'Wind Screen Damages'),
								('Head Lamp Damage', 'Head Lamp Damage'),
								('Body Dants & Scratches', 'Body Dents & Scratches'),
								('Car Theft & Hijacking', 'Car Theft & Hijacking'),
								('Vandalism', 'Vandalism')
							))
	case_number = models.CharField(max_length=120, unique=True, null=False, blank=False)
	location = models.CharField(max_length=120, default=None, null=True, blank=True)
	Description = models.CharField(max_length=2000, default=None, null=True, blank=True)	
	date_reported = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	police_station = models.CharField(max_length=200, default=None, null=True, blank=True)
	damage_extent = models.CharField(max_length=200, default=None, null=True, blank=True,
							choices=(								
								('Minor Damages', 'Vehicle with minor damage'),
								('Major Damages', 'Vehicle with major damage'),
								('Write Off', 'Vehicle write off')
							))
	current_mileage = models.FloatField(null=True, blank=True, max_length=20, default=0)
	no_claim = models.BooleanField(blank=True, default=False)
	claimed = models.BooleanField(blank=True, default=False)
	right_rear_fender = models.BooleanField(blank=True, default=False)
	right_rear_wheel = models.BooleanField(blank=True, default=False)
	right_rear_door = models.BooleanField(blank=True, default=False)
	right_rear_lamp = models.BooleanField(blank=True, default=False)
	right_rear_window = models.BooleanField(blank=True, default=False)
	right_rear_door_window = models.BooleanField(blank=True, default=False)
	right_rear_viewmirror = models.BooleanField(blank=True, default=False)
	right_front_door_window = models.BooleanField(blank=True, default=False)
	right_front_door = models.BooleanField(blank=True, default=False)
	right_front_wheel = models.BooleanField(blank=True, default=False)
	right_front_fender = models.BooleanField(blank=True, default=False)	
	right_head_lamp = models.BooleanField(blank=True, default=False)

	left_rear_fender = models.BooleanField(blank=True, default=False)
	left_rear_wheel = models.BooleanField(blank=True, default=False)
	left_rear_door = models.BooleanField(blank=True, default=False)
	left_rear_lamp = models.BooleanField(blank=True, default=False)
	left_rear_window = models.BooleanField(blank=True, default=False)
	left_rear_door_window = models.BooleanField(blank=True, default=False)
	left_rear_viewmirror = models.BooleanField(blank=True, default=False)
	left_front_door_window = models.BooleanField(blank=True, default=False)
	left_front_door = models.BooleanField(blank=True, default=False)
	left_front_wheel = models.BooleanField(blank=True, default=False)
	left_front_fender = models.BooleanField(blank=True, default=False)	
	left_head_lamp = models.BooleanField(blank=True, default=False)

	rear_bumper = models.BooleanField(blank=True, default=False)
	boot_door = models.BooleanField(blank=True, default=False)
	rear_wind_screen = models.BooleanField(blank=True, default=False)
	car_top = models.BooleanField(blank=True, default=False)
	wind_screen = models.BooleanField(blank=True, default=False)
	hood = models.BooleanField(blank=True, default=False)
	grill = models.BooleanField(blank=True, default=False)
	front_bumper = models.BooleanField(blank=True, default=False)
	chasis = models.BooleanField(blank=True, default=False)
	suspension = models.BooleanField(blank=True, default=False)
	engine = models.BooleanField(blank=True, default=False)
	gear_box = models.BooleanField(blank=True, default=False)
	dashboard = models.BooleanField(blank=True, default=False)
	dashboard_controls = models.BooleanField(blank=True, default=False)
	sound_system = models.BooleanField(blank=True, default=False)	
	Steering = models.BooleanField(blank=True, default=False)
	left_front_seat = models.BooleanField(blank=True, default=False)
	rear_seat = models.BooleanField(blank=True, default=False)
	right_front_seat = models.BooleanField(blank=True, default=False)
	door_panels = models.BooleanField(blank=True, default=False)
	foot_pedals = models.BooleanField(blank=True, default=False)
	hand_brake = models.BooleanField(blank=True, default=False)
	capets = models.BooleanField(blank=True, default=False)
	ceiling = models.BooleanField(blank=True, default=False)
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_incidences')	
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modifed_incidences')
	history = HistoricalRecords()

	@property
	def insurance_claim_ref(self):
		return "%s-%s"%(self.vehicle, self.incident_date)


	def __unicode__(self):
		return self.insurance_claim_ref

#=========================================================================================================================
#Vehicle Insurance Models
#=========================================================================================================================

class InsuranceClaim(models.Model):

	vehicle = models.ForeignKey(Vehicle, null=False, blank=False, related_name='vehicle_insuranceClaims')
	driver = models.ForeignKey('employees.Employee', null=False, blank=False, related_name='driver_insuranceClaims')
	submission_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	claim_number = models.CharField(max_length=120, unique=True, null=False, blank=False)
	payout_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	payout_amount = models.FloatField(null=True, blank=True, max_length=20, default=0)
	sp_payout_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	sp_payout_amount = models.FloatField(null=True, blank=True, max_length=20, default=0)
	excess = models.FloatField(null=True, blank=True, max_length=20, default=0)	
	claim_status = models.CharField(max_length=200, default=None, null=True, blank=True,
							choices=(								
								('Pending', 'Claim Pending'),
								('Awaiting additional information from driver','Awaiting additional information from driver'),
								('Awaiting Assessors Report', 'Awaiting Assessors Report'),
								('Rejected', 'Rejected'),								
								('Finalized', 'Finalized')
							))	
	accept = models.BooleanField(blank=True, default=False)
	
	authorize = models.CharField(max_length=20, default='Pending', null=True, blank=True,
							choices=(
								('Pending', 'Pending'),							
								('Aproved', 'Authorize'),
								('Declined', 'Decline')
							))
	incidence_number = models.ForeignKey(Incident, null=True, blank=True, related_name='incidenceNumber_vehicleInsuranceClaims')	
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_insuranceClaims')	
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modifed_insuranceClaims')
	history = HistoricalRecords()


class Comment(models.Model):
	comments = models.CharField(max_length=2000, default=None, null=False, blank=False)
	commented = models.DateTimeField(auto_now_add=True)
	comment_type = models.CharField(max_length=120, default=None, null=False, blank=False)
	obj_id = models.IntegerField(null=True, blank=True,)
	vehicle = models.ForeignKey(Vehicle, null=False, blank=False, related_name='vehicle_comments')
	created_by = models.ForeignKey('accounts.ElopsysUser', null=False, blank=False, related_name='user_comments')



class Requisition(models.Model):
	quotation_1 = models.CharField(max_length=120, default=None, null=False, blank=False)
	quotation_2 = models.CharField(max_length=120, default=None, null=False, blank=False)	
	obj_id = models.IntegerField(null=True, blank=True,)
	requisition_type = models.CharField(max_length=120, default=None, null=False, blank=False)
	description = models.CharField(max_length=2000, default=None, null=True, blank=True)
	mortivation = models.CharField(max_length=2000, default=None, null=True, blank=True)
	vehicle = models.ForeignKey(Vehicle, null=False, blank=False, related_name='vehicle_requisitions')
	driver = models.ForeignKey('employees.Employee', null=False, blank=False, related_name='driver_requisitions')
	requested_by = models.ForeignKey('employees.Employee', null=False, blank=False, related_name='employee_requisitions')	
	requested = models.DateTimeField(auto_now_add=True)
	supplier = models.CharField(max_length=120, default=None, null=False, blank=False)
	amount = models.FloatField(null=True, blank=True, max_length=20, default=0)
	vat_included = models.BooleanField(blank=True, default=True)
	budgeted = models.BooleanField(blank=True, default=False)
	authorized = models.BooleanField(blank=True, default=False)
	authorized_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='authorizer_requisitions')
	finalized = models.BooleanField(blank=True, default=False)
	finalized_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='finalizer_requisitions')
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_requisitions')	
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modifed_requisitions')
	history = HistoricalRecords()

	def get_sub_total(self):
		sub_total = RequisitionItem.objects.filter(requisition_no=self).aggregate(sub_total=Sum('line_total'))["sub_total"]
		if sub_total:
			return sub_total
		else:
			return 0

	def get_total_tax(self):		
		VAT = self.vat_included
		if not VAT:						
			return 0.14*self.get_sub_total()
		else:
			return 0

	def get_total(self):
		return self.get_sub_total() + self.get_total_tax()


class RequisitionItem(models.Model):
	requisition_no = models.ForeignKey(Requisition, null=False, blank=False, related_name='requisition_requistionItems')
	item_code = models.CharField(max_length=200, default=None, null=True, blank=True)
	line_item = models.CharField(max_length=200, default=None, null=True, blank=True)
	qty = models.IntegerField(null=True, blank=True,)
	unit_price = models.FloatField(null=True, blank=True, max_length=20, default=0)
	line_total = models.FloatField(null=True, blank=True, max_length=20, default=0)
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_requisitionitems')	
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modifed_requisitionitems')
	history = HistoricalRecords()



