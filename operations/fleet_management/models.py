from django.db import models
from lib.models import BaseModel
from lib.fields import ProtectedForeignKey
from django.core.validators import MaxValueValidator, MinValueValidator
from simple_history.models import HistoricalRecords
from datetime import datetime
from datetime import timedelta
from django.db.models import Sum
from django.conf import settings

class VehicleMake(BaseModel):
    make_name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    def __unicode__(self):
        return self.make_name

class VehicleModel(BaseModel):
    make = ProtectedForeignKey('VehicleMake', null=False, blank=False, related_name="model_make")
    model_name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    def __unicode__(self):
        return self.model_name

class VehicleStatusType(BaseModel):
    
    description = models.CharField(max_length=250, null=True,blank=True)

    def __str__(self):
        return "{0}".format(self.description)

class Vehicle(BaseModel):

    OWNERSHIP_TYPES = (('emerald','Emerald'),('private','Private'),('rental','Rental'))
    DIVISION_TYPES = (('all','All'),('marketing','Marketing'),('sales','Sales'))
    STATUS_AT_CREATE_TYPES = (('new','New'),('used','Used'))
    TRANSMISSION_TYPES = (('automatic','Automatic'),('manual','Manual'))
    FUEL_TYPES = (('diesel','Diesel'),('petrol','Petrol'))
    DEPOSIT_PAID = (('emerald','Emerald'),('driver','Driver'))

    ownership = models.CharField(max_length=50, null=False, blank=False,
                                 choices=OWNERSHIP_TYPES)
    division = models.CharField(max_length=120, null=False, blank=False,
                                choices=DIVISION_TYPES)
    status_at_create = models.CharField(max_length=50, null=True, blank=True, verbose_name='Status at Create', choices=STATUS_AT_CREATE_TYPES)
    vehicle_make = ProtectedForeignKey('VehicleMake', null=True, blank=True, related_name="vehicle_make", verbose_name='Make')
    make = models.CharField(max_length=255, null=True, blank=True)
    vehicle_model = ProtectedForeignKey('VehicleModel', null=True, blank=True, related_name="vehicle_model", verbose_name='Model')
    model = models.CharField(max_length=255, null=True, blank=True)
    year_model = models.IntegerField(null=True, blank=True, verbose_name='Year Model')

    registration_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='Registration Number')
    registration_date = models.DateTimeField(null=True, blank=True, verbose_name='Registration Date')
    licence_disk_expiry = models.DateTimeField(null=True, blank=True, verbose_name='License Disk Expiry')

    vin_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='Vin Number')
    engine_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='Engine Number')
    colour = models.CharField(max_length=255, null=True, blank=True)

    transmission = models.CharField(max_length=50, null=True, blank=True, choices=TRANSMISSION_TYPES)
    fuel_type = models.CharField(max_length=120, null=True, blank=True, verbose_name='Fuel Type',
                                 choices=FUEL_TYPES)
    engine_capacity = models.IntegerField(null=True, blank=True, verbose_name='Engine Capacity',
                                        validators=[MinValueValidator(0)])
    tank_capacity = models.IntegerField(null=True, blank=True, verbose_name='Tank Capacity',
                                        validators=[MinValueValidator(0)])
    delivery_mileage = models.IntegerField(null=True, blank=True, verbose_name='Delivery Mileage',
                                          validators=[MinValueValidator(0)])
    service_interval = models.IntegerField(null=True, blank=True, default=0,
                                          validators=[MinValueValidator(0)],
                                          verbose_name='Service Interval')

    has_aircon = models.NullBooleanField(verbose_name='Aircon')
    has_radio = models.NullBooleanField(verbose_name='Radio')
    has_bluetooth = models.NullBooleanField(verbose_name='Bluetooth')
    has_jack = models.NullBooleanField(verbose_name='Jack')
    has_spanner = models.NullBooleanField(verbose_name='Spanner')
    has_triangle = models.NullBooleanField(verbose_name='Triangle')
    rental_company = models.CharField(max_length=255, null=True, blank=True, verbose_name='Rental Company')
    rental_contact_person = models.CharField(max_length=255, null=True, blank=True, verbose_name='Rental Company Contact Person')
    delivery_date = models.DateTimeField(null=True, blank=True, verbose_name='Date Accepted')
    delivery_location = models.CharField(max_length=255, null=True, blank=True, verbose_name='Accepted Location')
    delivery_odometer_mileage = models.IntegerField(null=True, blank=True, verbose_name='Accepted Odometer Mileage',
                                        validators=[MinValueValidator(0)])
    returned_date = models.DateTimeField(null=True, blank=True, verbose_name='Date Returned')
    returned_location = models.CharField(max_length=255, null=True, blank=True, verbose_name='Return Location')
    returned_mileage = models.IntegerField(null=True, blank=True, verbose_name='Returned Odometer Mileage',
                                        validators=[MinValueValidator(0)])
    vehicle_class = models.CharField(max_length=255, null=True, blank=True, verbose_name='Vehicle Class')
    rental_reason = models.CharField(max_length=255, null=True, blank=True, verbose_name='Reason For Rental')
    rental_deposit_amount = models.IntegerField(null=True, blank=True, verbose_name='Rental Deposit Amount',
                                          validators=[MinValueValidator(0)])
    deposit_paid_by = models.CharField(max_length=50, null=True, blank=True, choices=DEPOSIT_PAID)
    deposit_driver = ProtectedForeignKey('employees.Employee', null=True, blank=True, related_name='driver_deposit')
    deposit_paid_date = models.DateTimeField(null=True, blank=True, verbose_name='Date Deposit Paid')
    region = ProtectedForeignKey('operations.Region', null = True, blank = True, related_name='vehicle_region')
    district = ProtectedForeignKey('operations.Branch', null = True, blank = True, related_name='vehicle_district')
    service_area = models.CharField(max_length=25, null=True, blank=True, verbose_name='Service Area')
    updated_mileage = models.IntegerField(null=True, blank=True, verbose_name='Updated Odometer Mileage',
                                        validators=[MinValueValidator(0)])
    updated_date = models.DateTimeField(null=True, blank=True, verbose_name='Odometer Updated Date')
    status = models.ForeignKey(VehicleStatusType, null=True, blank=True,db_index=True)

    created_by = ProtectedForeignKey('operations.OperationsUser', null=False, blank=False, related_name='created_vehicles')
    modified_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True, related_name='modified_vehicles')

    history = HistoricalRecords()

    @property
    def driver(self):
        try:
            return self.vehicle_driver.get(end_date__isnull=True).driver
        except VehicleDriver.DoesNotExist:
            return None

    @property
    def current_vehicle_driver(self):
        try:
            return self.vehicle_driver.get(end_date__isnull=True)
        except VehicleDriver.DoesNotExist:
            return None

    @property
    def authorization_status(self):
        try:
            temp = self.vehicle_driver.get(end_date__isnull=True)
            return temp.status
        except VehicleDriver.DoesNotExist:
            return None

    @property
    def current_fuel_card(self):
        try:
            fuel_cards =  self.vehicle_fuelcard.filter(cancelled_date__isnull=True)
            cfc = fuel_cards.last()
            return cfc
        except FuelCard.DoesNotExist:
            return None

    def __unicode__(self):
            return self.registration_number

