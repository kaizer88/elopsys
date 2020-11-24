
# Create your models here.
from django.db import models
from django.db.models import Count, Sum, Q
from simple_history.models import HistoricalRecords
from offices.models import *
from employees.models import * 
from accounts.models import *
# Create your models here.

class LeaseAgreement(models.Model):
	branch = models.ForeignKey(Branch, null=False, blank=False, related_name='branch_leaseagreements')
	office_space = models.CharField(max_length=200, default=None, null=True, blank=True,)
	rental_amount = models.FloatField(null=True, blank=True, max_length=20, default=0)
	surety = models.BooleanField(blank=True, default=False)	
	deposit = models.FloatField(null=True, blank=True, max_length=20, default=0)
	surety_deposit = models.FloatField(null=True, blank=True, max_length=20, default=0)
	electricity_deposit = models.FloatField(null=True, blank=True, max_length=20, default=0)
	electricity = models.CharField(max_length=200, default=None, null=True, blank=True,
									  choices=(								
												('Eskom', 'Eskom'),
												('Pre-Paid', 'Pre-Paid'),
												('PEC', 'PEC Metering'),
												('Municipal', 'Municipal')
											))
	current_leasee = models.CharField(max_length=200, default=None, null=True, blank=True)
	leasor = models.CharField(max_length=200, default='Pending', null=True, blank=True)
	lease_expiry_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	notice_term = models.CharField(max_length=200, default=None, null=True, blank=True)
	contact_person = models.CharField(max_length=200, default=None, null=True, blank=True)
	status = models.CharField(max_length=20, default='Operational', null=True, blank=True,
									choices=(	
										('Operational', 'Operational'),													
										('Pending Closure', 'Pending Closure'),
										('Closed', 'Closed')
									))
	exit_clause_sent = models.BooleanField(blank=True, default=False)	
	accept = models.BooleanField(blank=True, default=False)	
	authorize = models.CharField(max_length=20, default='Pending', null=True, blank=True,
									choices=(	
										('Pending', 'Pending'),													
										('Aproved', 'Authorize'),
										('Declined', 'Decline')
									))
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_leaseagreements')	
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_leaseagreements')
	history = HistoricalRecords()


class PFDocument(models.Model):
	branch = models.ForeignKey(Branch, null=True, blank=True, related_name='branch_propfac_documents')
	file_name = models.CharField(max_length=255, blank=True)
	file = models.FileField(upload_to='uploads/property')
	obj_id = models.CharField(max_length=20, default=None, null=True, blank=True)
	obj_type = models.CharField(max_length=50, default=None, null=True, blank=True)
	date_uploaded = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_pfdocuments')
	history = HistoricalRecords()

	def filename(self):
		return os.path.basename(self.file.name)



class LeaseAgreementRenewal(models.Model):
	branch = models.ForeignKey(Branch, null=False, blank=False, related_name='branch_leaseagreement_renewals')	
	expiry_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	renewal_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	rental_amount = models.FloatField(null=True, blank=True, max_length=20, default=0)
	new_expiry_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	accept = models.BooleanField(blank=True, default=False)	
	authorize = models.CharField(max_length=20, default='Pending', null=True, blank=True,
									choices=(	
										('Pending', 'Pending'),													
										('Aproved', 'Authorize'),
										('Declined', 'Decline')
									))
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_leaseagreementrenewals')	
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_leaseagreementrenewals')
	history = HistoricalRecords()
	


