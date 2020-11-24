
# Create your models here.
from django.db import models
from django.db.models import Count, Sum, Q
from simple_history.models import HistoricalRecords
from offices.models import *
from employees.models import * 
from accounts.models import *



class STDocument(models.Model):
	branch = models.ForeignKey(Branch, null=False, blank=False, related_name='branch_stock_document')
	file_name = models.CharField(max_length=255, blank=True)
	file = models.FileField(upload_to='uploads/property')
	obj_id = models.CharField(max_length=20, default=None, null=True, blank=True)
	obj_type = models.CharField(max_length=50, default=None, null=True, blank=True)
	date_uploaded = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_stock_document')
	history = HistoricalRecords()

	def filename(self):
		return os.path.basename(self.file.name)


class STComment(models.Model):
	comments = models.CharField(max_length=2000, default=None, null=False, blank=False)
	commented = models.DateTimeField(auto_now_add=True)
	comment_type = models.CharField(max_length=120, default=None, null=True, blank=True)
	obj_id = models.IntegerField(null=True, blank=True,)
	branch = models.ForeignKey(Branch, null=True, blank=True, related_name='branch_stock_comments')
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_stock_comments')
	history = HistoricalRecords()


class STRequisition(models.Model):
	quote_number = models.CharField(max_length=120, default=None, null=False, blank=False)	
	obj_id = models.IntegerField(null=True, blank=True,)
	requisition_type = models.CharField(max_length=120, default=None, null=False, blank=False)
	description = models.CharField(max_length=2000, default=None, null=True, blank=True)
	branch = models.ForeignKey(Branch, null=False, blank=False, related_name='branches_stock_requisitions')
	requested_by = models.ForeignKey('employees.Employee', null=False, blank=False, related_name='employee_stock_requisitions')
	requested = models.DateTimeField(auto_now_add=True)
	supplier = models.CharField(max_length=120, default=None, null=False, blank=False)
	vat_included = models.BooleanField(blank=True, default=True)
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_stock_requisitions')	
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_stock_rerequisitions')
	history = HistoricalRecords()

	def get_sub_total(self):
		sub_total = STRequisitionItem.objects.filter(requisition_no=self).aggregate(sub_total=Sum('line_total'))["sub_total"]
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


class STRequisitionItem(models.Model):
	requisition_no = models.ForeignKey(STRequisition, null=False, blank=False, related_name='requisition_stock_requistionItems')
	item_code = models.CharField(max_length=200, default=None, null=True, blank=True)
	line_item = models.CharField(max_length=200, default=None, null=True, blank=True)
	qty = models.IntegerField(null=True, blank=True,)
	unit_price = models.FloatField(null=True, blank=True, max_length=20, default=0)
	line_total = models.FloatField(null=True, blank=True, max_length=20, default=0)
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_stock_requisitionitems')	
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_stock_rerequisitionitems')
	history = HistoricalRecords()



class StockItem(models.Model):
	item_name = models.CharField(max_length=200, default=None, null=True, blank=True)
	item_code = models.CharField(max_length=200, default=None, null=True, blank=True)
	category = models.CharField(max_length=20, default=None, null=True, blank=True,
									choices=(																							
										('grocery', 'Grocery'),
										('sanitation', 'Sanitation'),
										('stationary', 'Stationary'),
									))
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_stockitems')	
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_stockitems')
	history = HistoricalRecords()

	@property
	def item_description(self):
		return "%s-%s"%(self.item_code, self.item_name)

	def __unicode__(self):
		return self.item_description

class BranchStock(models.Model):
	branch = models.ForeignKey(Branch, null=False, blank=False, related_name='branch_branchstockitems')
	item = models.ForeignKey(StockItem, null=False, blank=False, related_name='item_branchstockitems')
	quantity = models.FloatField(null=True, blank=True, max_length=20, default=0)
	reorder_quantity = models.FloatField(null=True, blank=True, max_length=20, default=0)
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_branchstocktems')	
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_branchstocktems')
	history = HistoricalRecords()


