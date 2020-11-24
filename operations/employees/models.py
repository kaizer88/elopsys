from __future__ import unicode_literals
from lib.models import BaseModel
from django.db import models
from datetime import datetime, timedelta
from operations.models import OperationsUser
from simple_history.models import HistoricalRecords
from lib.fields import ProtectedForeignKey
from fleet_management.models import VehicleDriver

class Employee(BaseModel):
	first_name = models.CharField(max_length=120, null=False, blank=False, verbose_name='First Name')
	last_name = models.CharField(max_length=120, null=False, blank=False, verbose_name='Last Name')
	employee_no = models.CharField(max_length=120, default=None, null=True, blank=True, verbose_name='Employee Number')
	commission_code = models.CharField(max_length=120, default=None, null=True, blank=True, verbose_name='Commission Code')
	id_number = models.CharField(max_length=120, null=False, blank=False, verbose_name='ID Number')
	
	email = models.CharField(max_length=120, default=None, null=True, blank=True, verbose_name='Email')

	role = models.CharField(max_length=20, null=True, blank=True,
							choices = (
									('RM', 'Regional Manager'),
									('RSM', 'Regoinal Sales Manager'),
									('PAM', 'Regional Admin Manager'),
									('BM', 'Branch Manager'),
									('DM', 'Junior District Manager'),
									('SM', 'Sales Manager'),
									('SADM', 'Executive Agent'),
									('ADM', 'Assistant District Manager'),
									('AG', 'Agent')))
	division = models.CharField(max_length=20, null=True, blank=True,
								choices = (
										('marketing', 'Marketing'),
										('sales', 'Sales'),
										('other', 'Other')))
	region = ProtectedForeignKey('operations.Region', null=True, blank=True,
								db_index=True, related_name='employees_in_region')
	imported = models.BooleanField(default=False)

	def __unicode__(self):
		return "{} {}".format(self.first_name, self.last_name)

	@property
	def full_name(self):
				return "{} {}".format(self.first_name, self.last_name)

	@property
	def driving_licence(self):
		return self.employee_driving_licence.filter(expiry_date__gt=datetime.now()).last()

	@property
	def vehicle(self):
		vehicle = self.driver_vehicle.filter(end_date__isnull=True).order_by('id').last()
		if vehicle:			
			return vehicle.vehicle
		else:
			return None


class DrivingLicence(BaseModel):

	LICENCE_CODE = (
		('A', 'A-Motor Cycle'),
		('A1', 'A1-Motor Cycle LTE 125cc'),
		('AA', 'AA-International Driving Permit'),
		('B', 'B-Light Motor Vehicle LTE 3500kg'),
		('EB', 'EB-Articulated vehicles LTE 3500kg'),
		('C1', 'C1-Minibuses, Buses and Goods vehicles LTE 16000kg'),
		('C', 'C-Buses and goods vehicles GTE 16000kg'),
		('EC1', 'EC1-Articulated vehicles LTE 16000kg'),
		('EC', 'EC-Articulated vehicles GTE 18000kg'))

	VEHICLE_RESTRICTIONS = (('no_restrictions','No Restrictions'),
				('automatic','Automatic transmission'),
				('electric', 'Electrically powered'),
				('physically_disabled', 'Physically disabled'),
				('bus', 'Bus GTE 16000kg (GVM) permited'))

	DRIVER_RESTRICTIONS = (('no_restrictions','No Restrictions'),
						   ('glasses','Glasses or Contact lenses'),
						   ('artificial_limb','Artificial limb'))
		
	employee = models.ForeignKey(Employee, null=True, blank=True,
									 related_name='employee_driving_licence')
	licence_number = models.CharField(max_length=120, null=False, blank=False)
	date_of_issue = models.DateField(null=True, blank=True, auto_now=False,
										 editable=True)
	expiry_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
		
	code = models.CharField(max_length=120, default='B', null=True, blank=True,
				choices=LICENCE_CODE)
		
	vehicle_restrictions = models.CharField(max_length=120, default='no_restrictions',
												null=True, blank=True,
												choices=VEHICLE_RESTRICTIONS)
	driver_restrictions = models.CharField(max_length=120, default='no_restrictions',
											   null=True, blank=True,
											   choices=DRIVER_RESTRICTIONS)
		
	date_added = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey('operations.OperationsUser', null=True, blank=True,
									   related_name='user_created_driving_licence') 
	modified_by = models.ForeignKey('operations.OperationsUser', null=True, blank=True,
										related_name='user_modified_driving_licence')

	licence_image = ProtectedForeignKey('operations.Document', null=True, blank=True,
											db_index=True)

		
	history = HistoricalRecords()

	