class VehicleTyre(BaseModel):
    vehicle = ProtectedForeignKey('Vehicle', null=False, blank=False, related_name="tyres")
    make = models.CharField(max_length=255, null=False, blank=False, verbose_name='Make')
    size = models.CharField(max_length=255, null=False, blank=False, verbose_name='Size')
    position = models.CharField(max_length=50, null=False, blank=False, verbose_name='Position',
                                choices=(('fr','Front Right'),('fl','Front Left'),
                                         ('rr','Rear Right'),('rl','Rear Left'),
                                         ('spare','Spare')))
    serial_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='Serial Number')

    mileage_at_replacement = models.IntegerField(null=True, blank=True, verbose_name='Mileage At Replacement',
                                          validators=[MinValueValidator(0)])

    in_use = models.BooleanField(default=False)

    created_by = ProtectedForeignKey('operations.OperationsUser', null=False, blank=False, related_name='created_tyres')
    modified_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True, related_name='modified_tyres')
    history = HistoricalRecords()


class PurchaseDetail(BaseModel):

    PURCHASE_TYPES = (('cash','Cash'),('hp','HP - Hire Purchase'),
                      ('lease','Lease'))

    vehicle = ProtectedForeignKey('Vehicle', null=False, blank=False, related_name='purchase_detail')

    vendor = ProtectedForeignKey('operations.Vendor', null = True, blank = True, related_name='purchase_details_dealer')

    invoice_number = models.CharField(max_length=255, null=False, blank=False, verbose_name='Invoice Number')

    purchase_amount = models.IntegerField(null=False, blank=False, verbose_name='Purchase Amount',
                                          validators=[MinValueValidator(0)])
    purchase_date = models.DateTimeField(null=True, blank=True, verbose_name='Purchase Date')
    purchase_type = models.CharField(max_length=50, null=False, blank=False, verbose_name='Purchase Type',
                                     choices=PURCHASE_TYPES)


    created_by = ProtectedForeignKey('operations.OperationsUser', null=False, blank=False, related_name='created_purchase_detail')
    modified_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True, related_name='modified_purchase_detail')
    history = HistoricalRecords()

