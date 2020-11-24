import os
import csv
import json
import xmltodict
from lib.excel_helper import ExcelHelper
from lib.file_handler import file_download, save_file
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from django.core.files import File
from django.http import HttpResponse
from models import Vehicle, Incident, InsuranceClaim
from datetime import datetime
from django.db import transaction
import sys
from django.db.models import Sum, Count
from django.db.models import Q, F, Case, When, FloatField, IntegerField, Value

reload(sys)
sys.setdefaultencoding('utf8')

import logging
logger = logging.getLogger(__name__)

def export_vehicle_data(user, sheet_name, vehicles, data):
    row_number = 1
    try:
        with transaction.atomic():           

            file_name = "Vehicle Extract - %s.csv" %(datetime.now().strftime("%Y%m%d_%H%M%S"))                
            csv_file = os.path.join(settings.MEDIA_ROOT, 'uploads/documents/', file_name)
            f = open(csv_file, "w+b")
            f.truncate()
            writer = csv.writer(f)

            writer.writerow(['Vehicles as of:', '{}'.format(datetime.strftime(datetime.now(), '%b %d, %Y'))])

            writer.writerow([''])

            headers = ['Ownership','Division','Status at Create','Make','Model',
                       'Year Model','Registration','Registration Date',
                       'Licence Expiry Date','Vin Number','Engine Number','Colour',
                       'Transmission','Fuel Type','Engine Capacity','Tank Capacity',
                       'Delivery Mileage','Aircon','Radio','Bluetooth','Jack','Spanner',
                       'Triangle']

            
            writer.writerow(headers)

            rows = [writer.writerow([v.get_ownership_display(),
                                     v.get_division_display(),
                                     v.get_status_at_create_display(),
                                     v.make.title() if v.make else '',
                                     v.model.title() if v.model else '',
                                     v.year_model,
                                     v.registration_number.upper() if v.registration_number else '',
                                     datetime.strftime(v.registration_date, '%d %b, %Y') \
                                                       if v.registration_date else '',
                                     datetime.strftime(v.licence_disk_expiry, '%d %b, %Y') \
                                                       if v.licence_disk_expiry else '',
                                     v.vin_number.upper() if v.vin_number else '',
                                     v.engine_number.upper() if v.engine_number else '',
                                     v.colour.title() if v.colour else '',
                                     v.get_transmission_display(),
                                     v.get_fuel_type_display(),
                                     v.engine_capacity,
                                     v.tank_capacity,
                                     v.delivery_mileage,
                                     'Yes' if v.has_aircon else 'No',
                                     'Yes' if v.has_radio else 'No',
                                     'Yes' if v.has_bluetooth else 'No',
                                     'Yes' if v.has_jack else 'No',
                                     'Yes' if v.has_spanner else 'No',
                                     'Yes' if v.has_triangle else 'No'])
                    for v in vehicles]
            
            return save_file(user, file_name, csv_file, "Download","Vehicles Extract")
        
    except Exception, ex:        
        logger.exception(ex)
        raise Exception("Failed while processing export. Error was %s" % (ex))



