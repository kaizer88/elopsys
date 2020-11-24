from lib.excel_helper import ExcelHelper
from datetime import datetime, timedelta
from decimal import Decimal
from django.utils import timezone
from django.conf import settings
from django.core.files import File

from models import Vehicle, Tracker
from employees.models import Employee
from operations.models import *
from facilities.models import *

from django.db import transaction
from django.db.models.functions import Concat
from django.db.models import Q
from datetime import datetime
from django.db.models import Value as V

import logging
logger = logging.getLogger(__name__)

def import_vehicle_data(user, vehicles_file):
    row_number = 1

    try:
        with transaction.atomic():
            excel = ExcelHelper(content=vehicles_file.file.read())

            headers = excel.read_header(1)

            row_number = 2
            while row_number <= excel.nrows:
                row = excel.read_row(row_number)
                row_data = dict(zip(headers, row))

                reg_date = None if not row_data.get('registration date') else row_data.get('registration date')
                if reg_date:
                    reg_date = datetime.strptime(reg_date, '%Y %m %d')

                mak = None if not row_data.get('make') else row_data.get('make')
                make = VehicleMake.objects.filter(make_name=mak).first()
                if not make or make is None:
                    make = VehicleMake(make_name=mak)
                    make.save()

                modl = None if not row_data.get('model') else row_data.get('model')
                model = VehicleModel.objects.filter(model_name=modl).first()
                if not model or model is None:
                    model = VehicleModel(model_name=modl,
                                         make=make)
                    model.save()

                region = Region.objects.filter(name=row_data.get('region')).first() or None

                district = Branch.objects.filter(description=row_data.get('district')).first() or None

                lic_exp_date = None if not row_data.get('licence expiry date') else row_data.get('licence expiry date')
                if lic_exp_date:
                    lic_exp_date = datetime.strptime(lic_exp_date, '%Y %m %d')


                engine_cap = row_data.get('engine capacity')
                if engine_cap:
                    engine_cap = int(engine_cap)
                else:
                    engine_cap = None

                tank_cap = row_data.get('tank capacity (liters)')
                if tank_cap:
                    tank_cap = int(tank_cap)
                else:
                    tank_cap = None

                del_mileage = 0 if not row_data.get('delivery mileage') else int(row_data.get('delivery mileage'))
                vehicle = Vehicle.objects.filter(registration_number=row_data.get('reg'))

                if not vehicle.exists():
                    Vehicle.objects.create(
                        ownership=row_data.get('vehicle owner').lower(),
                        division=row_data.get('division').lower(),
                        status_at_create=row_data.get('status at create').lower(),
                        vehicle_make=make,
                        vehicle_model=model,
                        region=region,
                        district=district,
                        year_model=int(row_data.get('year model')),
                        registration_number=row_data.get('reg').upper().replace(' ',''),
                        registration_date=reg_date,
                        licence_disk_expiry=lic_exp_date,
                        vin_number=row_data.get('vin number').upper(),
                        engine_number=row_data.get('engine number').upper(),
                        colour=row_data.get('colour').title(),
                        transmission=row_data.get('transmission').lower(),
                        fuel_type=row_data.get('fuel type').lower(),
                        engine_capacity=engine_cap,
                        tank_capacity=tank_cap,
                        delivery_mileage=del_mileage,
                        has_aircon=True if 'yes' in row_data.get('aircon').lower() else False,
                        has_radio=True if 'yes' in row_data.get('radio').lower() else False,
                        has_bluetooth=True if 'yes' in row_data.get('bluetooth').lower() else False,
                        has_jack=True if 'yes' in row_data.get('jack').lower() else False,
                        has_spanner=True if 'yes' in row_data.get('spanner').lower() else False,
                        has_triangle=True if 'yes' in row_data.get('triangle').lower() else False,
                        created_by=user)

                else:

                    vehicle.update(
                        ownership=row_data.get('vehicle owner').lower(),
                        division=row_data.get('division').lower(),
                        status_at_create=row_data.get('status at create').lower(),
                        vehicle_make=make,
                        vehicle_model=model,
                        region=region,
                        district=district,
                        year_model=int(row_data.get('year model')),
                        registration_number=row_data.get('reg').upper().replace(' ',''),
                        registration_date=reg_date,
                        licence_disk_expiry=lic_exp_date,
                        vin_number=row_data.get('vin number').upper(),
                        engine_number=row_data.get('engine number').upper(),
                        colour=row_data.get('colour').title(),
                        transmission=row_data.get('transmission').lower(),
                        fuel_type=row_data.get('fuel type').lower(),
                        engine_capacity=engine_cap,
                        tank_capacity=tank_cap,
                        delivery_mileage=del_mileage,
                        has_aircon=True if 'yes' in row_data.get('aircon').lower() else False,
                        has_radio=True if 'yes' in row_data.get('radio').lower() else False,
                        has_bluetooth=True if 'yes' in row_data.get('bluetooth').lower() else False,
                        has_jack=True if 'yes' in row_data.get('jack').lower() else False,
                        has_spanner=True if 'yes' in row_data.get('spanner').lower() else False,
                        has_triangle=True if 'yes' in row_data.get('triangle').lower() else False)
                row_number += 1

    except Exception, ex:
        logger.exception(ex)
        raise Exception("Failed while processing row %d. Error was %s" % (row_number, ex))