class FinanceDetail(BaseModel):
    purchase_detail = ProtectedForeignKey('PurchaseDetail', null=False, blank=False, related_name='finance_detail')
    financier = models.CharField(max_length=255, null=True, blank=True)

    contract_number = models.CharField(max_length=255, null=False, blank=False, verbose_name='Contract Number')
    contract_term_months = models.IntegerField(null=True, blank=True, verbose_name='Contract Term Months',
                                               validators=[MinValueValidator(0)])

    deposit = models.IntegerField(null=False, blank=False, default=0,
                                  validators=[MinValueValidator(0)])
    installment = models.IntegerField(null=False, blank=False, default=0,
                                      validators=[MinValueValidator(0)])
    settlement_amount = models.IntegerField(null=True, blank=True, default=0, verbose_name='Settlement Amount',
                                            validators=[MinValueValidator(0)])
    settlement_amount_date = models.DateTimeField(null=True, blank=True, verbose_name='Settlement Amount Date')


    created_by = ProtectedForeignKey('operations.OperationsUser', null=False, blank=False, related_name='created_finance_detail')
    modified_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True, related_name='modified_finance_detail')
    history = HistoricalRecords()


class VehicleMaintenance(BaseModel):

    vehicle = ProtectedForeignKey('Vehicle', null=False, blank=False, related_name='maintenance_plan')
    end_date = models.DateTimeField(null=True, blank=True, verbose_name='End Date')
    end_mileage = models.IntegerField(null=True, blank=True, default=0,
                                      validators=[MinValueValidator(0)], verbose_name='End Mileage')
    service_interval = models.IntegerField(null=True, blank=True, default = 0, verbose_name='Service Interval')

    created_by = ProtectedForeignKey('operations.OperationsUser', null=False, blank=False, related_name='created_vehicle_maintenance')
    modified_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True, related_name='modified_vehicle_maintenance')
    history = HistoricalRecords()

    @property
    def registration_number(self):
        try:
            return self.registration_number.get(end_date__isnull=True).registration_number
        except Vehicle.DoesNotExist:
            return None

class Insurance(BaseModel):

    COVER_TYPES = (('insurance','Insurance'),
                   ('shortfall','Shortfall Cover'))

    vehicle = ProtectedForeignKey('Vehicle', null=False, blank=False, related_name='insurance')
    broker_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Broker Name')
    broker_contact_person = ProtectedForeignKey('operations.Contact', null=True,
                                                blank=True, related_name='insurance_broker_contact')
    broker_address = ProtectedForeignKey('operations.Address', null=True, blank=True,
                                         related_name='insurance_broker_address')

    insurance_type = models.CharField(max_length=255, null=False, blank=False, verbose_name='Insurance Type',choices=COVER_TYPES)

    insured_amount = models.IntegerField(null=False, blank=False, default=0, verbose_name='Insured Amount',
                                            validators=[MinValueValidator(0)])

    installment = models.IntegerField(null=False, blank=False, default=0,
                                      validators=[MinValueValidator(0)])

    vendor = ProtectedForeignKey('operations.Vendor', null = True, blank = True, related_name='insurance_insurer')

    created_by = ProtectedForeignKey('operations.OperationsUser', null=False, blank=False, related_name='created_insurance')
    modified_by = ProtectedForeignKey('operations.OperationsUser', null=False, blank=False, related_name='modified_insurance')
    history = HistoricalRecords()


class Tracker(BaseModel):

    INSTALLATION_TYPES = (('new','New'),('reinstall','Re-Install'))

    vehicle = ProtectedForeignKey('Vehicle', null=False, blank=False, related_name='tracker')

    installation_type = models.CharField(max_length=255, null=True, blank=True, verbose_name='Installation Type',
                                         choices=INSTALLATION_TYPES)
    installation_date = models.DateTimeField(null=True, blank=True, verbose_name='Installation Date')

    vendor = ProtectedForeignKey('operations.Vendor', null = True, blank = True, related_name='Tracker_tracker')

    contract_term_months = models.IntegerField(null=True, blank=True, verbose_name='Contract Term Months',
                                               validators=[MinValueValidator(0)])
    deposit = models.IntegerField(null=False, blank=False, default=0,
                                  validators=[MinValueValidator(0)])
    installment = models.IntegerField(null=False, blank=False, default=0,
                                      validators=[MinValueValidator(0)])
    settlement_amount = models.IntegerField(null=False, blank=False, default=0, verbose_name='Settlement Amount',
                                            validators=[MinValueValidator(0)])
    settlement_amount_date = models.DateTimeField(null=True, blank=True, verbose_name='Settlement Amount Date')
    previous_vehicle_reg_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='Unit Serial Number')
    active = models.BooleanField(default=False)
    tracking_source = models.CharField(null=False, blank=False, max_length=15, default='None')

class Branding(BaseModel):
    vehicle = ProtectedForeignKey('Vehicle', null=False, blank=False, related_name='branding')

    supplier = ProtectedForeignKey('operations.Vendor', null = True, blank = True, related_name='branding_supplier')
    installer = ProtectedForeignKey('operations.Vendor', null = True, blank = True, related_name='branding_installer')

    installation_date = models.DateTimeField(null=True, blank=True, verbose_name='Installation Date')

    created_by = ProtectedForeignKey('operations.OperationsUser', null=False, blank=False, related_name='created_trackers')
    modified_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True, related_name='modified_trackers')
    history = HistoricalRecords()