class PropertyMaintenance(models.Model):
	maint_date = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	branch = models.ForeignKey(Branch, null=False, blank=False, related_name='branch_building_maintenance')
	maintenance_type = models.CharField(max_length=20, default=None, null=True, blank=True,
									choices=(
										('General', 'General'),			
										('Air Conditioning', 'Air Conditioning'),
										('Electrical', 'Elecriical'),
										('Floor Capets and Tiling', 'Floor Capets and Tiling'),																					
										('Plumbing', 'Plumbing'),										
										('Security', 'Security'),
										('Walls And Partitioning', 'Walls And Partitioning'),
										
									))
	description = models.CharField(max_length=2000, default=None, null=True, blank=True)
	projected_cost = models.FloatField(null=True, blank=True, max_length=20, default=0)
	actual_cost = models.FloatField(null=True, blank=True, max_length=20, default=0)	
	difference = models.FloatField(null=True, blank=True, max_length=20, default=0)	
	invoice_number = models.CharField(max_length=200, default=None, null=True, blank=True)
	service_provider = models.CharField(max_length=200, default=None, null=True, blank=True)
	status = models.CharField(max_length=20, default=None, null=True, blank=True,
							choices=(
								('Good Condition', 'Good Condition'),
								('Minor Damages', 'Minor Damages'),
								('Major Damages', 'Major Damages'),
								('Write Off', 'Write Off')
							))		
	
	accept = models.BooleanField(blank=True, default=False)	
	authorize = models.CharField(max_length=20, default='Pending', null=True, blank=True,
							choices=(							
								('Pending', 'Pending'),
								('Aproved', 'Authorize'),
								('Declined', 'Decline')
							))
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_propertymaintenance')	
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_propertymaintenance')
	history = HistoricalRecords()


class OfficeInspection(models.Model):
	branch = models.ForeignKey(Branch, null=False, blank=False, related_name='branch_propfac_inspections')
	floor = models.ForeignKey(Floor, null=False, blank=False, related_name='floor_propfac_inspections')
	section = models.ForeignKey(Section, null=False, blank=False, related_name='section_propfac_inspections')
	date_checked = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	time_checked = models.TimeField(null=True, blank=True, auto_now=False, editable=True)
	inspector  = models.ForeignKey('employees.Employee', null=False, blank=False, related_name='inspector_propfac_inspections')	
	walls_and_covering = models.BooleanField(blank=True, default=False)
	windows_and_handles = models.BooleanField(blank=True, default=False)
	blinds = models.BooleanField(blank=True, default=False)
	ceiling = models.BooleanField(blank=True, default=False)
	lights_and_switches = models.BooleanField(blank=True, default=False)
	doors_and_handles = models.BooleanField(blank=True, default=False)
	air_conditioner = models.BooleanField(blank=True, default=False)
	furniture = models.BooleanField(blank=True, default=False)
	fire_extinguisher = models.BooleanField(blank=True, default=False)
	white_board = models.BooleanField(blank=True, default=False)
	overhead_projector = models.BooleanField(blank=True, default=False)
	appliances = models.BooleanField(blank=True, default=False)
	shelving = models.BooleanField(blank=True, default=False)
	status = models.CharField(max_length=20, default=None, null=True, blank=True,
							choices=(
								('Good Condition', 'Good Condition'),
								('Minor Damages', 'Minor Damages'),
								('Major Damages', 'Major Damages')								
							))		
	accept = models.BooleanField(blank=True, default=False)	
	authorize = models.CharField(max_length=20, default='Pending', null=True, blank=True,
							choices=(							
								('Pending', 'Pending'),
								('Aproved', 'Authorize'),
								('Declined', 'Decline')
							))
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_officeinspections')	
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_officeinspections')
	history = HistoricalRecords()