def import_fuel_card_data(user, fuel_card_file):
    row_number = 1
    err_list = None
    temp = datetime(1899, 12, 30)

    try:
        with transaction.atomic():
            excel = ExcelHelper(content=fuel_card_file.file.read())

            headers = excel.read_header(1)

            row_number = 2
            while row_number <= excel.nrows:
                row = excel.read_row(row_number)
                row_data = dict(zip(headers, row))

                tran_xldate = None if not row_data.get('transactiondate') else row_data.get('transactiondate')
                if tran_xldate:
                    tran_date = datetime.strptime(tran_xldate, '%Y-%m-%d')

                tran_desc = None if not row_data.get('transactiondescription') else row_data.get('transactiondescription')
                transaction_type = FuelCardUsageTransactionType.objects.filter(description=tran_desc).first()
                if not transaction_type or transaction_type is None:
                    transaction_type = FuelCardUsageTransactionType(description=tran_desc)
                    transaction_type.save()

                vehicle_reg = None if not row_data.get('registrationnumber') else row_data.get('registrationnumber')
                vehicle = Vehicle.objects.filter(registration_number=vehicle_reg).first()
                if not vehicle:
                    if err_list == None:
                        err_list = "Vehicle does not exist on import line : " + str(row_number)
                    else:
                        err_list = err_list + "Vehicle does not exist on import line : " + str(row_number)

                card_num = None if not row_data.get('cardnumber') else row_data.get('cardnumber')
                fuel_card = FuelCard.objects.filter(card_number=card_num).first()
                if not fuel_card or fuel_card is None:
                    fuel_card = FuelCard(card_number=card_num, 
                                        vehicle_assigned=vehicle,
                                        start_date=tran_date,
                                        card_type='fuel, oil & toll',
                                        status='active',
                                        created_by=user)
                    fuel_card.save()
                    if err_list == None:
                        err_list = "Fuel Card does not exist on import line, created a new one : " + str(row_number)
                    else:
                        err_list = err_list + "Fuel Card does not exist on import line, created a new one : " + str(row_number)
                if vehicle:
                    driver = VehicleDriver.objects.filter((Q(vehicle=vehicle) & \
                                                           Q(start_date__lte=tran_date)) &\
                                                          (Q(end_date__gte=tran_date) | \
                                                           Q(end_date=None))) \
                                                  .first()
                    if not driver:
                        if err_list == None:
                            err_list = "Driver does not exist on import line : " + str(row_number)
                        else:
                            err_list = err_list + "Driver does not exist on import line : " + str(row_number)
                    else:
                        driver = driver.driver
                else:
                    driver = None

                use_type = 'Import'
                
                amount_used = None if not row_data.get('amount') else row_data.get('amount')
                if amount_used:
                    amount_used = Decimal(amount_used)

                quantity = None if not row_data.get('quantity') else row_data.get('quantity')
                if quantity:
                    quantity = Decimal(quantity)

                transaction_number = None if not row_data.get('transactionnumber') else row_data.get('transactionnumber')
                merchant_name = None if not row_data.get('merchantname') else row_data.get('merchantname')
                transaction_code = None if not row_data.get('transactioncode') else row_data.get('transactioncode')

                fuel_card_usage = FuelCardUsage.objects.filter(fuel_card=fuel_card,
                                                               transaction_date=tran_date,
                                                               transaction_number=transaction_number,
                                                               amount=amount_used)

                if not fuel_card_usage.exists() or fuel_card_usage is None:
                    fuel_card_usage = FuelCardUsage(
                        fuel_card=fuel_card,
                        vehicle=vehicle,
                        driver=driver,
                        usage_type=use_type,
                        transaction_date=tran_date,
                        transaction_number=transaction_number,
                        transaction_code=transaction_code,
                        merchant_name=merchant_name,
                        quantity=quantity,
                        amount=amount_used)

                    fuel_card_usage.save()
                    fuel_card_usage.transaction_type.add(transaction_type)
                    fuel_card_usage.save()
                    print str(row_number) + "-- Created -- " + str(fuel_card.pk) + " -- " + str(fuel_card.card_number)
                else:
                    print str(row_number) + "-- Exists -- " + str(fuel_card.pk) + " -- " + str(fuel_card.card_number)
                row_number += 1

    except Exception, ex:
        logger.exception(ex)
        raise Exception("Failed while processing row %d. Error was %s" % (row_number, ex))