class VehicleDocument(BaseModel):

    DOCUMENT_TYPES = (('contract','Contract'),
                      ('invoice','Invoice'),
                      ('lease','Lease Agreement'),
                      ('natis','Natis Document'),
                      ('quotation','Quotation'),
                      ('other', 'Other'))

    vehicle = ProtectedForeignKey('Vehicle', null=False, blank=False, related_name='documents')
    document = ProtectedForeignKey('operations.Document', null=False, blank=False)
    document_type = models.CharField(max_length=255, null=False, blank=False, choices=DOCUMENT_TYPES)
    created_by = ProtectedForeignKey('operations.OperationsUser', null=False, blank=False, related_name='created_documents')
    modified_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True, related_name='modified_documents')

class VehicleDriver(BaseModel):

    REASONS = (('discretionary change','Discretionary Vehicle Change'),
               ('new employee','New Employee'),
               ('pool car','Pool Car'),
               ('relocation','Relocation'),
               ('temp vehicle','Temp Vehicle'))

    UNASSIGN_REASONS = (('adsconded', 'Absconded'),
                        ('discretionary change','Discretionary Vehicle Change'),
                        ('dismissed','Dismissal'),
                        ('long term repair','Long-term Maintenance/Repairs'),
                        ('relocation','Relocation'),
                        ('resignation','Resignation'),
                        ('suspend','Suspension'),
                        ('temp vehicle','Temp Vehicle'),
                        ('insurance pending','Insurance Claim - Pending'),
                        ('insurance repairs','Insurance Claim - Repairs'))

    vehicle = ProtectedForeignKey('Vehicle', null=False, blank=False, related_name='vehicle_driver')
    driver = ProtectedForeignKey('employees.Employee', null=False, blank=False, related_name='driver_vehicle')
    start_date = models.DateTimeField(null=False, blank=False, verbose_name='Start Date')
    end_date = models.DateTimeField(null=True, blank=True, verbose_name='End Date')
    reason = models.CharField(max_length=255, null=False, blank=False)
    status = models.CharField(max_length=255, null=True, blank=True)
    unassign_reason = models.CharField(max_length=255, null=True, blank=True)
    created_by = ProtectedForeignKey('operations.OperationsUser', null=False, blank=False, related_name='created_vehicle_drivers')
    modified_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True, related_name='modified_vehicle_drivers')
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        curr_vehicle_driver = self.vehicle.current_vehicle_driver

        if curr_vehicle_driver:
            curr_vehicle_driver.end_date = self.start_date
            curr_vehicle_driver.modified_by_id = self.created_by_id
            super(VehicleDriver, curr_vehicle_driver).save(*args, **kwargs)

        new_vehicle_driver = self
        super(VehicleDriver, self).save(*args, **kwargs)

        return self

    def __unicode__(self):
                return self.reason

class Incident(BaseModel):
    INCIDENT_TYPES = (('vehicle','Vehicle'),
                      ('windscreen','Windscreen'), 
                      ('tyres','Tyres'),
                      ('other','Other'))
    INCIDENT_STATUSES = (('captured','Captured'),
                         ('paid','Paid'),
                         ('rejected','Rejected'),
                         ('submitted for payment','Submit For Payment'))
    CO_PAYMENTS = (('yes','Yes'),('no','No'))
    
    incident_date = models.DateTimeField(null=False, blank=False, verbose_name='Incident Date')
    incident_type = models.CharField(max_length=255, null=False, blank=False, choices=INCIDENT_TYPES, verbose_name='Incident Type')
    description = models.TextField(null=False, blank=False)
    cost = models.DecimalField(default=0, max_digits=10, decimal_places=2)    
    driver = ProtectedForeignKey('employees.Employee', null=True, blank=True, related_name='incident_driver')
    vehicle = ProtectedForeignKey('Vehicle', null=False, blank=False, related_name='incident_vehicle')
    reference_number = models.CharField(max_length=255, null=True, blank=True, verbose_name="Reference Number")
    resolved = models.BooleanField(default=False)
    status = models.CharField(max_length=255, null=True, blank=True, choices=INCIDENT_STATUSES)
    invoice_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="Invoice Amount")
    invoice_number = models.CharField(max_length=255, null=True, blank=True, verbose_name="Invoice Number")
    driver_co_payment = models.CharField(max_length=255, null=True, blank=True, choices=CO_PAYMENTS, verbose_name="Driver Co Payment")
    percentage = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    share_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Share Amount")
    date_recieved_by_fleet = models.DateTimeField(null=True, blank=True, verbose_name='Date Recieved By Fleet')
    date_sent_to_finance = models.DateTimeField(null=True, blank=True, verbose_name='Date Sent Through To Finance')
    created_by = ProtectedForeignKey('operations.OperationsUser', null=False, blank=False, related_name='created_incidents')
    modified_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True, related_name='modified_incidents')
    history = HistoricalRecords()

    def __unicode__(self):
        return self.incident_type

    def get_share_amount(self):
        result = (self.invoice_amount * self.percentage)/100
        return result

    def save(self, *args, **kwargs):
        if self.driver_co_payment == 'yes':
            self.share_amount = self.get_share_amount()

        super(Incident, self).save(*args, **kwargs)


