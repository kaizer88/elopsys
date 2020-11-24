from __future__ import unicode_literals

from django.db import models
from datetime import datetime, timedelta
from django.db.models import Count, Sum, Q
from simple_history.models import HistoricalRecords
from offices.models import *
from employees.models import *
from accounts.models import *
from fleet.models import *


# Create your models here.

class Region(models.Model):
	region = models.CharField(max_length=120, default=None, null=True, blank=True)
	prefix = models.CharField(max_length=2, default=None, null=True, blank=True)
	elipsys_region_id = models.IntegerField(null=True, blank=True)

	def __unicode__(self):
		return self.region


class Branch(models.Model):
	branch = models.CharField(max_length=120, default=None, null=True, blank=True)
	prefix = models.CharField(max_length=2, default=None, null=True, blank=True)
	region = models.ForeignKey(Region, null=True, blank=True)
	office_type = models.CharField(max_length=20, default=None, null=True, blank=True,
						choices=(
							('HQ', 'Head Office'),
							('RO', 'Regional Office'),
							('SO', 'Satelite Office')
						))
	email = models.CharField(max_length=120, default=None, null=True, blank=True)
	celphone = models.CharField(max_length=20, default=None, null=True, blank=True)
	telephone = models.CharField(max_length=20, default=None, null=True, blank=True)
	fax = models.CharField(max_length=20, default=None, null=True, blank=True)
	address = models.CharField(max_length=200, default=None, null=True, blank=True)
	street_address = models.CharField(max_length=200, default=None, null=True, blank=True)
	suburb = models.CharField(max_length=200, default=None, null=True, blank=True)
	city = models.CharField(max_length=200, default=None, null=True, blank=True)
	postal_code = models.CharField(max_length=20, default=None, null=True, blank=True)
	telephone = models.CharField(max_length=20, default=None, null=True, blank=True)
	telephone2 = models.CharField(max_length=20, default=None, null=True, blank=True)
	telephone3 = models.CharField(max_length=20, default=None, null=True, blank=True)
	telephone4 = models.CharField(max_length=20, default=None, null=True, blank=True)
	fax = models.CharField(max_length=20, default=None, null=True, blank=True)
	fax2 = models.CharField(max_length=20, default=None, null=True, blank=True)

	def __unicode__(self):
		return self.branch



# class RegionalOffice(models.Model):
# 	region = models.ForeignKey(Region, null=True, blank=True)
# 	branch = models.ForeignKey(Branch, null=True, blank=True)

class Floor(models.Model):
	floor = models.CharField(max_length=120, default=None, null=True, blank=True)
	branch = models.ForeignKey(Branch, null=True, blank=True, related_name='branch_floor')

	def __unicode__(self):
		return self.floor


class Section(models.Model):
	section_no = models.CharField(max_length=120, default=None, null=True, blank=True)
	description = models.CharField(max_length=120, default=None, null=True, blank=True)
	floor = models.ForeignKey(Floor, null=True, blank=True, related_name='floor_section')

	def __unicode__(self):
		return self.section_no +' '+ self.description

class Department(models.Model):
	department = models.CharField(max_length=120, default=None, null=True, blank=True)
	prefix = models.CharField(max_length=20, default=None, null=True, blank=True)

	def __unicode__(self):
		return self.department


class Document(models.Model):
	file_name = models.CharField(max_length=255, blank=True)
	file = models.FileField(upload_to='uploads/fleet')
	transaction_id = models.CharField(max_length=20, default=None, null=True, blank=True)
	transaction = models.CharField(max_length=50, default=None, null=True, blank=True)
	date_uploaded = models.DateTimeField(auto_now_add=True)


class ElectricityMeterNumber(models.Model):
	meter_number = models.CharField(max_length=120, null=True, blank=True)
	meter_type = models.CharField(max_length=20, default=None, null=True, blank=True, choices=(
																							('prepaid', 'Prepaid Electricity Meter'),
																							('account', 'Metered Electricity Bill'),
																						))
	service_provider = models.CharField(max_length=120, null=True, blank=True)
	branch = models.ForeignKey(Branch, null=True, blank=True, related_name='branch_electricitymeternumber')
	history = HistoricalRecords()
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_electricitymeternumber')
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_electrictymeternumber')
	def __unicode__(self):
		return self.meter_number


class ElectricityPurchase(models.Model):
	meter_number = models.ForeignKey(ElectricityMeterNumber, null=True, blank=True, related_name='meter_electricitypurchase')
	purchase_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	amount = models.FloatField(null=True, blank=True, max_length=20, default=0)
	token = models.CharField(max_length=120, null=True, blank=True)
	accept = models.BooleanField(blank=True, default=False)
	authorize = models.CharField(max_length=20, default='Pending', null=True, blank=True,
									choices=(
										('Pending', 'Pending'),
										('Aproved', 'Authorize'),
										('Declined', 'Decline')
									))
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_electricitypurchase')
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_electricitypurchase')
	history = HistoricalRecords()


