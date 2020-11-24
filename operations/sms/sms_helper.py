import logging
from datetime import datetime, date
logger = logging.getLogger(__name__)

from models import SmsMessage
from fleet.models import *
from employees.models import *
from models import *
from django.conf import settings
import requests
from django.template.loader import render_to_string
from datetime import date
from datetime import datetime
import time
from django.db.models import Q

def queue_service_booking_sms(vehicle):

    vehicle = Vehicle.objects.get(licence_plate=vehicle)
    driver = vehicle.get_current_driver()      
    employee = Employee.objects.get(pk=driver.id) 
    if employee.designation.designation=="Regional Manager":
      phone = CardAllocation.objects.filter(~Q(mobile_number__isnull=True),employee=employee).order_by('-id').first()
    else:
      phone = CardAllocation.objects.filter(~Q(mobile_number__isnull=True),employee=employee.regional_manager).order_by('-id').first()    
    # employee_contact = Contact.objects.get(employee_id=driver.id)
    booking = ServiceBooking.objects.filter(vehicle=vehicle).order_by('-id').first()

    return queue_templated_sms(template_name="sms/new_service_booking.txt",
                               context={                                   
                                   'driver': employee.full_name,
                                   'vehicle':vehicle.vehicle,
                                   'service_date':booking.service_date,
                                   'garage':booking.garage,
                                   'mileage': booking.mileage
                               },

                               phone_number = phone.mobile_number.phone_number,
                               vehicle=vehicle,
                               driver=employee,
    )


def queue_templated_sms(template_name, context, phone_number=None, vehicle=None, driver=None):
    content = render_to_string(template_name, context)    
    return queue_sms(content, phone_number=phone_number, vehicle=vehicle, driver=driver)
    
def queue_sms(content, phone_number=None, vehicle=None, driver=None):

    if phone_number is None:
        raise Exception("Internal error: No phone number given for sms")
    
    sms = SmsMessage.objects.create(content=content,
                                    phone_number=phone_number,
                                    vehicle=vehicle,
                                    driver=driver,
                                    sent=None,
                                    created=date.today())

    send_sms = send_clickatel_sms(sms, phone_number)

    return sms

def send_clickatel_sms(sms, phone_number):    
    if settings.SMS_TEST_MODE:
        return

    params = {
        'text': sms.content,
        'to': phone_number,
        'api_id': settings.CLICKATEL_API_ID,
        'user': settings.CLICKATEL_USERNAME,
        'password': settings.CLICKATEL_PASSWORD
        }
    try:

        requests.get(settings.CLICKATEL_API_URL, params=params)
        sms.sent=True
        sms.save()
        return { 'status': 'ok', 'msg': None }
    except Exception, ex:
        logger.exception(ex)
        return { 'status': 'failed', 'msg': str(ex) }
        