class FuelCard(BaseModel):
    CARD_TYPES = (('fuel only', 'Fuel Only'),
                  ('fuel & oil','Fuel & Oil'),
                  ('fuel, oil & toll', 'Fuel, Oil & Toll'),
                  ('fuel, oil & etag', 'Fuel, Oil & eTag'))

    FUEL_CARD_STATUSES = (('active', 'Active'),
                          ('cancelled', 'Cancelled'))
    BOOL_OPTIONS = (('yes', 'Yes'),
                    ('no', 'No'))

    card_type = models.CharField(max_length=255, null=False, blank=False, choices=CARD_TYPES, verbose_name='Card Type')
    card_number = models.CharField(max_length=255, null=False, blank=False, verbose_name='Card Number', unique=True)
    vendor = ProtectedForeignKey('operations.Vendor', null = True, blank = True, related_name='fuel_card_supplier')
    vehicle_assigned = ProtectedForeignKey('Vehicle', null = True, blank = True, related_name='vehicle_fuelcard')
    status = models.CharField(max_length=25, null=False, blank=False, default='active', choices=FUEL_CARD_STATUSES, verbose_name='Status')
    cancelled_date = models.DateTimeField(null=True, blank=True, verbose_name='Cancelled Date')
    start_date = models.DateTimeField(null=True, blank=True, verbose_name='Start Date')
    card_limit = models.IntegerField(null=True, blank=True, default=0,
                                      validators=[MinValueValidator(0)], verbose_name='Card Limit')
    new_card_ordered = models.CharField(max_length=255, null=True, blank=True, choices=BOOL_OPTIONS, verbose_name='New Card Ordered')
    date_ordered = models.DateTimeField(null=True, blank=True, verbose_name='Date Ordered')
    comment = models.CharField(max_length=255, null=True, blank=True, verbose_name='Comments')
    delivery_destination = models.CharField(max_length=255, null=True, blank=True, verbose_name='Delivery Destination')
    created_by = ProtectedForeignKey('operations.OperationsUser', null=False, blank=False, related_name='created_fuel_cards')
    modified_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True, related_name='modified_fuel_cards')
    history = HistoricalRecords()

    def save(self, *args, **kwargs):

        curr_fuel_card = self.vehicle_assigned.current_fuel_card if self.vehicle_assigned else None

        if curr_fuel_card and curr_fuel_card.id != self.id:
            curr_fuel_card.cancelled_date = self.start_date
            curr_fuel_card.status = 'cancelled'
            curr_fuel_card.modified_by_id = self.created_by_id
            super(FuelCard, curr_fuel_card).save(*args, **kwargs)

        super(FuelCard, self).save(*args, **kwargs)

        return self 

    def __unicode__(self):
        return self.card_number

    @property
    def total_usage(self):
        return FuelCardUsage.objects.filter(fuel_card=self.pk,
                                            transaction_type__description__in=['FUEL', 'OIL','TOLL-GATE'],)\
                                    .aggregate(Sum('amount'))['amount__sum'] or 0

    def previous_fuel_card(self):
        if self.vehicle_assigned:
            fuel_card = FuelCard.objects.filter(vehicle_assigned=self.vehicle_assigned,
                                                status='cancelled',
                                                cancelled_date__lte=self.start_date)\
                                        .order_by('-cancelled_date').first()
            if fuel_card:
                return fuel_card
            else:
                return None
        else:
            return None

    @property
    def last_transaction(self):
        usage =  FuelCardUsage.objects.filter(fuel_card=self.pk,
                                              transaction_type__description__in=['FUEL', 'OIL','TOLL-GATE'])\
                                      .order_by('-transaction_date', '-id')
        if usage:
            return usage
        else:
            return None

    @property
    def previous_fuel_card_balance(self):
        balance = 0
        if self.previous_fuel_card() and self.previous_fuel_card().last_transaction:
            balance = self.previous_fuel_card().last_transaction.balance
        return balance

    @property
    def current_balance(self):
        first_of_month = datetime.now().replace(day=1)
        usage =  FuelCardUsage.objects.filter(fuel_card=self.pk,
                                              transaction_type__description__in=['FUEL', 'OIL','TOLL-GATE'], 
                                              transaction_date__gte=first_of_month,)\
                                      .aggregate(Sum('amount'))['amount__sum'] or 0
        return self.card_limit - usage

    @property
    def balance(self):
        first_of_month = datetime.now().replace(day=1)
        if datetime.now().month == 12:
            last_of_month = datetime.now().replace(day=31)

        else:
            last_of_month = datetime.now().replace(month=datetime.now().month+1, day=1) - timedelta(days=1)

        usage =  FuelCardUsage.objects.filter(vehicle=self.vehicle_assigned,
                                              transaction_type__description__in=['FUEL', 'OIL','TOLL-GATE'],
                                              transaction_date__gte=first_of_month,)\
                                      .aggregate(Sum('amount'))['amount__sum'] or 0
        return self.card_limit - usage

    @property
    def fuel_usage(self):
        first_of_month = datetime.now().replace(day=1)
        usage =  FuelCardUsage.objects.filter(fuel_card=self.pk,
                                              transaction_type__description__in=['FUEL', 'OIL','TOLL-GATE'],
                                              transaction_date__gte=first_of_month,)\
                                      .aggregate(Sum('amount'))['amount__sum'] or 0
        return usage

    @property
    def driver(self):
        try:
            if self.vehicle_assigned:
                return self.vehicle_assigned.driver
            else:
                return None
        except VehicleDriver.DoesNotExist:
            return None