class TelcomPABXContract(models.Model):
	branch = models.ForeignKey(Branch, null=True, blank=True, related_name='branch_telcomcontract')
	start_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	expiry_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	extensions = models.IntegerField()
	price = models.FloatField(null=True, blank=True, max_length=20, default=0)
	accept = models.BooleanField(blank=True, default=False)
	authorize = models.CharField(max_length=20, default='Pending', null=True, blank=True,
									choices=(
										('Pending', 'Pending'),
										('Aproved', 'Authorize'),
										('Declined', 'Decline')
									))
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_pabxcontract')
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_pabxcontract')
	history = HistoricalRecords()


class TelcomPABXContractRenewal(models.Model):
	branch = models.ForeignKey(Branch, null=True, blank=True, related_name='branch_telcomcontractrenewal')
	date_expired = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	start_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	expiry_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	extensions = models.IntegerField()
	price = models.FloatField(null=True, blank=True, max_length=20, default=0)
	accept = models.BooleanField(blank=True, default=False)
	authorize = models.CharField(max_length=20, default='Pending', null=True, blank=True,
									choices=(
										('Pending', 'Pending'),
										('Aproved', 'Authorize'),
										('Declined', 'Decline')
									))
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_pabxcontractrenewal')
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_pabxcontractrenewal')
	history = HistoricalRecords()


class MobilePurchase(models.Model):
	branch = models.ForeignKey(Branch, null=True, blank=True, related_name='branch_mobilepurchase')
	purchase_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	mobile_option = models.CharField(max_length=20, default='Pending', null=True, blank=True,
									choices=(
										('airtime', 'Airtime Purchase'),
										('data', 'Data Purchase'),
									))
	service_provider = models.CharField(max_length=120, null=True, blank=True,
								choices=(
										('cell_c', 'Cell C'),
										('mtn', 'MTN'),
										('telcom_mobile', 'Telcom Mobile'),
										('virgin_mobile', 'Virgin Mobile'),
										('vodacom', 'Vodacom'),
									))
	phone_number = models.CharField(max_length=120, null=True, blank=True)
	units = models.CharField(max_length=120, null=True, blank=True)
	price = models.FloatField(null=True, blank=True, max_length=20, default=0)
	accept = models.BooleanField(blank=True, default=False)
	authorize = models.CharField(max_length=20, default='Pending', null=True, blank=True,
									choices=(
										('Pending', 'Pending'),
										('Aproved', 'Authorize'),
										('Declined', 'Decline')
									))
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_mobilepurchase')
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_mobilepurchase')
	history = HistoricalRecords()

class MobileNumber(models.Model):
	phone_number = models.CharField(max_length=120,unique=True, null=False, blank=False)
	sim_number = models.CharField(max_length=120, null=True, blank=True)
	service_provider = models.CharField(max_length=120, null=True, blank=True,
								choices=(
										('cell_c', 'Cell C'),
										('mtn', 'MTN'),
										('telcom_mobile', 'Telcom Mobile'),
										('virgin_mobile', 'Virgin Mobile'),
										('vodacom', 'Vodacom'),
									))
	active = models.BooleanField(blank=True, default=False)
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_mobilenumber')
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_mobilenumber')
	history = HistoricalRecords()

	def __unicode__(self):
		return self.phone_number


class CardAllocation(models.Model):
	mobile_number = models.ForeignKey(MobileNumber, null=True, blank=True, related_name='phone_cardallocation')
	parckage = models.CharField(max_length=20, default='UC5GB', null=True, blank=True,
									choices=(
										('UC5GB', 'Unlimited Calls 5GB Data'),
										('UC10GB ', 'Unlimited Calls 10GB Data'),
									))
	fuel_card = models.ForeignKey('fleet.FuelCard', null=True, blank=True, related_name='fuelcard_cardallocation')
	fuel_cycle_limit = models.CharField(max_length=120, null=True, blank=True)
	allocation_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	allocation_type = models.CharField(max_length=50, default=None, null=True, blank=True,
						choices=(
							('Allocate Sim And Fuel Card', 'Allocate Sim And Fuel Card'),
							('Allocate Sim Card', 'Allocate Sim Card'),
							('Allocate Fuel Card', 'Allocate Fuel Card'),
							('Return Sim And Fuel Card', 'Return Sim And Fuel Card'),
							('Return Sim Card', 'Return Sim Card'),
							('Return Fuel Card', 'Return Fuel Card'),
						))
	accept = models.BooleanField(blank=True, default=False)
	authorize = models.CharField(max_length=20, default='Pending', null=True, blank=True,
									choices=(
										('Pending', 'Pending'),
										('Aproved', 'Authorize'),
										('Declined', 'Decline')
									))
	employee = models.ForeignKey('employees.Employee', null=True, blank=True, related_name='employee_cardallocation')
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_cardallocation')
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_cardallocation')
	history = HistoricalRecords()