from django.db import models
from lib.models import BaseModel
from lib.fields import ProtectedForeignKey
from dal import autocomplete
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from django.contrib.auth.models import AbstractUser
from fleet_management.models import *

class OperationsUser(AbstractUser):
    phone_number = models.CharField(null=True, max_length=50)
    signature = models.FileField(null=True, blank=True, upload_to='uploads/accounts')
    regional_staff = models.BooleanField(blank=True, default=False)
    region = ProtectedForeignKey('operations.Region', null = True, blank = True, related_name='user_region')
    district = ProtectedForeignKey('operations.Branch', null = True, blank = True, related_name='user_district')

    def __unicode__(self):
        return self.username


    @property
    def full_name(self):
        full_name = "{} {}".format(self.first_name,self.last_name) \
                    if self.first_name and self.last_name else \
                    "{}".format(self.first_name) if self.first_name \
                    else "{}".format(self.last_name) if self.last_name \
                    else None
        return full_name

    @property
    def can_edit(self):
        return self.is_superuser or self.privilege == 'create_elopsysuser' or self.privilege == 'admin'

    @property
    def is_executive(self):
        return 'Operations Executive' in self.groups.all()


    @property
    def is_emerald_employee(self):
        return 'Emerald Employee' in self.groups.all().values_list('name', flat=True)

    @property
    def is_technician(self):
        return 'Technician' in self.groups.all().values_list('name', flat=True)

    @property
    def is_administrator(self):
        return 'Administrator' in self.groups.all().values_list('name', flat=True)

    @property
    def is_management(self):
        return 'Management' in self.groups.all().values_list('name', flat=True)

    @property
    def is_regional_manager(self):
        return 'Regional Manager' in self.groups.all().values_list('name', flat=True)

    @property
    def is_regional_user(self):
        return self.regional_staff

    @property
    def get_user_region(self):
        if self.region is None:
            return Region.objects.none()
        else:
            return self.region.id

    @property
    def get_user_district(self):
        if self.district is None:
            return Branch.objects.none()
        else:
            return self.district.id

class Contact(BaseModel):
    first_name = models.CharField(max_length=255, null=False, blank=False, verbose_name='Contact First Name')
    last_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Contact Last Name')
    tel_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='Telephone Number')
    tel_number_2 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Telephone Number 2')
    tel_number_3 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Telephone Number 3')
    cell_number = models.CharField(max_length=255, null=True, blank=True, db_index=True, verbose_name='Cell Number')
    email = models.CharField(max_length=255, null=True, blank=True, db_index=True)

class Address(BaseModel):

    ADDRESS_TYPES = (('postal','Postal'),('residential','Residential'),
                     ('business','Business'),('residential', 'Residential'),
                     ('pobox','POBox'))
    
    address_type = models.CharField(max_length=50, null=False, blank=False,
                                    choices=ADDRESS_TYPES, db_index=True)
    address_line_1 = models.CharField(max_length=255, null=False, blank=False, verbose_name='Address Line 1')
    address_line_2 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Address Line 2')
    suburb = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True, verbose_name='Postal Code')
    city = models.CharField(max_length=255, null=False, blank=False, db_index=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=False, blank=False,
                               default="South Africa")

class ThumbnailImageField(ImageSpecField):
    def __init__(self, *args, **kwargs):
        super(ThumbnailImageField, self).__init__(processors=[ResizeToFill(400, 400)],
                                                  options={'quality': 80},
                                                  *args, **kwargs)
        
class Document(BaseModel):

    FILE_TYPES = (('document','Document'),('photo','Photo'))
    
    document_name = models.CharField(max_length=255, null=False, blank=False, db_index=True)
    
    document = models.FileField(null=True, blank=True, upload_to='uploads/documents')
    image = models.ImageField(null=True, blank=True, upload_to="uploads/images")
    thumbnail = ThumbnailImageField(source="image")
    
    file_type = models.CharField(max_length=50, null=False, blank=False,
                                 choices=FILE_TYPES, db_index=True)
    
    description = models.TextField(null=True, blank=True)
    created_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True,
                                     db_index=True)

class Comment(BaseModel):
    comment = models.TextField(null=True, blank=True)
    created_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True,
                                     db_index=True)
    