class StockTake(models.Model):
	branch = models.ForeignKey(Branch, null=False, blank=False, related_name='branch_stocktakes')
	floor = models.ForeignKey(Floor, null=False, blank=False, related_name='floor_stocktakes')
	item = models.ForeignKey(StockItem, null=False, blank=False, related_name='item_stocktakes')
	quantity = models.FloatField(null=True, blank=True, max_length=20, default=0)
	checker  = models.ForeignKey('employees.Employee', null=False, blank=False, related_name='checker_stocktakes')
	date_checked = models.DateField(null=True, blank=True, auto_now=False, editable=True)	
	time_checked = models.TimeField(null=True, blank=True, auto_now=False, editable=True)
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_stocktakes')	
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_stocktakes')
	history = HistoricalRecords()


class StockReplenishment(models.Model):
	branch = models.ForeignKey(Branch, null=False, blank=False, related_name='branch_stockreplenishments')
	item = models.ForeignKey(StockItem, null=False, blank=False, related_name='item_stockreplenishmennts')
	quantity = models.FloatField(null=True, blank=True, max_length=20, default=0)
	replenisher  = models.ForeignKey('employees.Employee', null=False, blank=False, related_name='checker_stockreplenishments')
	date_replenished = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_stockreplenishments')	
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_stockreplenishments')
	history = HistoricalRecords()


class Book(models.Model):
	book_type = models.CharField(max_length=120, null=True, blank=True)
	written_by = models.CharField(max_length=20,default=None, null=True, blank=True,
									choices=(																							
										('sales', 'Sales Department'),
										('marketing', 'Marketing Departrment')
								))
	quantity = models.FloatField(null=True, blank=True, max_length=20, default=0)
	def __unicode__(self):
		return self.book_type

class BookReplenishment(models.Model):
	book = models.ForeignKey(Book, null=False, blank=False, related_name='book_bookreplenishment')
	range_from = models.CharField(max_length=120, default='Operational', null=True, blank=True,)
	range_to = models.CharField(max_length=120, default='Operational', null=True, blank=True,)
	in_stock = models.FloatField(null=True, blank=True, max_length=20, default=0)
	quantity = models.FloatField(null=True, blank=True, max_length=20, default=0)
	date_ordered = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	date_recieved = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	recieved = models.BooleanField(blank=True, default=False)
	accept = models.BooleanField(blank=True, default=False)	
	authorize = models.CharField(max_length=20, default='Pending', null=True, blank=True,
									choices=(	
										('Pending', 'Pending'),													
										('Aproved', 'Authorize'),
										('Declined', 'Decline')
									))
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_bookreplenishment')	
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_bookreplenishment')
	history = HistoricalRecords()


class BookAllocation(models.Model):
	book = models.ForeignKey(Book, null=False, blank=False, related_name='book_bookallocations')
	range_from = models.CharField(max_length=120, null=True, blank=True,)
	range_to = models.CharField(max_length=120, null=True, blank=True,)
	quantity = models.FloatField(null=True, blank=True, max_length=20, default=0)	
	regional_admin_manager = models.ForeignKey('employees.Employee', null=False, blank=False, related_name='ram_bookallocations')
	region = models.ForeignKey(Region, null=False, blank=False, related_name='region_bookallocations')
	date_allocated = models.DateField(null=True, blank=True, auto_now=False, editable=True)
	accept = models.BooleanField(blank=True, default=False)	
	authorize = models.CharField(max_length=20, default='Pending', null=True, blank=True,
									choices=(	
										('Pending', 'Pending'),													
										('Aproved', 'Authorize'),
										('Declined', 'Decline')
									))
	created_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_bookallocations')	
	modified_by = models.ForeignKey('accounts.ElopsysUser', null=True, blank=True, related_name='user_modified_bookallocations')
	history = HistoricalRecords()





		