def import_service_provider_data(user, service_provider_file):
    row_number = 1
    try:
        with transaction.atomic():
            excel = ExcelHelper(content=service_provider_file.file.read())

            headers = excel.read_header(2)

            row_number = 3
            while row_number <= excel.nrows:
                row = excel.read_row(row_number)
                row_data = dict(zip(headers, row))
               
                sp = Vendor.objects.filter(name=row_data.get('supplier'))
                if row_data.get('last contact person'):
                    last_contact = row_data.get('last contact person')
                else:
                    last_contact = row_data.get('supplier')
                contact = Contact.objects.annotate(fullname=Concat('first_name', V(' '), 'last_name')).filter(
                                                    Q(fullname__icontains=last_contact)|
                                                    Q(first_name__icontains=last_contact)|
                                                    Q(last_name__icontains=last_contact)).filter(
                                                    tel_number__icontains=row_data.get('contact'),
                                                    tel_number_2__icontains=row_data.get('contact 2')
                                                    )
                if not contact.exists():
                    contact = Contact(
                        first_name=last_contact,
                        tel_number=row_data.get('contact'),
                        tel_number_2=row_data.get('contact 2'),
                        email=row_data.get('email'),
                        )
                    contact.save()
                else:
                    contact = contact.first()
                    contact.first_name=last_contact
                    contact.tel_number=row_data.get('contact')
                    contact.tel_number_2=row_data.get('contact 2')
                    contact.email=row_data.get('email')
                    contact.save()

                if row_data.get('number') or row_data.get('street'):
                    address = Address.objects.filter(address_line_1=row_data.get('number'),
                                                      address_line_2=row_data.get('street'),
                                                      city=row_data.get('town'),
                                                      province=row_data.get('province'))
                    if not address.exists():
                        address = Address(address_line_1=row_data.get('number'),
                                          address_line_2=row_data.get('street'),
                                          city=row_data.get('town'),
                                          province=row_data.get('province')
                                          )
                        address.save()
                    else:
                        address = address.first()
                        address.address_line_1=row_data.get('number')
                        address.address_line_2=row_data.get('street')
                        address.city=row_data.get('town')
                        address.province=row_data.get('province')
                        address.save()

                if not sp.exists():
                    sp = Vendor(
                        name=row_data.get('supplier'),
                        vendor_type="service provider",
                        contact_person=contact,
                        address=address,
                        created_by=user)
                    sp.save()

                else:
                    sp = sp.first()
                    sp.name=row_data.get('supplier')
                    sp.vendor_type="service provider"
                    sp.contact_person=contact
                    sp.address=address
                    sp.save()
                        
                row_number += 1

                if row_data.get('bank name'):
                    bank_details = VendorBankDetail.objects.filter(vendor=sp,
                                                                   bank_name=row_data.get('bank name'),
                                                                   branch_code=row_data.get('branch code'),
                                                                   account_holder_name=row_data.get('supplier'),
                                                                   account_number=row_data.get('account number'),
                                                                   )
                    if not bank_details.exists():
                        bank_details = VendorBankDetail(vendor=sp,
                                                        bank_name=row_data.get('bank name'),
                                                        branch_code=row_data.get('branch code'),
                                                        account_holder_name=row_data.get('supplier'),
                                                        account_number=row_data.get('account number'),
                                                        created_by=user,
                                                       )
                        bank_details.save()
                    else:
                        bank_details.update(vendor=sp,
                                            bank_name=row_data.get('bank name'),
                                            branch_code=row_data.get('branch code'),
                                            account_holder_name=row_data.get('supplier'),
                                            account_number=row_data.get('account number'),
                                            modified_by=user,
                                           )

    except Exception, ex:

        logger.exception(ex)

        raise Exception("Failed while processing row %d. Error was %s" % (row_number, ex))


