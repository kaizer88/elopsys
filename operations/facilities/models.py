from django.db import models
from lib.models import BaseModel
from lib.fields import ProtectedForeignKey
from django.core.validators import MaxValueValidator, MinValueValidator
from simple_history.models import HistoricalRecords
from datetime import datetime
from django.db.models import Sum

class StockItem(BaseModel):
	STOCK_CATEGORIES = (('consumables', 'Consumables'),
						('sanitary', 'Sanitary'),
						('stationery', 'Stationery'))
	item_name = models.CharField(max_length=255, unique=True, null=False, blank=False, verbose_name="Item Name")
	category = models.CharField(max_length=255, null=False, blank=False, choices=STOCK_CATEGORIES)
	stock_quantity = models.IntegerField(null=True, blank=True, verbose_name='Stock Quantity',
										validators=[MinValueValidator(0)])
	created_by = ProtectedForeignKey('operations.OperationsUser', null=False, blank=False, related_name='created_stock_item')
	modified_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True, related_name='modified_stock_item')
	
	def __unicode__(self):
		return self.item_name


class StockTransaction(BaseModel):
	STOCK_TRANSACTION_TYPES = (('allocated','Allocated'),
							   ('received','Received'))

	stock_item = ProtectedForeignKey('StockItem', null=True, blank=True, related_name="stock_item_stock_recieved", verbose_name='Stock Item')
	reference = models.CharField(max_length=255, null=False, blank=False)
	transaction_type = models.CharField(max_length=255, null=False, blank=False, choices=STOCK_TRANSACTION_TYPES)
	opening_stock = models.IntegerField(null=True, blank=True, verbose_name='Opening Stock',
										validators=[MinValueValidator(0)])
	quantity = models.IntegerField(null=True, blank=True, verbose_name='Quantity',
										validators=[MinValueValidator(0)])
	transaction_date = models.DateTimeField(null=True, blank=True, verbose_name='Transaction Date')
	supplier = ProtectedForeignKey('operations.Vendor', null = True, blank = True, related_name='supplier_stock_received')
	district = ProtectedForeignKey('operations.Branch', null = True, blank = True, related_name='district_stock_allocation')
	comment = models.TextField(null=True, blank=True)
	created_by = ProtectedForeignKey('operations.OperationsUser', null=False, blank=False, related_name='created_stock_received')
	modified_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True, related_name='modified_stock_received')
	
	@property
	def stock_balance(self):
		if self.transaction_type == 'allocated':
			stock_bal = self.opening_stock - self.quantity
		else:
			stock_bal = self.opening_stock + self.quantity
		return stock_bal