class VehicleFuelCard(BaseModel):

    vehicle = ProtectedForeignKey('Vehicle', null=False, blank=False, related_name='vehicle_fuel_card')
    fuel_card = ProtectedForeignKey('FuelCard', null=False, blank=False, related_name='fuel_card_vehicle')
    start_date = models.DateTimeField(null=False, blank=False, verbose_name='Start Date')
    end_date = models.DateTimeField(null=True, blank=True, verbose_name='End Date')
    reason = models.CharField(max_length=255, null=True, blank=True)
    created_by = ProtectedForeignKey('operations.OperationsUser', null=False, blank=False, related_name='created_vehiclefuelcard')
    modified_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True, related_name='modified_vehiclefuelcard')

    def save(self, *args, **kwargs):

        curr_fuel_card = self.vehicle.current_fuel_card

        if curr_fuel_card:
            curr_fuel_card.end_date = self.start_date
            curr_fuel_card.modified_by_id = self.created_by_id
            super(VehicleFuelCard, curr_fuel_card).save(*args, **kwargs)

            fuel_card = curr_fuel_card.fuel_card
            fuel_card.status  = "cancelled"
            fuel_card.cancelled_date = self.start_date
            fuel_card.save()

        new_vehicle_driver = self

        super(VehicleFuelCard, self).save(*args, **kwargs)

        return self

class FuelCardUsageTransactionType(BaseModel):
    description = models.CharField(max_length=255, null=False, blank=False,)

    def __unicode__(self):
        return self.description


class FuelCardUsage(BaseModel):
    USAGE_TYPES = (('import','Import'),('manual','Manual'))
    TRAN_TYPES  = (('CARD FEE','CARD FEE'),
                   ('COURIER SERVICE','COURIER SERVICE'),
                   ('DAMAGED CRD_FEE','DAMAGED CRD_FEE'),
                   ('EFT','EFT'),
                   ('FUEL','FUEL'),
                   ('MAINTENANCE','MAINTENANCE'),
                   ('OIL','OIL'),
                   ('TOLL-GATE','TOLL-GATE'),
                   ('TRANSACTION FEE','TRANSACTION FEE'),
                   ('VAT OF SER FEES','VAT OF SER FEES'))
    fuel_card = ProtectedForeignKey('FuelCard', null=True, blank=True, verbose_name='Fuel Card Number', related_name='fuel_card_usage')
    transaction_date = models.DateTimeField(null=False, blank=False, verbose_name='Transaction Date',)
    usage_type = models.CharField(max_length=255, null=False, blank=False, verbose_name='Usage Type', default='import', choices=USAGE_TYPES)
    transaction_type = models.ManyToManyField(FuelCardUsageTransactionType, verbose_name='Transaction Type', related_name='fuel_usage_transaction_types')
    transaction_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='Transaction Number')
    transaction_code = models.CharField(max_length=255, null=True, blank=True, verbose_name='Transaction Code')
    merchant_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Merchant Name')
    quantity = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    driver = ProtectedForeignKey('employees.Employee', null=True, blank=True, related_name='fuel_usage_driver')
    vehicle = ProtectedForeignKey('Vehicle', null=True, blank=True, related_name='fuel_usage_vehicle')
    comment = models.CharField(max_length=255, null=True, blank=True, verbose_name='Comments')

    @property
    def total_usage(self):
        return FuelCardUsage.objects.filter(fuel_card=self.pk,
                                            transaction_type__description__in=['FUEL', 'OIL','TOLL-GATE'],)\
                                    .aggregate(Sum('amount'))['amount__sum'] or 0

    def fuel_usage(self):
        first_of_month = self.transaction_date.replace(day=1)
        if self.transaction_date.month == 12:
            last_of_month = self.transaction_date.replace(day=31)
        else:
            last_of_month = self.transaction_date.replace(month=self.transaction_date.month+1, day=1) - timedelta(days=1)
        transaction_types = FuelCardUsageTransactionType.objects.filter(description__in=['FUEL', 'OIL','TOLL-GATE'])
        usage =  FuelCardUsage.objects.filter(fuel_card=self.fuel_card, 
                                              transaction_type__in=transaction_types,
                                              transaction_date__gte=first_of_month, 
                                              transaction_date__lte=self.transaction_date)\
                                      .aggregate(Sum('amount'))['amount__sum'] or 0
        return usage


    @property
    def balance(self):
        return self.fuel_card.card_limit - self.fuel_usage()