class BaseTicket(BaseModel):
    TICKET_STATUS = (('new', 'New'), ('pending', 'Pending'),
                     ('closed', 'Closed'))
    CATEGORIES = (('fleet management', 'Fleet Management'), ('inventory', 'Inventory'),
                     ('property and facilities', 'Property & Facilities'), ('offices', 'Offices'))
    number = models.CharField(max_length=255, null=False, blank=False, unique=True,
                              db_index=True)

    category = models.CharField(max_length=50, null=False, blank=False, default='new',
                              choices=CATEGORIES, db_index=True)

    subject = models.CharField(max_length=255, null=False, blank=False, db_index=True)

    status = models.CharField(max_length=50, null=False, blank=False, default='new',
                              choices=TICKET_STATUS, db_index=True)

    employee = ProtectedForeignKey('employees.Employee', null=True, blank=True,
                                   db_index=True)

    technician = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True,
                                     db_index=True, related_name='baseticket_technician')

    description = models.TextField(null=False, blank=False)

    is_closed = models.BooleanField(default=False)

    possible_fix = ProtectedForeignKey('TicketFixOption', null=True, blank=True)

    created_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True,
                                     db_index=True, related_name='baseticket_creator')

    # def save(self,*args, **kwargs):
    #     if self.status == 'closed':
    #         self.is_closed = True
    #         super(BaseTicket, self).save(*args, **kwargs)


class TicketEscalation(BaseModel):
    ticket = ProtectedForeignKey('BaseTicket', blank=False, null=False, db_index=True)
    reason = models.TextField(null=False, blank=False)
    
    from_user = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True,
                                    db_index=True, related_name='escalate_from_user')
    
    to_user = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True,
                                  db_index=True, related_name='escalate_to_user')
    
    created_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True,
                                     db_index=True)
    
class TicketFixOption(BaseModel):
    name = models.CharField(max_length=255, null=False, blank=False, db_index=True)
    description = models.TextField(null=False, blank=False)

class Region(BaseModel):
    code = models.CharField(max_length=255, unique=True, null=False, blank=False)
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)

    def __unicode__(self):
        return "{} - {}".format(self.code, self.name)

    @property
    def region_name(self):
        return "{} - {}".format(self.code, self.name)
    
class Branch(BaseModel):

    OFFICE_TYPES = (('Head Office', 'Head Office'),
                    ('Regional', 'Regional'),
                    ('Satelite', 'Satelite'))
    code = models.CharField(max_length=255, unique=True, null=False, blank=False)
    description = models.CharField(max_length=255, null=False, blank=False)
    office_type = models.CharField(max_length=50, null=True, blank=True, default='new',
                                   choices=OFFICE_TYPES, db_index=True)
    region = ProtectedForeignKey('operations.Region', null=True, blank=True, related_name='branch_region')
    contact_person = ProtectedForeignKey('operations.Contact', null=True, blank=True, related_name='branch_contact')
    address = ProtectedForeignKey('operations.Address', null=True, blank=True, related_name='branch_address')
    
    def __unicode__(self):
        return "{} - {}".format(self.code, self.description)

    @property
    def branch_name(self):
        return "{} - {}".format(self.code, self.description)
    

class Insurer(BaseModel):
    name = models.CharField(max_length=255, null=False, unique=True, blank=False, verbose_name='Insurer Name')
    contact_person = ProtectedForeignKey('operations.Contact', null=True, blank=True, related_name='insurer_contact')
    address = ProtectedForeignKey('operations.Address', null=True, blank=True, related_name='insurer_address')
    created_by = ProtectedForeignKey('operations.OperationsUser', null=False, blank=False, related_name='created_insurer')
    modified_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True, related_name='modified_insurer')

    def insured_vehicles(self):
        iv = Insurance.objects.filter(insurer=self).count()
        return iv

    def __unicode__(self):
        return self.name

class ServiceProvider(BaseModel):
    name = models.CharField(max_length=255, null=False, unique=True, blank=False, verbose_name='Service Provider')
    contact_person = ProtectedForeignKey('operations.Contact', null=True, blank=True, related_name='service_provider_contact')
    address = ProtectedForeignKey('operations.Address', null=True, blank=True, related_name='service_provider_address')
    created_by = ProtectedForeignKey('operations.OperationsUser', null=False, blank=False, related_name='created_service_provider')
    modified_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True, related_name='modified_service_provider')

    def __unicode__(self):
        return self.name