class ToiletInspection(models.Model):
	branch = models.ForeignKey(Branch, null=False, blank=False, related_name='branch_propfac_toilet_inspection')
	floor = models.ForeignKey(Floor, null=False, blank=False, related_name='floor_propfac_toilet_inspection')	
	toilet = models.CharField(max_length=20, default=None, null=True, blank=True,
							choices=(
								('gents', 'Gents'),
								('ladies', 'Ladies'),															
							))
	date_checked = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	time_checked = models.TimeField(null=True, blank=True, auto_now=False, editable=True)
	inspector  = models.ForeignKey('employees.Employee', null=False, blank=False, related_name='inspector_propfac_toilet_inspection')
	
	walls_and_covering = models.BooleanField(blank=True, default=False)
	windows_and_handles = models.BooleanField(blank=True, default=False)	
	ceiling = models.BooleanField(blank=True, default=False)
	lights_and_switches = models.BooleanField(blank=True, default=False)
	doors_and_hanles = models.BooleanField(blank=True, default=False)	
	air_extractor = models.BooleanField(blank=True, default=False)
	seat_and_cover = models.BooleanField(blank=True, default=False)
	urinary = models.BooleanField(blank=True, default=False)
	water_dispenser = models.BooleanField(blank=True, default=False)
	washing_basin = models.BooleanField(blank=True, default=False)
	taps = models.BooleanField(blank=True, default=False)
	towel_dispencer = models.BooleanField(blank=True, default=False)
	detegent_dispencer = models.BooleanField(blank=True, default=False)
	mirror = models.BooleanField(blank=True, default=False)
	furniture = models.BooleanField(blank=True, default=False)
	fire_extinguisher = models.BooleanField(blank=True, default=False)	
	shelving = models.BooleanField(blank=True, default=False)
	status = models.CharField(max_length=20, default=None, null=True, blank=True,
							choices=(
								('Good Condition', 'Good Condition'),
								('Minor Damages', 'Minor Damages'),
								('Major Damages', 'Major Damages')								
							))		
	accept = models.BooleanField(blank=True, default=False)	
	authorize = models.CharField(max_length=20, default='Pending', null=True, blank=True,
							choices=(							
								('Pending', 'Pending'),
								('Aproved', 'Authorize'),
								('Declined', 'Decline')
							))
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_toiletinspections')	
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_toiletinspections')
	history = HistoricalRecords()


class PFComment(models.Model):
	comments = models.CharField(max_length=2000, default=None, null=False, blank=False)
	commented = models.DateTimeField(auto_now_add=True)
	comment_type = models.CharField(max_length=120, default=None, null=True, blank=True)
	obj_id = models.IntegerField(null=True, blank=True,)
	branch = models.ForeignKey(Branch, null=True, blank=True, related_name='branch_propfac_comments')
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_propfac_comments')
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_propfac_comments')
	history = HistoricalRecords()


class PFRequisition(models.Model):
	quotation_1 = models.CharField(max_length=120, default=None, null=False, blank=False)
	quotation_2 = models.CharField(max_length=120, default=None, null=False, blank=False)	
	obj_id = models.IntegerField(null=True, blank=True,)
	requisition_type = models.CharField(max_length=120, default=None, null=False, blank=False)
	description = models.CharField(max_length=2000, default=None, null=True, blank=True)
	mortivation = models.CharField(max_length=2000, default=None, null=True, blank=True)
	branch = models.ForeignKey(Branch, null=False, blank=False, related_name='branches_propfac_requisitions')
	requested_by = models.ForeignKey('employees.Employee', null=False, blank=False, related_name='employee_propfac_requisitions')
	requested = models.DateTimeField(auto_now_add=True)
	supplier = models.CharField(max_length=120, default=None, null=False, blank=False)
	amount = models.FloatField(null=True, blank=True, max_length=20, default=0)
	vat_included = models.BooleanField(blank=True, default=True)
	budgeted = models.BooleanField(blank=True, default=False)
	authorized = models.BooleanField(blank=True, default=False)
	authorized_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='authorizer_propfac_requisitions')
	finalized = models.BooleanField(blank=True, default=False)
	finalized_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='finalizer_propfac_requisitions')
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_pfrequisitions')	
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_pfrequisitions')
	history = HistoricalRecords()

	def get_sub_total(self):
		sub_total = PFRequisitionItem.objects.filter(requisition_no=self).aggregate(sub_total=Sum('line_total'))["sub_total"]
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


class PFRequisitionItem(models.Model):
	requisition_no = models.ForeignKey(PFRequisition, null=False, blank=False, related_name='requisition_requistionItems')
	item_code = models.CharField(max_length=200, default=None, null=True, blank=True)
	line_item = models.CharField(max_length=200, default=None, null=True, blank=True)
	qty = models.IntegerField(null=True, blank=True,)
	unit_price = models.FloatField(null=True, blank=True, max_length=20, default=0)
	line_total = models.FloatField(null=True, blank=True, max_length=20, default=0)
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_pfrequisitionitems')	
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_pfrequisitionitems')
	history = HistoricalRecords()