class FuelCardUsageDocumentUploads(BaseModel):
    description = models.CharField(max_length=255, null=False, blank=False,)

    def __unicode__(self):
                return self.description

class FuelCardUsageDocument(BaseModel):

    fuel_usage = ProtectedForeignKey('FuelCard', null=False, blank=False, related_name='fuel_usage_documents')
    document = ProtectedForeignKey('operations.Document', null=False, blank=False)
    document_type = models.ManyToManyField(FuelCardUsageDocumentUploads, verbose_name='Document Type')
    created_by = ProtectedForeignKey('operations.OperationsUser', null=False, blank=False, related_name='created_fuel_usage_documents')
    modified_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True, related_name='modified_fuel_usage_documents')

class FuelCardDocumentUploads(BaseModel):
    description = models.CharField(max_length=255, null=False, blank=False,)

    def __unicode__(self):
                return self.description

class FuelCardDocument(BaseModel):

    fuel_card = ProtectedForeignKey('FuelCard', null=False, blank=False, related_name='fuel_card_documents')
    document = ProtectedForeignKey('operations.Document', null=False, blank=False)
    document_type = models.ManyToManyField(FuelCardDocumentUploads, verbose_name='Document Type')
    created_by = ProtectedForeignKey('operations.OperationsUser', null=False, blank=False, related_name='created_fuel_card_documents')
    modified_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True, related_name='modified_fuel_card_documents')    

class IncidentDocumentUploads(BaseModel):
    description = models.CharField(max_length=255, null=False, blank=False,)
    incident_type = models.CharField(max_length=255, null=False, blank=False,)

    def __unicode__(self):
                return self.description

class IncidentDocument(BaseModel):

    incident = ProtectedForeignKey('Incident', null=False, blank=False, related_name='incident_documents')
    document = ProtectedForeignKey('operations.Document', null=False, blank=False)
    document_type = models.ManyToManyField(IncidentDocumentUploads, verbose_name='Document Type')
    created_by = ProtectedForeignKey('operations.OperationsUser', null=False, blank=False, related_name='created_incident_documents')
    modified_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True, related_name='modified_incident_documents')

class IncidentComment(BaseModel):

    incident = ProtectedForeignKey('Incident', null=False, blank=False, related_name='incident_comment')
    comment = ProtectedForeignKey('operations.Comment', null=False, blank=False)
    created_by = ProtectedForeignKey('operations.OperationsUser', null=False, blank=False, related_name='created_incident_comment')
    modified_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True, related_name='modified_incident_comment')

class ServiceBooking(BaseModel):
    
    service = models.BooleanField(default=False)
    maintenance = models.BooleanField(default=False)
    vehicle = ProtectedForeignKey('Vehicle', null=False, blank=False, related_name='service_bookings')
    comment = models.TextField(null=True, blank=True)
    booking_date = models.DateTimeField(null=True, blank=True, verbose_name='Booking Date')
    service_date = models.DateTimeField(null=True, blank=True, verbose_name='Service Date')
    current_mileage = models.IntegerField(null=True, blank=True, default=0,
                                      validators=[MinValueValidator(0)], verbose_name='Current Mileage')

    brakes = models.BooleanField(default=False)
    clutch = models.BooleanField(default=False)
    tyres = models.BooleanField(default=False)
    other = models.BooleanField(default=False)

    long_term_repairs = models.BooleanField(default=False, verbose_name='Long Term Repairs')
    follow_up_date = models.DateTimeField(null=True, blank=True, verbose_name='Follow-up Date')
    status = models.CharField(max_length=255, null=True, blank=True)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    service_interval = models.CharField(max_length=255, null=True, blank=True, verbose_name='Service Interval')

    document_received = models.CharField(max_length=255, null=True, blank=True, verbose_name='Document Type')
    document_number = models.CharField(max_length=50, null=True, blank=True, verbose_name='Document Number')
    document_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0.00)], verbose_name='cost')
    document_date = models.DateTimeField(null=True, blank=True, verbose_name='Document Date')
    vendor = ProtectedForeignKey('operations.Vendor', null = True, blank = True, related_name='service_bookings_vendor')

    created_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True, related_name='created_service_bookings')
    authorised_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True, related_name='authorised_service_bookings')

