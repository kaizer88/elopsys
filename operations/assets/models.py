# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from lib.models import BaseModel
from lib.fields import ProtectedForeignKey
from django.core.validators import MaxValueValidator, MinValueValidator
from simple_history.models import HistoricalRecords
from datetime import datetime
from datetime import timedelta
from django.db.models import Sum

# Create your models here.

class Asset(BaseModel):

    
    CATEGORY_ONE_LIST = (('appliances','Appliances'),('electronic_equipment','Electronic Equipment'),('furniture','Furniture'),
    					('it_equipment','IT Equipment'),('stationery','Stationery'))
    CATEGORY_TWO_LIST = ()
    CATEGORY_THREE_LIST = ()
    CONDITION_LIST = (('good','Good'),('new','New'),('poor','Poor'))
    STATUS_LIST = (('in_use','In Use'),('in_storage','In Storage'))

    category_one = models.CharField(max_length=50, null=True, blank=True, choices=CATEGORY_ONE_LIST, verbose_name='Category 1')
    category_two = models.CharField(max_length=50, null=True, blank=True, choices=CATEGORY_TWO_LIST, verbose_name='Category 2')
    category_three = models.CharField(max_length=50, null=True, blank=True, choices=CATEGORY_THREE_LIST, verbose_name='Category 3')
    
    asset_description = models.CharField(max_length=255, null=True, blank=True, verbose_name='Asset Description')
    make = models.CharField(max_length=255, null=True, blank=True)
    model = models.CharField(max_length=255, null=True, blank=True)
    serial_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='Serial Number')
    colour = models.CharField(max_length=255, null=True, blank=True)
    reason = models.CharField(max_length=255, null=True, blank=True)
    condition = models.CharField(max_length=50, null=True, blank=True, choices=CONDITION_LIST)
    status = models.CharField(max_length=50, null=True, blank=True, choices=STATUS_LIST)

    supplier_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Supplier Name')

    asset_detail = ProtectedForeignKey('AssetDetail', null=True, blank=True, related_name='asset_detail')
    asset_purchase_detail = ProtectedForeignKey('AssetPurchaseDetail', null=True, blank=True, related_name='asset_purchase_detail')
    contact_person = ProtectedForeignKey('operations.Contact', null=True, blank=True, related_name='asset_contact')
    address = ProtectedForeignKey('operations.Address', null=True, blank=True, related_name='asset_address')

    warranty_expiry = models.DateTimeField(null=True, blank=True, verbose_name='Warranty Expiry')

    created_by = ProtectedForeignKey('operations.OperationsUser', null=False, blank=False, related_name='created_asset')
    modified_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True, related_name='modified_asset')
    history = HistoricalRecords()


class AssetDetail(BaseModel):

    DEPARTMENT_LISTS = (('administration','Administration'),('client_services','Client Services'),('finance','Finance'),
                        ('human_resources','Human Resources'),('it','IT'),('marketing','Marketing'),('operations','Operations'),
                        ('sales','Sales'))

    quantity = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    user = models.CharField(max_length=255, null=True, blank=True)

    department = models.CharField(max_length=50, null=True, blank=True, choices=DEPARTMENT_LISTS)
    region = ProtectedForeignKey('operations.Region', null = True, blank = True, related_name='region_asset_detail')
    district = ProtectedForeignKey('operations.Branch', null = True, blank = True, related_name='district_asset_detail')
    created_by = ProtectedForeignKey('operations.OperationsUser', null=False, blank=False, related_name='created_asset_detail')
    modified_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True, related_name='modified_asset_detail')
    history = HistoricalRecords()

class AssetPurchaseDetail(BaseModel):

    invoice_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='Invoice Number')
    purchase_date = models.DateTimeField(null=True, blank=True, verbose_name='Purchase Date')
    asset_purchase_price = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='Purchase Price')
    vat = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='VAT')
    total_price = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='Total Price')

    created_by = ProtectedForeignKey('operations.OperationsUser', null=False, blank=False, related_name='created_purchase_detail_asset')
    modified_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True, related_name='modified_purchase_detail_asset')

    history = HistoricalRecords()