def import_stock_items_data(user, stock_items_file):
    row_number = 1    
    try:
        with transaction.atomic():
            excel = ExcelHelper(content=stock_items_file.file.read())

            headers = excel.read_header(1)

            row_number = 2
            while row_number <= excel.nrows:
                row = excel.read_row(row_number)
                row_data = dict(zip(headers, row))

                item = StockItem.objects.filter(item_name=row_data.get('stock item'),
                                                category=row_data.get('category'),)
                
                if not item.exists():
                    StockItem.objects.create(
                        item_name=row_data.get('stock item'),
                        category=row_data.get('category'),
                        stock_quantity=0,
                        created_by=user,
                        modified_by=user)

                else:
                    item.update(
                        item_name=row_data.get('stock item'),
                        category=row_data.get('category'),
                        created_by=user,
                        modified_by=user
                        )
                row_number += 1

    except Exception, ex:

        logger.exception(ex)

        raise Exception("Failed while processing row %d. Error was %s" % (row_number, ex))

def import_district_data(user, district_file):
    row_number = 1    
    try:
        with transaction.atomic():
            excel = ExcelHelper(content=district_file.file.read())

            headers = excel.read_header(1)

            row_number = 2
            while row_number <= excel.nrows:
                row = excel.read_row(row_number)
                row_data = dict(zip(headers, row))

                region = Region.objects.filter(name=row_data.get('region'))

                district = Branch.objects.filter(description=row_data.get('elbranches'))

                contact, created = Contact.objects.get_or_create(
                            first_name=row_data.get('contactperson'),
                            tel_number=row_data.get('contactnumber'),
                            tel_number_2=row_data.get('contactnumber2'),
                            tel_number_3=row_data.get('contactnumber3')
                            )

                address, created = Address.objects.get_or_create(
                            address_line_1=row_data.get('address'),
                            city=row_data.get('elbranches'),
                            country='South Africa'
                            )
                if region.exists():
                    region = region.first()

                if not district.exists():
                    district, created = Branch.objects.get_or_create(
                        description=row_data.get('elbranches'),
                        code=row_data.get('code'),
                        office_type=row_data.get('officetype'),
                        region=region,
                        contact_person=contact,
                        address=address)

                else:
                    district.update(
                        description=row_data.get('elbranches'),
                        code=row_data.get('code'),
                        office_type=row_data.get('officetype'),
                        region=region,
                        contact_person=contact,
                        address=address)
                row_number += 1

    except Exception, ex:

        logger.exception(ex)

        raise Exception("Failed while processing row %d. Error was %s" % (row_number, ex))

def import_mileage_data(user, mileage_file):
    row_number = 1
    err_list = None

    try:
        with transaction.atomic():
            excel = ExcelHelper(content=mileage_file.file.read())

            headers = excel.read_header(1)

            row_number = 2
            while row_number <= excel.nrows:
                row = excel.read_row(row_number)
                row_data = dict(zip(headers, row))

                tran_xldate = None if not row_data.get('updated date') else row_data.get('updated date')
                if tran_xldate:
                    upd_date = datetime.strptime(tran_xldate, '%Y/%m/%d')

                mileage = None if not row_data.get('updated mileage') else row_data.get('updated mileage')
                if mileage:
                    mileage = int(mileage)
                else:
                    mileage = None

                vehicle_reg = None if not row_data.get('vehicle registration') else row_data.get('vehicle registration')
                vehicle = Vehicle.objects.filter(registration_number=vehicle_reg).first()
                if not vehicle:
                    if err_list == None:
                        err_list = "Vehicle does not exist on import line : " + str(row_number)
                    else:
                        err_list = err_list + "Vehicle does not exist on import line : " + str(row_number)
                else:
                    if not mileage or mileage < 1:
                        logger.warning("Mileage is less or equal to zero on import line : %s", row_number)
                        if err_list == None:
                            err_list = "Mileage is less or equal to zero on import line : " + str(row_number)
                        else:
                            err_list = err_list + "Mileage is less or equal to zero on import line : " + str(row_number)
                    else:
                        if mileage < vehicle.updated_mileage:
                            logger.warning("Mileage is less than current reading on import line : %s", row_number)
                            if err_list == None:
                                err_list = "Mileage is less than current reading on import line : " + str(row_number)
                            else:
                                err_list = err_list + "Mileage is less than current reading on import line : " + str(row_number)
                        else:
                            vehicle.updated_mileage=mileage
                            vehicle.updated_date=upd_date

                            vehicle.save()
                            print str(row_number) + "-- Mileage Updated -- " + str(vehicle.registration_number)
                row_number += 1

    except Exception, ex:
        logger.exception(ex)
        raise Exception("Failed while processing row %d. Error was %s" % (row_number, ex))