class InsuranceClaim(BaseModel):

    CLAIMTYPES = (('accident claim', 'Accident Claim'),
                  ('vehicle theft', 'Vehicle Theft'),
                  ('windscreen', 'Windscreen'),
                  ('other', 'Other'))

    INSURANCECLAIM_STATUSES = (('captured','Captured'),
                         ('paid','Paid'),
                         ('rejected','Rejected'),
                         ('submitted for payment','Submit For Payment'))
    CO_PAYMENTS = (('yes','Yes'),('no','No'))

    # incident = ProtectedForeignKey('Incident', null=False, blank=False, related_name='insurance_claim')
    vehicle = ProtectedForeignKey('Vehicle', null=False, blank=False, related_name='insurance_vehicle')
    incident_date = models.DateTimeField(null=False, blank=False, verbose_name='Incident Date')
    driver = ProtectedForeignKey('employees.Employee', null=True, blank=True, related_name='insurance_claim_driver')

    claim_type = models.CharField(max_length=50, null=False, blank=False, choices=CLAIMTYPES, verbose_name='Claim Type')
    reason_other = models.CharField(max_length=255, null=True, blank=True, verbose_name="Reason")
    quote_reference_number = models.CharField(max_length=255, null=True, blank=True, verbose_name="Quote Reference Number")
    quote_amount = models.CharField(max_length=50, null=True, blank=True, validators=[MinValueValidator(0)], verbose_name='Quote Amount')
    damage_description = models.TextField(null=False, blank=False, verbose_name="Damage Description")
    incident_description = models.TextField(null=False, blank=False, verbose_name="Incident Description")
    submission_date = models.DateTimeField(null=True, blank=True, verbose_name='Insurance Submission Date')

    insurance_reference_number = models.CharField(max_length=255, null=True, blank=True, verbose_name="Claim Reference Number")
    insurance_date_recieved = models.DateTimeField(null=True, blank=True, verbose_name='Insurance Date Recieved')
    insurance_comment = models.TextField(null=True, blank=True, verbose_name="Insurance Comment")
    claim_number = models.CharField(max_length=255, null=True, blank=True, verbose_name="Claim Number")
    claim_date_recieved = models.DateTimeField(null=True, blank=True, verbose_name='Claim Date Recieved')
    claim_comment = models.TextField(null=True, blank=True, verbose_name="Claim Comment")
    vendor = ProtectedForeignKey('operations.Vendor', null = True, blank = True, related_name='insurance_claim_vendor')
    status = models.CharField(max_length=255, null=True, blank=True, choices=INSURANCECLAIM_STATUSES)

    invoice_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="Invoice Amount")
    invoice_number = models.CharField(max_length=255, null=True, blank=True, verbose_name="Invoice Number")
    driver_co_payment = models.CharField(max_length=255, null=True, blank=True, choices=CO_PAYMENTS, verbose_name="Driver Co Payment")
    percentage = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    share_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Share Amount")

    created_by = ProtectedForeignKey('operations.OperationsUser', null=False, blank=False, related_name='created_insurance_claims')
    modified_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True, related_name='modified_insurance_claims')

    def get_share_amount(self):
        result = (self.invoice_amount * self.percentage)/100
        return result

    def save(self, *args, **kwargs):
        if self.driver_co_payment == 'yes':
            self.share_amount = self.get_share_amount()

        super(InsuranceClaim, self).save(*args, **kwargs)


class InsuranceClaimDocumentUploads(BaseModel):
    description = models.CharField(max_length=255, null=False, blank=False,)
    insurance_claim_type = models.CharField(max_length=255, null=False, blank=False,)

    def __unicode__(self):
                return self.description

class InsuranceClaimDocumentTypes(BaseModel):
    description = models.CharField(max_length=255, null=False, blank=False)

    def __unicode__(self):
                return self.description

class InsuranceClaimDocument(BaseModel):

    insurance_claim = ProtectedForeignKey('InsuranceClaim', null=False, blank=False, related_name='insurance_claim_documents')
    document = ProtectedForeignKey('operations.Document', null=False, blank=False)
    document_type = models.ManyToManyField(InsuranceClaimDocumentTypes, verbose_name='Document Type')
    created_by = ProtectedForeignKey('operations.OperationsUser', null=False, blank=False, related_name='created_insurance_claim_documents')
    modified_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True, related_name='modified_insurance_claim_documents')

class InsuranceClaimComment(BaseModel):

    insurance_claim = ProtectedForeignKey('InsuranceClaim', null=False, blank=False, related_name='insurance_claim_comment')
    comment = ProtectedForeignKey('operations.Comment', null=False, blank=False)
    created_by = ProtectedForeignKey('operations.OperationsUser', null=False, blank=False, related_name='created_insurance_claim_comment')
    modified_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True, related_name='modified_insurance_claim_comment')

class ServiceMaintanceDocument(BaseModel):

    service_booking = ProtectedForeignKey('ServiceBooking', null=False, blank=False, related_name='service_booking_documents')
    document = ProtectedForeignKey('operations.Document', null=False, blank=False)
    created_by = ProtectedForeignKey('operations.OperationsUser', null=False, blank=False, related_name='created_service_maintenance_documents')
    modified_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True, related_name='modified_service_maintenance_documents')
    
class VehicleStatus(BaseModel):

    vehicle = models.ForeignKey(Vehicle, null=True, blank=True, related_name='vehicle_status')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,related_name="status_capture_by")
    status_type = models.ForeignKey(VehicleStatusType, null=True, blank=True, related_name='vehicle_status_type')
    comment = models.TextField(default=None, blank=True, null=True)
    deleted = models.BooleanField(default=False, db_index=True)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,related_name="status_changed_by")
    history = HistoricalRecords()

    def delete(self, logged_in_user):
        self.deleted = True
        self.save()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value