def extract_incident_data(user, incidents, data, traffic_fines = False):
    row_number = 1
    report_name = 'Incident Extract'
    if traffic_fines:
        report_name = 'Traffic Fine Extract'
                
    try:
        with transaction.atomic():
            file_name = '{} Extract - {}.csv'.format(report_name, datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'))
            
            csv_file = os.path.join(settings.MEDIA_ROOT, 'uploads/documents/', file_name)
            f = open(csv_file, "w+b")
            f.truncate()
            writer = csv.writer(f)
            
            writer.writerow(['{}s as of:'.format(report_name), '{}'.format(datetime.strftime(datetime.now(), '%b %d, %Y'))])

            writer.writerow([''])

            headers = ['Vehicle Registration Number', 'Vehicle Make', 'Vehicle Model', 'Driver Name', 'Description', 'Resolved', 'Cost', 'Incident Date']

            if not traffic_fines:
                headers = ['Vehicle Registration Number', 'Vehicle Make', 'Vehicle Model', 'Driver Name', 'Description', 'Resolved', 'Cost', 'Incident Date', 'Incident Type']

            writer.writerow(headers)
            rows = [writer.writerow([incident.vehicle.registration_number,
                                     incident.vehicle.make,
                                     incident.vehicle.model,
                                     incident.description,
                                     'Yes' if incident.resolved else 'No',
                                     incident.cost,
                                     datetime.strftime(incident.incident_date, '%d %b, %Y') \
                                                       if incident.incident_date else '',
                                     incident.incident_type if not traffic_fines else ""])
                    for incident in incidents]

            
            return save_file(user, file_name, csv_file, "Download",report_name)
        
    except Exception, ex:
        logger.exception(ex)
        raise Exception("Failed while processing export. Error was %s" % (ex))


def extract_employee_data(user, sheet_name, employees, data):

    row_number = 1

    try:
        with transaction.atomic():
            file_name = 'Drivers Extract - {}.csv'.format(
                datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'))
            csv_file = os.path.join(settings.MEDIA_ROOT, 'uploads/documents/', file_name)
            f = open(csv_file, "w+b")
            f.truncate()
            writer = csv.writer(f)

            writer.writerow(['Drivers as of:', '{}'.format(datetime.strftime(datetime.now(), '%b %d, %Y'))])

            writer.writerow([''])

            headers = ['First Name','Last Name','Employee Number','Commission Code','ID Number','Email']

            
            writer.writerow(headers)

            rows = [writer.writerow([emp.first_name,
                                     emp.last_name,
                                     emp.employee_no,
                                     emp.commission_code,
                                     emp.id_number,
                                     emp.email,
                                    ])
                    for emp in employees]

            
            return save_file(user, file_name, csv_file, "Download","Drivers Extract")
        
    except Exception, ex:
        logger.exception(ex)
        raise Exception("Failed while processing export. Error was %s" % (ex))

def extract_user_data(user, sheet_name, users, data):

    row_number = 1

    try:
        with transaction.atomic():
            file_name = 'User Extract - {}.csv'.format(
                datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'))
            csv_file = os.path.join(settings.MEDIA_ROOT, 'uploads/documents/', file_name)
            f = open(csv_file, "w+b")
            f.truncate()
            writer = csv.writer(f)

            writer.writerow(['Users as of:', '{}'.format(datetime.strftime(datetime.now(), '%b %d, %Y'))])

            writer.writerow([''])

            headers = ['User Name','First Name','Surname','Phone Number','Email']
            
            writer.writerow(headers)

            rows = [writer.writerow([emp.username,
                                     emp.first_name,
                                     emp.last_name,
                                     emp.phone_number,
                                     emp.email,
                                    ])
                    for emp in users]

            
            return save_file(user, file_name, csv_file, "Download","Users Extract")
        
    except Exception, ex:
        logger.exception(ex)
        raise Exception("Failed while processing export. Error was %s" % (ex))


def extract_fuel_card_usage_data(user, sheet_name, fuel_cards, total_usage,available, data):

    row_number = 1

    try:
        with transaction.atomic():
            file_name = 'Fuel Card Usage Extract - {}.csv'.format(
                datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'))
            print file_name
            print settings.MEDIA_ROOT
            csv_file = os.path.join(settings.MEDIA_ROOT, 'uploads/documents/', file_name)
            f = open(csv_file, "w+b")
            f.truncate()
            writer = csv.writer(f)

            writer.writerow(['Fuel Cards as of:', '{}'.format(datetime.strftime(datetime.now(), '%b %d, %Y %H:%M:%S'))])

            writer.writerow([''])

            headers = ['Driver', 'Registration Number', 'Card Number', 'Transaction Date', 
                       'Transaction','Transaction Number','Transaction Code', 
                       'Quantity', 'Opening Balance', 'Amount', 'Balance']
            totals = ['Total Fuel Usage | Available Balance','','','','','','','','',total_usage,available]
            
            writer.writerow(headers)

            for fuel_card in fuel_cards:
                trans_list = ''
                for trans in fuel_card.transaction_type.all():
                    if not trans_list == '':
                        trans_list += ', '+ trans.description
                    else:
                        trans_list += trans.description

                writer.writerow([fuel_card.driver.full_name if fuel_card.driver else '',
                                 fuel_card.vehicle.registration_number if fuel_card.vehicle else '',
                                 fuel_card.fuel_card.card_number if fuel_card.fuel_card else '',
                                 datetime.strftime(fuel_card.transaction_date, '%Y-%m-%d %H:%M:%S'),
                                 trans_list,
                                 fuel_card.transaction_number,
                                 fuel_card.transaction_code,
                                 fuel_card.quantity,
                                 fuel_card.opening_balance,
                                 fuel_card.amount,
                                 fuel_card.balance,
                                ])

            writer.writerow(totals)

            return save_file(user, file_name, csv_file, "Download","Fuel Cards Usage Extract")
        
    except Exception, ex:
        logger.exception(ex)
        raise Exception("Failed while processing export. Error was %s" % (ex))

def extract_fuel_card_usage_summary(user, sheet_name, fuel_cards, total_usage, data):

    row_number = 1

    try:
        with transaction.atomic():
            file_name = 'Driver Fuel Usage Summary Extract - {}.csv'.format(
                datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'))
            print file_name
            print settings.MEDIA_ROOT
            csv_file = os.path.join(settings.MEDIA_ROOT, 'uploads/documents/', file_name)
            f = open(csv_file, "w+b")
            f.truncate()
            writer = csv.writer(f)

            writer.writerow(['Driver fuel usage as of:', '{}'.format(datetime.strftime(datetime.now(), '%b %d, %Y'))])

            writer.writerow([''])

            headers = ['Card Number', 'Registration Number', 'Driver','Amount']
            
            writer.writerow(headers)

            rows = [writer.writerow([
                                     card['fuel_card__card_number'],
                                     card['vehicle__registration_number'],
                                     '{} {}'.format(card['driver__first_name'], card['driver__last_name']),
                                     card['sum_amount'],
                                    ])
                    for card in fuel_cards]
            writer.writerow(['Total Fuel Usage','','', total_usage])
            
            return save_file(user, file_name, csv_file, "Download","Driver Fuel Usage Summary Extract")
        
    except Exception, ex:
        logger.exception(ex)
        raise Exception("Failed while processing export. Error was %s" % (ex))    

def extract_fuel_cards(user, sheet_name, fuel_cards, data):

    row_number = 1

    try:
        with transaction.atomic():
            file_name = 'Fuel Cards Extract - {}.csv'.format(
                datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'))
            print file_name
            print settings.MEDIA_ROOT
            csv_file = os.path.join(settings.MEDIA_ROOT, 'uploads/documents/', file_name)
            f = open(csv_file, "w+b")
            f.truncate()
            writer = csv.writer(f)

            writer.writerow(['Fuel Cards as of:', '{}'.format(datetime.strftime(datetime.now(), '%b %d, %Y'))])

            writer.writerow([''])

            headers = ['Card Number', 'Registration Number', 'Driver', 'Card Type', 'Supplier', 'Status', 'Cancelled Date']
            
            writer.writerow(headers)

            rows = [writer.writerow([c.card_number,
                                     c.vehicle_assigned.registration_number if c.vehicle_assigned else "",
                                     c.driver.full_name if c.driver else "",
                                     c.card_type,
                                     c.vendor.name if c.vendor else "",
                                     c.status,
                                     datetime.strftime(c.cancelled_date, '%Y-%m-%d %H%M%S') if c.cancelled_date else "",
                                    ])
                    for c in fuel_cards]

            
            return save_file(user, file_name, csv_file, "Download","Fuel Cards Extract")
        
    except Exception, ex:
        logger.exception(ex)
        raise Exception("Failed while processing export. Error was %s" % (ex))

def extract_vehicle_maintenance_data(user, sheet_name, vehicle_maintenances, data):

    row_number = 1

    try:
        with transaction.atomic():
            file_name = 'Vehicle Maintenance Extract - {}.csv'.format(
                datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'))
            csv_file = os.path.join(settings.MEDIA_ROOT, 'uploads/documents/', file_name)
            f = open(csv_file, "w+b")
            f.truncate()
            writer = csv.writer(f)

            writer.writerow(['Vehicle Maintenances as of:', '{}'.format(datetime.strftime(datetime.now(), '%b %d, %Y'))])

            writer.writerow([''])

            headers = ['Vehicle Registration','Plan Type','End Date', 'End Mileage']

            
            writer.writerow(headers)

            rows = [writer.writerow([e.vehicle.registration_number,
                                     e.plan_type,
                                     datetime.strftime(e.end_date, '%d %b, %Y'),
                                     e.end_mileage,
                                    ])
                    for e in vehicle_maintenances]

            
            return save_file(user, file_name, csv_file, "Download","Vehicle Maintenance Extract")
        
    except Exception, ex:
        logger.exception(ex)
        raise Exception("Failed while processing export. Error was %s" % (ex))


def extract_insurer_vehicles_data(user, sheet_name, insurer, insured_vehicles, data):

    row_number = 1

    try:
        with transaction.atomic():
            file_name = '{} - Insurer Vehicles Extract - {}.csv'.format(insurer.name, datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'))
            csv_file = os.path.join(settings.MEDIA_ROOT, 'uploads/documents/', file_name)
            f = open(csv_file, "w+b")
            f.truncate()
            writer = csv.writer(f)

            writer.writerow(['Insurer Vehicles as of:', '{}'.format(datetime.strftime(datetime.now(), '%b %d, %Y'))])

            writer.writerow([''])

            headers = ['Vehicle Registration','Brocker Name', 'Insurance Type', 'Cover Amount', 'Installment']

            
            writer.writerow(headers)

            rows = [writer.writerow([v.vehicle.registration_number,
                                     v.broker_name,
                                     v.insurance_type,v.insured_amount,
                                     v.installment,
                                    ])
                    for v in insured_vehicles]

            
            return save_file(user, file_name, csv_file, "Download","Insurer Vehicle Extract")
        
    except Exception, ex:
        logger.exception(ex)
        raise Exception("Failed while processing export. Error was %s" % (ex))


def extract_insurers_data(user, sheet_name, insurers, data):

    row_number = 1

    try:
        with transaction.atomic():
            file_name = 'Insurers Extract - {}.csv'.format(datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'))
            csv_file = os.path.join(settings.MEDIA_ROOT, 'uploads/documents/', file_name)
            f = open(csv_file, "w+b")
            f.truncate()
            writer = csv.writer(f)

            writer.writerow(['Insurers as of:', '{}'.format(datetime.strftime(datetime.now(), '%b %d, %Y'))])

            writer.writerow([''])

            headers = ['Insurer','Contact First Name', 'Contact Last Name', 'Address Line 1',
                       'Address Line 2', 'Postal Code', 'City',
                       'Telephone', 'Cell', 'Email', 'Insured Vehicles']

            
            writer.writerow(headers)

            rows = [writer.writerow([i.name,
                                     i.contact_person.first_name, i.contact_person.last_name, 
                                     i.address.address_line_1, i.address.address_line_2,
                                     i.address.postal_code, i.address.city,
                                     i.contact_person.tel_number, i.contact_person.cell_number,
                                     i.contact_person.email, i.insured_vehicles()
                                    ])
                    for i in insurers]

            
            return save_file(user, file_name, csv_file, "Download","Insurers Extract")
        
    except Exception, ex:
        logger.exception(ex)
        raise Exception("Failed while processing export. Error was %s" % (ex))



def extract_tickets_data(user, sheet_name, tickets, data):
    
    row_number = 1

    try:
        with transaction.atomic():

            file_name = 'Tickets Extract - {}.csv'.format(

                datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'))
            csv_file = os.path.join(settings.MEDIA_ROOT, 'uploads/documents/', file_name)
            f = open(csv_file, "w+b")
            f.truncate()
            writer = csv.writer(f)

            writer.writerow(['Tickets as of:', '{}'.format(datetime.strftime(datetime.now(), '%b %d, %Y'))])

            writer.writerow([''])

            headers = ['Ticket Number','Created By','Status','Subject','Category','Technician','Create Date']

            
            writer.writerow(headers)


            rows = [writer.writerow([tkt.number,
                                     tkt.created_by.full_name,
                                     tkt.status,
                                     tkt.subject,
                                     tkt.category,
                                     tkt.technician,
                                     datetime.strftime(tkt.created_at, '%d %b, %Y'),
                                    ])
                    for tkt in tickets]

            
            return save_file(user, file_name, csv_file, "Download","Tickets Extract")
        
    except Exception, ex:
        logger.exception(ex)
        raise Exception("Failed while processing export. Error was %s" % (ex))



def extract_service_booking_data(user, sheet_name, service_bookings, data):

    row_number = 1

    try:
        with transaction.atomic():
            file_name = 'Service - Maintenance - {}.csv'.format(
                datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'))
            csv_file = os.path.join(settings.MEDIA_ROOT, 'uploads/documents/', file_name)
            f = open(csv_file, "w+b")
            f.truncate()
            writer = csv.writer(f)

            writer.writerow(['Service/Maintenance as of:', '{}'.format(datetime.strftime(datetime.now(), '%b %d, %Y'))])

            writer.writerow([''])

            headers = ['Vehicle Registration','Service/Maintenance Date','Comment']
          
            writer.writerow(headers)

            rows = [writer.writerow([e.vehicle.registration_number,
                                     datetime.strftime(e.service_date, '%d %b, %Y') if e.service_date else "",
                                     e.comment,
                                    ])
                    for e in service_bookings]
      
            return save_file(user, file_name, csv_file, "Download","Service/Maintenance Extract")
        
    except Exception, ex:
        logger.exception(ex)
        raise Exception("Failed while processing export. Error was %s" % (ex))

def extract_resolved_service_booking_data(user, sheet_name, service_bookings, data):

    row_number = 1

    try:
        with transaction.atomic():
            file_name = 'Resolved Service - Maintenance - {}.csv'.format(
                datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'))
            csv_file = os.path.join(settings.MEDIA_ROOT, 'uploads/documents/', file_name)
            f = open(csv_file, "w+b")
            f.truncate()
            writer = csv.writer(f)

            writer.writerow(['Resolved Service/Maintenance as of:', '{}'.format(datetime.strftime(datetime.now(), '%b %d, %Y'))])

            writer.writerow([''])

            headers = ['Vehicle Registration','Resolved Service/Maintenance Date','Comment']

            
            writer.writerow(headers)

            rows = [writer.writerow([e.vehicle.registration_number,
                                     datetime.strftime(e.follow_up_date, '%d %b, %Y') if e.follow_up_date else "",
                                     e.comment,
                                    ])
                    for e in service_bookings]

            
            return save_file(user, file_name, csv_file, "Download","Resolved Service/Maintenance Extract")
        
    except Exception, ex:
        logger.exception(ex)
        raise Exception("Failed while processing export. Error was %s" % (ex))

def extract_invoice_service_booking_data(user, sheet_name, service_bookings, data):

    row_number = 1

    try:
        with transaction.atomic():
            file_name = 'Invoice Service - Maintenance - {}.csv'.format(
                datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'))
            csv_file = os.path.join(settings.MEDIA_ROOT, 'uploads/documents/', file_name)
            f = open(csv_file, "w+b")
            f.truncate()
            writer = csv.writer(f)

            writer.writerow(['Invoice Service/Maintenance as of:', '{}'.format(datetime.strftime(datetime.now(), '%b %d, %Y'))])

            writer.writerow([''])

            headers = ['Vehicle Registration','Invoice Service/Maintenance Date','Comment']


            writer.writerow(headers)

            rows = [writer.writerow([e.vehicle.registration_number,
                                     datetime.strftime(e.follow_up_date, '%d %b, %Y') if e.follow_up_date else "",
                                     e.comment,
                                    ])
                    for e in service_bookings]


            return save_file(user, file_name, csv_file, "Download","Invoice Service/Maintenance Extract")

    except Exception, ex:
        logger.exception(ex)
        raise Exception("Failed while processing export. Error was %s" % (ex))

def extract_service_providers_data(user, sheet_name, service_providers, data):

    row_number = 1

    try:
        with transaction.atomic():
            file_name = 'Service Providers Extract - {}.csv'.format(datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'))
            csv_file = os.path.join(settings.MEDIA_ROOT, 'uploads/documents/', file_name)
            f = open(csv_file, "w+b")
            f.truncate()
            writer = csv.writer(f)

            writer.writerow(['Service Providers as of:', '{}'.format(datetime.strftime(datetime.now(), '%b %d, %Y'))])

            writer.writerow([''])

            headers = ['Service Provider','Contact First Name', 'Contact Last Name', 'Address Line 1',
                       'Address Line 2', 'Postal Code', 'City',
                       'Telephone', 'Cell', 'Email']

            
            writer.writerow(headers)

            rows = [writer.writerow([i.name,
                                     i.contact_person.first_name if i.contact_person else "",
                                     i.contact_person.last_name if i.contact_person else "", 
                                     i.address.address_line_1 if i.contact_person else "",
                                     i.address.address_line_2 if i.contact_person else "",
                                     i.address.postal_code if i.contact_person else "",
                                     i.address.city if i.contact_person else "",
                                     i.contact_person.tel_number if i.contact_person else "",
                                     i.contact_person.cell_number if i.contact_person else "",
                                     i.contact_person.email if i.contact_person else "",
                                    ])
                    for i in service_providers]

            
            return save_file(user, file_name, csv_file, "Download","Service Provider Extract")
        
    except Exception, ex:
        logger.exception(ex)
        raise Exception("Failed while processing export. Error was %s" % (ex))

def extract_vendors_data(user, sheet_name, vendors, data):

    row_number = 1

    try:
        with transaction.atomic():
            file_name = 'Service Providers Extract - {}.csv'.format(datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'))
            csv_file = os.path.join(settings.MEDIA_ROOT, 'uploads/documents/', file_name)
            f = open(csv_file, "w+b")
            f.truncate()
            writer = csv.writer(f)

            writer.writerow(['Service Providers as of:', '{}'.format(datetime.strftime(datetime.now(), '%b %d, %Y'))])

            writer.writerow([''])

            headers = ['Service Provider Name','Type', 'Contact First Name', 'Contact Last Name', 'Address Line 1',
                       'Address Line 2', 'Postal Code', 'City',
                       'Telephone', 'Cell', 'Email']

            
            writer.writerow(headers)

            rows = [writer.writerow([i.name,
                                     i.vendor_type,
                                     i.contact_person.first_name if i.contact_person else "",
                                     i.contact_person.last_name if i.contact_person else "", 
                                     i.address.address_line_1 if i.address else "",
                                     i.address.address_line_2 if i.address else "",
                                     i.address.postal_code if i.address else "",
                                     i.address.city if i.address else "",
                                     i.contact_person.tel_number if i.contact_person else "",
                                     i.contact_person.cell_number if i.contact_person else "",
                                     i.contact_person.email if i.contact_person else "",
                                    ])
                    for i in vendors]

            
            return save_file(user, file_name, csv_file, "Download","Service Providers Extract")
        
    except Exception, ex:
        logger.exception(ex)
        raise Exception("Failed while processing export. Error was %s" % (ex))

def extract_vehicle_makes_data(user, sheet_name,vehicle_makes, data):

    row_number = 1

    try:
        with transaction.atomic():
            file_name = 'Vehicle Makes Extract - {}.csv'.format(datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'))
            csv_file = os.path.join(settings.MEDIA_ROOT, 'uploads/documents/', file_name)
            f = open(csv_file, "w+b")
            f.truncate()
            writer = csv.writer(f)

            writer.writerow(['Vehicle Makes as of:', '{}'.format(datetime.strftime(datetime.now(), '%b %d, %Y'))])

            writer.writerow([''])

            headers = ['Make Name']

            
            writer.writerow(headers)

            rows = [writer.writerow([i.make_name
                                    ])
                    for i in vehicle_makes]

            
            return save_file(user, file_name, csv_file, "Download","Vehicle Makes Extract")
        
    except Exception, ex:
        logger.exception(ex)
        raise Exception("Failed while processing export. Error was %s" % (ex))


def extract_vehicle_models_data(user, sheet_name,vehicle_models, data):

    row_number = 1

    try:
        with transaction.atomic():

            file_name = 'Vehicle Models Extract - {}.csv'.format(datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'))
            csv_file = os.path.join(settings.MEDIA_ROOT, 'uploads/documents/', file_name)
            f = open(csv_file, "w+b")
            f.truncate()
            writer = csv.writer(f)

            writer.writerow(['Vehicle Models as of:', '{}'.format(datetime.strftime(datetime.now(), '%b %d, %Y'))])

            writer.writerow([''])

            headers = ['Make Name','Model Name']
            
            writer.writerow(headers)

            rows = [writer.writerow([i.make.make_name,
                                     i.model_name,
                                    ])
                    for i in vehicle_models]

            
            return save_file(user, file_name, csv_file, "Download","Vehicle Models Extract")
        
    except Exception, ex:
        logger.exception(ex)
        raise Exception("Failed while processing export. Error was %s" % (ex))


def extract_driving_licences_data(user, sheet_name, driving_licences, data):
    try:
        with transaction.atomic():
            file_name = 'Drivers Licence Extract - {}.csv'.format(datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'))
            csv_file = os.path.join(settings.MEDIA_ROOT, 'uploads/documents/', file_name)
            f = open(csv_file, "w+b")
            f.truncate()
            writer = csv.writer(f)

            writer.writerow(['Drivers Licence as of:', '{}'.format(datetime.strftime(datetime.now(), '%b %d, %Y'))])

            writer.writerow([''])

            headers = ['Driver','Registration Number','Licence Number','Code','Date Of Issue','Expiry Date']

            writer.writerow(headers)

            rows = [writer.writerow([dl.employee.full_name,
                                     dl.employee.vehicle.registration_number if dl.employee.vehicle else "",
                                     dl.licence_number,
                                     dl.code,
                                     datetime.strftime(dl.date_of_issue, '%d %b, %Y') if dl.date_of_issue else "",
                                     datetime.strftime(dl.expiry_date, '%d %b, %Y') if dl.expiry_date else "",
                                    ])
                    for dl in driving_licences]

            
            return save_file(user, file_name, csv_file, "Download","Drivers Licence Extract")
    except Exception, ex:
        logger.exception(ex)
        raise Exception("Failed while processing export. Error was %s" % (ex))


def extract_insurance_claims_data(user, sheet_name, insurance_claims, data):
    try:
        with transaction.atomic():
            file_name = 'Insurance Claim Extract - {}.csv'.format(datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'))
            csv_file = os.path.join(settings.MEDIA_ROOT, 'uploads/documents/', file_name)
            f = open(csv_file, "w+b")
            f.truncate()
            writer = csv.writer(f)

            writer.writerow(['Insurance Claim as of:', '{}'.format(datetime.strftime(datetime.now(), '%b %d, %Y'))])

            writer.writerow([''])

            headers = ['Insurance','Registration Number','Quote Reference Number','Claim Reference Number','Claim Type','Incident Date']

            writer.writerow(headers)
            
            rows = [writer.writerow([ic.vendor.name,
                                     ic.vehicle.registration_number,
                                     ic.quote_reference_number,
                                     ic.insurance_reference_number,
                                     ic.claim_type,
                                     datetime.strftime(ic.incident_date, '%d %b, %Y') if ic.incident_date else "",
                                    ]) 
                    for ic in insurance_claims]

            
            return save_file(user, file_name, csv_file, "Download","Insurance Claims Extract")

    except Exception, ex:
        logger.exception(ex)
        raise Exception("Failed while processing export. Error was %s" % (ex))


def extract_stock_items_data(user, sheet_name, stock_items, data):
    try:
        with transaction.atomic():
            file_name = 'Stock Items Extract - {}.csv'.format(datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'))
            csv_file = os.path.join(settings.MEDIA_ROOT, 'uploads/documents/', file_name)
            f = open(csv_file, "w+b")
            f.truncate()
            writer = csv.writer(f)

            writer.writerow(['Stock Items as of:', '{}'.format(datetime.strftime(datetime.now(), '%b %d, %Y'))])

            writer.writerow([''])

            writer = csv.writer(f)

            headers = ['Stock Item','Category','Stock Balance']

            writer.writerow(headers)
            
            rows = [writer.writerow([item.item_name,
                                     item.category if item.category else "",
                                     item.stock_quantity,
                                    ]) 
                    for item in stock_items]
            
            return save_file(user, file_name, csv_file, "Download","Stock Items Extract")
    except Exception, ex:
        logger.exception(ex)
        raise Exception("Failed while processing export. Error was %s" % (ex))


def extract_stock_items_received_data(user, sheet_name, stock_items, data):
    try:
        with transaction.atomic():
            file_name = 'Stock Items Received Extract - {}.xlsx'.format(datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'))
            csv_file = os.path.join(settings.MEDIA_ROOT, 'uploads/documents/', file_name)
            f = open(csv_file, "w+b")
            f.truncate()
            writer = csv.writer(f)

            writer.writerow(['Stock Items Received as of:', '{}'.format(datetime.strftime(datetime.now(), '%b %d, %Y'))])

            writer.writerow([''])

            headers = ['Stock Item','Category','Reference', 'Stock Opening Balance', 
                       'Stock Received', 'Stock Closing Balance', 'Date Received', 'Supplier']

            writer.writerow(headers)
            
            rows = [writer.writerow([item.stock_item.item_name,
                                     item.stock_item.category if item.stock_item.category else "",
                                     item.reference,
                                     item.opening_stock_quantity,
                                     item.received_stock_quantity,
                                     item.stock_balance,
                                     datetime.strftime(item.date_received, '%Y-%m-%d'),
                                     item.supplier.name,
                                    ]) 
                    for item in stock_items]
            
            return save_file(user, file_name, csv_file, "Download","Stock Items Received Extract")
    except Exception, ex:
        logger.exception(ex)
        raise Exception("Failed while processing export. Error was %s" % (ex))


def extract_stock_items_allocated_data(user, sheet_name, stock_items, data):
    try:
        with transaction.atomic():
            file_name = 'Stock Items Allocated Extract - {}.xlsx'.format(datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'))
            csv_file = os.path.join(settings.MEDIA_ROOT, 'uploads/documents/', file_name)
            f = open(csv_file, "w+b")
            f.truncate()
            writer = csv.writer(f)

            writer.writerow(['Stock Items Allocated as of:', '{}'.format(datetime.strftime(datetime.now(), '%b %d, %Y'))])

            writer.writerow([''])

            headers = ['Stock Item','Category', 'Stock Opening Balance', 
                       'Stock Received', 'Stock Closing Balance', 'Date Received', 'Allocated To']

            writer.writerow(headers)
            
            rows = [writer.writerow([item.stock_item.item_name,
                                     item.stock_item.category if item.stock_item.category else "",
                                     item.opening_stock_quantity,
                                     item.allocated_stock_quantity,
                                     item.stock_balance,
                                     datetime.strftime(item.date_allocated, '%Y-%m-%d'),
                                     item.district.branch_name,
                                    ]) 
                    for item in stock_items]

            return save_file(user, file_name, csv_file, "Download","Stock Items Allocated Extract")
    except Exception, ex:
        logger.exception(ex)
        raise Exception("Failed while processing export. Error was %s" % (ex))

def extract_asset_data(user, sheet_name, assets, data):

    row_number = 1

    try:
        with transaction.atomic():
            file_name = 'Asset Extract - {}.csv'.format(
                datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S'))
            csv_file = os.path.join(settings.MEDIA_ROOT, 'uploads/documents/', file_name)
            f = open(csv_file, "w+b")
            f.truncate()
            writer = csv.writer(f)

            writer.writerow(['Assets as of:', '{}'.format(datetime.strftime(datetime.now(), '%b %d, %Y'))])

            writer.writerow([''])

            headers = ['Model','Make','Serial Number','Condition','Status']
            
            writer.writerow(headers)

            rows = [writer.writerow([emp.model,
                                     emp.make,
                                     emp.serial_number,
                                     emp.condition,
                                     emp.status,
                                    ])
                    for emp in assets]

            
            return save_file(user, file_name, csv_file, "Download","Assets Extract")
        
    except Exception, ex:
        logger.exception(ex)
        raise Exception("Failed while processing export. Error was %s" % (ex))

def extract_vehicle_service_due_data(user, vehicles):
    row_number = 1
    try:
        with transaction.atomic():           

            file_name = "Vehicle Service Due Extract - %s.csv" %(datetime.now().strftime("%Y%m%d_%H%M%S"))                
            csv_file = os.path.join(settings.MEDIA_ROOT, 'uploads/documents/', file_name)
            f = open(csv_file, "w+b")
            f.truncate()
            writer = csv.writer(f)

            writer.writerow(['Vehicles Due For Service as of:', '{}'.format(datetime.strftime(datetime.now(), '%b %d, %Y'))])

            writer.writerow([''])

            headers = ['Division','Status','Registration Number','Make','Model','Year Model',
                       'Registration Date','License Expiry Date','VIN Number','Engine Number',
                       'Colour','Current Mileage','Service Interval']

            
            writer.writerow(headers)

            rows = [writer.writerow([v.get_division_display(),
                                     v.get_status_at_create_display(),
                                     v.registration_number.upper() if v.registration_number else '',
                                     v.make.title() if v.make else '',
                                     v.model.title() if v.model else '',
                                     v.year_model,                                     
                                     datetime.strftime(v.registration_date, '%d %b, %Y') \
                                                       if v.registration_date else '',
                                     datetime.strftime(v.licence_disk_expiry, '%d %b, %Y') \
                                                       if v.licence_disk_expiry else '',
                                     v.vin_number.upper() if v.vin_number else '',
                                     v.engine_number.upper() if v.engine_number else '',
                                     v.colour.title() if v.colour else '',
                                     v.updated_mileage if v.updated_mileage else '',
                                     v.service_interval if v.service_interval else ''])
                    for v in vehicles]
            
            return save_file(user, file_name, csv_file, "Download","Vehicles Service Due Extract")
        
    except Exception, ex:        
        logger.exception(ex)
        raise Exception("Failed while processing export. Error was %s" % (ex))    