def import_additional_vehicle_information_data(user, additional_information_file):
    row_number = 1
    try:
        with transaction.atomic():
            excel = ExcelHelper(content=additional_information_file.file.read())

            headers = excel.read_header(1)

            row_number = 2
            while row_number <= excel.nrows:
                row = excel.read_row(row_number)
                row_data = dict(zip(headers, row))

                vehicle_reg = None if not row_data.get('reg') else row_data.get('reg')

                driver_code = None if not row_data.get('agent code') else row_data.get('agent code')

                start_date = None if not row_data.get('start date') else row_data.get('start date')
                if start_date:
                    start_date = datetime.strptime(start_date, '%d/%m/%Y')

                service_area = None if not row_data.get('service area') else row_data.get('service area')

                status = None if not row_data.get('status') else row_data.get('status')

                tracker = None if not row_data.get('tracking source') else row_data.get('tracking source')

                fleet_admin = None if not row_data.get('fleet admin') else row_data.get('fleet admin')

                vehicle_status = VehicleStatusType.objects.filter(description=status).values_list('id', flat=True).first()

                item = VehicleDriver.objects.filter(vehicle__registration_number=row_data.get('reg'))

                vehicle = Vehicle.objects.filter(registration_number=row_data.get('reg')).values_list('id', flat=True).first()

                vehicles = Vehicle.objects.filter(registration_number=row_data.get('reg'))

                driver = Employee.objects.filter(commission_code=driver_code).values_list('id', flat=True).first()

                vehicle_tracker = Tracker.objects.filter(vehicle_id=vehicles)

                fleet_user = OperationsUser.objects.filter(username=fleet_admin).values_list('id', flat=True).first()

                if not item.exists():
                    if vehicle and driver:
                        VehicleDriver.objects.create(
                            vehicle_id=vehicle,
                            driver_id=driver,
                            start_date=start_date,
                            status='authorized',
                            created_by=user)

                    if  vehicles.exists():
                        vehicles.update(
                            status_id=vehicle_status,
                            service_area=service_area,
                            created_by = fleet_user or user
                            )

                        if not vehicle_tracker.exists():
                            Tracker.objects.create(
                                tracking_source=tracker,
                                vehicle_id=vehicle
                                )
                        else:
                            vehicle_tracker.update(
                                tracking_source=tracker,
                                vehicle_id=vehicle
                                )

                else:
                    item.update(
                        vehicle_id=vehicle,
                        driver_id=driver,
                        start_date=start_date,
                        created_by=user,
                        modified_by=user
                        )


                row_number += 1

    except Exception, ex:
        logger.exception(ex)

        raise Exception("Failed while processing row %d. Error was %s" % (row_number, ex))

def import_fuel_cards_data(user, fuel_card_file):
    row_number = 1

    try:
        with transaction.atomic():
            excel = ExcelHelper(content=fuel_card_file.file.read())

            headers = excel.read_header(1)

            row_number = 2
            while row_number <= excel.nrows:
                row = excel.read_row(row_number)
                row_data = dict(zip(headers, row))

                vehicle_reg = None if not row_data.get('reg') else row_data.get('reg')

                card_number = None if not row_data.get('fuel card 1') else row_data.get('fuel card 1')

                start_date = None if not row_data.get('start date') else row_data.get('start date')
                if start_date:
                    start_date = datetime.strptime(start_date, '%Y/%m/%d')

                vehicle = Vehicle.objects.filter(registration_number=row_data.get('reg')).values_list('id', flat=True).first()

                fuel_card = FuelCard.objects.filter(card_number=row_data.get('fuel card 1'))

                if not fuel_card.exists():
                    FuelCard.objects.create(
                        card_number =card_number,
                        vehicle_assigned_id=vehicle,
                        start_date=start_date,
                        created_by=user)

                else:

                    fuel_card.update(
                        card_number =card_number,
                        vehicle_assigned=vehicle,
                        start_date=start_date,)
                row_number += 1

    except Exception, ex:
        logger.exception(ex)
        raise Exception("Failed while processing row %d. Error was %s" % (row_number, ex))