class Vendor(BaseModel):

    TYPE_LIST = (('branding', 'Branding'),('dealer', 'Dealer'),('fuel card supplier', 'Fuel Card Supplier'),('installer', 'Installer'),
                ('insurance', 'Insurance'),('service provider', 'Service Provider'),('tracker', 'Tracker'))
    ACCOUNT_TYPE = (('cash','Cash'),('credit','Credit'),('debit','Debit'))

    name = models.CharField(max_length=255, null=False, unique=True, blank=False, verbose_name='Vendor')
    vendor_type = models.CharField(max_length=50, null=False, blank=False, choices=TYPE_LIST, db_index=True, verbose_name='Vendor Type')
    account_type = models.CharField(max_length=50, null=True, blank=True, choices=ACCOUNT_TYPE, verbose_name='Account Type')
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    contact_person = ProtectedForeignKey('operations.Contact', null=True, blank=True, related_name='vendor_contact')
    address = ProtectedForeignKey('operations.Address', null=True, blank=True, related_name='vendor_address')
    created_by = ProtectedForeignKey('operations.OperationsUser', null=False, blank=False, related_name='created_vendor')
    modified_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True, related_name='modified_vendor')

    def __unicode__(self):
        return self.name

class VendorBankDetail(BaseModel):

    BANK_LIST = (('', 'Please select'),
              ('ABSA', 'ABSA'), ('AFRICAN', 'AFRICAN'),
              ('ALBARAKA', 'ALBARAKA'), ('ATHENS', 'ATHENS'),
              ('BIDVEST', 'BIDVEST'), ('BOE', 'BOE'),
              ('CAPITEC', 'CAPITEC'), ('CITI', 'CITI'),
              ('FBC', 'FBC'), ('FINBOND', 'FINBOND'),
              ('FNB', 'FNB'), ('FNBBOTS', 'FNBBOTS'),
              ('FNBLES', 'FNBLES'), ('FNBNAM', 'FNBNAM'),
              ('FNBSWAZ', 'FNBSWAZ'), ('FNBTRANS', 'FNBTRANS'),
              ('GRINDROD', 'GRINDROD'), ('HABIB', 'HABIB'),
              ('HBZ', 'HBZ'), ('HSBC', 'HSBC'),
              ('INDIA', 'INDIA'), ('INVESTEC', 'INVESTEC'),
              ('ITHALA', 'ITHALA'), ('JPMORGAN', 'JPMORGAN'),
              ('MERCANT', 'MERCANT'), ('MTN', 'MTN'),
              ('NBS', 'NBS'), ('NEDBANK', 'NEDBANK'),
              ('NEDBOND', 'NEDBOND'), ('NEDLES', 'NEDLES'),
              ('NEDNAM', 'NEDNAM'), ('NEDSWAZ', 'NEDSWAZ'),
              ('OLYMPUS', 'OLYMPUS'), ('PARIBAS', 'PARIBAS'),
              ('PEOP CUR', 'PEOP CUR'), ('PEOPLES', 'PEOPLES'),
              ('PEP', 'PEP'), ('POST', 'POST'),
              ('ROYALSCO', 'ROYALSCO'), ('SASFIN', 'SASFIN'),
              ('STANCHAR', 'STANCHAR'), ('STANDARD', 'STANDARD'),
              ('STANNAM', 'STANNAM'), ('STANSWAZ', 'STANSWAZ'),
              ('STD LES', 'STD LES'), ('UBANK', 'UBANK'),
              ('UNIBANK', 'UNIBANK'), ('VBSMut', 'VBSMut'),
              ('WINDHOEK', 'WINDHOEK'))

    vendor = ProtectedForeignKey('operations.Vendor', null=True, blank=True, related_name='vendor_bank_details')
    bank_name = models.CharField(max_length=255, null=False, blank=False, choices=BANK_LIST, db_index=True, verbose_name='Bank Name')
    branch_code = models.CharField(max_length=50, null=True, blank=True, verbose_name='Branch Code') 
    account_holder_name = models.CharField(max_length=250, null=True, blank=True, verbose_name='Account Holder Name')
    account_number = models.CharField(max_length=50, null=False, unique=True, blank=False, verbose_name='Account Number')
    created_by = ProtectedForeignKey('operations.OperationsUser', null=False, blank=False, related_name='created_service_provider_bank')
    modified_by = ProtectedForeignKey('operations.OperationsUser', null=True, blank=True, related_name='modified_service_provider_bank')

class RegionAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Region.objects.none()

        qs = Region.objects.all()

        if self.q:
            qs = qs.filter(Q(name__icontains=self.q) |
                           Q(code__icontains=self.q)).order_by('name')
        return qs

class DistrictAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Branch.objects.none()

        region_id = self.forwarded.get('region', None)
        qs = Branch.objects

        if region_id:
            qs = qs.filter(region__pk=region_id)
        else:
            return Branch.objects.none()

        if self.q:
            qs = qs.filter(Q(name__icontains=self.q) |
                           Q(code__icontains=self.q)).order_by('name')
        return qs
