from django import http
from django.template.loader import render_to_string, get_template
from django.template import RequestContext, Context
from django.conf import settings
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from django.core.mail import send_mail, EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, render_to_response
from django.core.urlresolvers import reverse
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from datetime import datetime, timedelta, date
from django.views.decorators.csrf import csrf_exempt
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

import csv
import os
from xhtml2pdf import pisa
import cStringIO as StringIO
import cgi
from .forms import *                      
from fleet.models import *
from assets.models import *
from employees.models import Employee, Contact
from offices.models import Branch, Region
from django.db.models import Count, Sum, Q
import collections
import json
import re
from sms.sms_helper import *

from unidecode import unidecode

def imports(request):
    upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')
    context = {
    	'title':"Data Imports",
        "upload_file_form": upload_file_form,

    }

    post = request.POST
    if request.POST:        
        if post.get('upload', None):
            if request.POST.get('update_current_driver', None):
                update_current_driver(request)
            if request.POST.get('update_fuel_card_allocation', None):
                update_fuel_card_allocation(request)
            if request.POST.get('update_commission', None):
                update_commission(request)

            validated = upload_file_form.is_valid()             
            if validated:                   
                uploaded = upload_file_form.save(commit=False)              
                uploaded.file_name = uploaded.file.name
                uploaded.transaction = "Data Imports"
                uploaded.save()

                file = '%s/%s'% (settings.MEDIA_ROOT, uploaded.file) 

                if request.POST.get('vehicles', None):
                    import_vehicle(request, file)
                if request.POST.get('vehicle_allocations', None):
                    import_vehicle_allocations(request, file)
                if request.POST.get('vehicle_incidences', None):
                    import_incidences(request, file)
                if request.POST.get('fuel_cards', None):
                    import_fuel_cards(request, file) 
                if request.POST.get('vehicle_inspections', None):
                    import_inspections(request, file)
                if request.POST.get('vehicle_maintenance', None):              
                    import_maint_data(request, file)   
                if request.POST.get('service_bookins', None):
                    import_service_bookings(request, file)
                if request.POST.get('traffic_fines', None):
                    import_traffic_fines(request, file) 
                if request.POST.get('vehicle_claims', None):
                    import_claims(request, file)
           
                  
                if request.POST.get('assets', None):
                    import_assets(request, file)

                if request.POST.get('regions', None):
                    import_regions(request, file)
                if request.POST.get('branches', None):
                    import_branches(request, file)
                if request.POST.get('departments', None):
                    import_departments(request, file)
                if request.POST.get('floors', None):
                    import_floors(request, file)
                if request.POST.get('sections', None):
                    import_sections(request, file)
                if request.POST.get('meters', None):
                    import_meters(request, file)

                if request.POST.get('designations', None):
                    import_designations(request, file)
                if request.POST.get('employees', None):
                    import_employees(request, file)

                if request.POST.get('employees_update', None):
                    update_employees(request, file)
                if request.POST.get('employee_contact', None):
                    employee_contacts(request, file)

                if request.POST.get('mobiles', None):
                    import_mobiles(request, file)               

                if request.POST.get('fuel_usage', None):
                    import_fuel_usage(request, file)    

                if request.POST.get('mk_Sl_drivers', None):
                    import_mk_Sl_drivers(request, file)  
           
                    

       	context ={
       		'title':"Records successfully imported",
       		"upload_file_form": upload_file_form,
       	}
    return render(request, "imports.html", context)

def import_mk_Sl_drivers(request, import_file):
    upload_list = []
    dataReader = csv.reader(open(import_file), delimiter=',', quotechar='"') 
    flag = False 
    x=0    
    emps = Employee.objects.all()
    for emp in emps:
        emp.department = Department.objects.filter(department="Sales").first()
        emp.save()
    for row in dataReader:
        if "Extract" in row[0] or "Extracted" in row[0]  or "Code" in row[0] or row[0]=="":
            continue
        employee = Employee.objects.filter(commission_code=row[0]) 
        if len(employee) > 0:
            employee = employee.first()            
            employee.commission_code=row[0].replace("'","")
            employee.first_name= row[1].replace("'","")
            employee.national_id=row[2].replace("'","")
            if row[4]:
                region = Region.objects.get(region=row[4].replace("'",""))
            if not row[4]:
                employee.branch=Branch.objects.get(branch="Unknown Branch")
            elif region.region=="Western Cape":
                employee.branch=Branch.objects.get(branch="Head Office")
            else:
                employee.branch = Branch.objects.get(region=region, office_type="RO")
            if row[3]:   
                code = row[3].replace("'","")             
                employee.designation = Designation.objects.filter(prefix=code).first()
            if row[6]:
                code = row[6].replace("'","")  
                employee.department = Department.objects.filter(department=code).first()
                                 
            employee.save()
            x +=1
            print (x,employee.first_name, ' updated')

            upload_list.append(employee) 
        else: 

            employee = Employee()            
            employee.commission_code=row[0].replace("'","")
            employee.first_name= row[1].replace("'","")
            employee.national_id=row[2].replace("'","")
            if row[4]:
                region = Region.objects.get(region=row[4].replace("'",""))
            if not row[4]:
                employee.branch=Branch.objects.get(branch="Unknown Branch")
            elif region.region=="Western Cape":
                employee.branch=Branch.objects.get(branch="Head Office")
            else:
                employee.branch = Branch.objects.get(region=region, office_type="RO")
            if row[3]:   
                code = row[3].replace("'","")             
                employee.designation = Designation.objects.filter(prefix=code).first()
            if row[6]:
                code = row[6].replace("'","")  
                employee.department = Department.objects.filter(department=code).first()

            employee.save()
            x +=1  
            print(x,employee.first_name, ' imported')

            upload_list.append(employee) 

    return upload_list 


def update_commission(request):
    employees =  Employee.objects.all()
    for employee in employees:
        employee.commission_code = employee.commission_code.replace("'","")
        employee.save()
        print('updated')

def import_maint_data(request, import_file):
    transaction_date = datetime.strptime("2017-02-01","%Y-%m-%d").date()
    VehicleMaintenance.objects.filter(maint_date__gte=transaction_date).delete()
    print("maintenance deleted", len(VehicleMaintenance.objects.filter(maint_date__gte=transaction_date)))
    ServiceBooking.objects.filter(service_date__gte=transaction_date).delete()
    print("bookings deleted",len(ServiceBooking.objects.filter(service_date__gte=transaction_date)))
    upload_list = []
    unimported = []
    dataReader = csv.reader(open(import_file), delimiter=',', quotechar='"') 
    x=0  
    for row in dataReader:
        if row[0] == "" or row[1]== "" or row[5]== "":
            x+=1
            print(x, "Row skipped")
            continue
        vehicle = Vehicle.objects.filter(licence_plate=row[1].replace("'","")).first() 
        transaction_date = datetime.strptime(row[0].replace("'",""),"%Y-%m-%d").date()
        if vehicle:
            vehicle_allocation = VehicleAllocation.objects.filter(vehicle=vehicle, allocation_date__lte=transaction_date).order_by('-allocation_date').first()
            if vehicle_allocation:
                employee = vehicle_allocation.driver
            else:
                vehicle_allocation = VehicleAllocation.objects.filter(vehicle=vehicle).order_by('allocation_date').first()
                if vehicle_allocation:
                    employee = vehicle_allocation.driver
                else:
                    employee = vehicle.get_current_driver()
            if employee:
                if 'Service' in row[5]:
                    booking = ServiceBooking()#.objects.get_or_create(vehicle=vehicle, driver=employee, booking_date=transaction_date)
                    booking.booking_date = transaction_date
                    booking.service_date = transaction_date
                    booking.vehicle = vehicle
                    booking.driver = employee
                    booking.service_type = "Minor"
                    booking.service_description = row[3].replace("'","")
                    booking.garage = row[2].replace("'","")
                    booking.mileage = float(row[4])
                    booking.next_service_mileage = int(int(row[4]) + int(vehicle.make_n_model.service_interval))
                    booking.serviced = True
                    booking.created_by = request.user
                    booking.save()

                    latest_booking =  ServiceBooking.objects.order_by('-id')[0]

                    maintenance = VehicleMaintenance()#.get_or_create(vehicle=vehicle, driver=employee, maint_date=transaction_date, actual_cost=float(row[6]))
                    maintenance.maint_date = transaction_date
                    maintenance.maint_type = row[5].replace("'","")
                    maintenance.vehicle = vehicle
                    if row[4]: 
                        maintenance.current_mileage=int(row[4])
                    maintenance.driver = employee
                    maintenance.description = row[3].replace("'","")
                    maintenance.projected_cost = float(row[6])
                    maintenance.actual_cost = float(row[6])
                    maintenance.difference = 0
                    maintenance.status = "Good Condition"
                    maintenance.service_provider = row[2].replace("'","")
                    maintenance.service_booking_number = latest_booking
                    maintenance.accept = True
                    maintenance.authorize = "Aproved"
                    maintenance.created_by = request.user
                    maintenance.save()
                    upload_list.append(maintenance)
                    x+=1
                    print(x, vehicle, "Booking And Maintenance Imported")

                else:

                    maintenance = VehicleMaintenance()#.get_or_create(vehicle=vehicle, driver=employee, maint_date=transaction_date, actual_cost=float(row[6]))
                    maintenance.maint_date = transaction_date
                    maintenance.maint_type = row[5].replace("'","")
                    maintenance.vehicle = vehicle
                    if row[4]:
                        maintenance.current_mileage=int(row[4])
                    maintenance.driver = employee
                    maintenance.description = row[3].replace("'","")
                    maintenance.projected_cost = float(row[6])
                    maintenance.actual_cost = float(row[6])
                    maintenance.difference = 0
                    maintenance.status = "Good Condition"
                    maintenance.service_provider = row[2]                
                    maintenance.accept = True
                    maintenance.authorize = "Aproved"
                    maintenance.created_by = request.user
                    maintenance.save()
                    upload_list.append(maintenance) 
                    x+=1
                    print(x, vehicle, "Maintenance Imported")
            


        else:
            x+=1
            print(x, row[1], "Not Imported") 

    return upload_list 



def import_fuel_cards(request, import_file):
    upload_list = []
    dataReader = csv.reader(open(import_file), delimiter=',', quotechar='"')   
    capture_date = date.today()
    for row in dataReader:
        if not row[0] == "TransactionType":
            fuel_card_count = FuelCard.objects.filter(card_number=row[0]).count()
            if fuel_card_count ==0:
                fuel_card = FuelCard()
                fuel_card.card_number = row[0]
                fuel_card.card_type = row[1]
                fuel_card.save() 
                upload_list.append(fuel_card) 

    return upload_list  


def import_fuel_usage(requests, import_file):
    upload_list = []
    unimported = []
    dataReader = csv.reader(open(import_file), delimiter=',', quotechar='"') 
    x=0  
    for row in dataReader:
        if "FleetNodeNumber" in row[0] or "TOTALS" in row[0] or row[0] == "":
            continue
        vehicle = Vehicle.objects.filter(licence_plate=row[2].replace("'","")).first() 
        transaction_date = datetime.strptime(row[9].replace("'",""),"%Y-%m-%d").date()
        if vehicle:
            vehicle_allocation = VehicleAllocation.objects.filter(vehicle=vehicle, allocation_date__lte=transaction_date).order_by('-allocation_date').first()
            if vehicle_allocation:
                employee = vehicle_allocation.driver
            else:
                employee = vehicle.current_driver

            usage = FuelUsage()
            usage.fleet_node_number=row[0]
            usage.fms_account_number=row[1]
            
            usage.vehicle = vehicle

            fuel_card = FuelCard.objects.filter(card_number=row[3].replace("'",""))
            if len(fuel_card) == 0:
                fc = FuelCard()
                fc.card_number = row[3]
                fc.card_type = "Absa Fleet"
                fc.save()

                ca = CardAllocation()            
                ca.allocation_type = "Allocate Fuel Card"            
                ca.allocation_date = datetime.now()
               
                ca.employee = employee
                ca.fuel_card = fc
                des = employee.designation
                if des =="Sales Manager" or des=="Regional Manager" or des=="Regional Sales Manager":
                    ca.fuel_cycle_limit=5000
                else:
                    ca.fuel_cycle_limit=7000
                ca.save()
                usage.fuel_card = fc
            else:
                usage.fuel_card = fuel_card.first()

            usage.driver = employee
            usage.cost_center_number = row[5]
            usage.cost_centre_name = row[6]
            usage.client_reference_1 = row[7]
            usage.client_reference_2 = row[8]
            usage.transaction_date = transaction_date
            usage.transaction_number = row[10]
            usage.merchant_name =  row[11]
            usage.transaction_code = row[12]
            usage.transaction_description = row[13]
            usage.odometer_reading = row[14]
            usage.distance_travelled = row[15]
            usage.quantity = row[16]
            usage.amount = row[17].replace("R","")
            usage.private_usage = row[18]
            usage.inhouse_indicator =  row[19]
            usage.current_usage = row[20]
            usage.save()
            x +=1
            print (x, usage.vehicle, usage.driver) 
            upload_list.append(usage)
        else:
            x +=1
            print(x, row[2], "Not imported") 
            unimported.append(row)
    print unimported
    return upload_list 

def import_mobiles(request, import_file):
    upload_list = []
    dataReader = csv.reader(open(import_file), delimiter=',', quotechar='"')   
  
    for row in dataReader:
        if not row[0] == "MSISDN":
            number = MobileNumber()
            number.phone_number=row[0]
            number.sim_number=row[1]
            number.service_provider = row[2]
            number.active=int(row[3])
            number.created_by=request.user
            number.modified_by=request.user
            
            number.save() 
            upload_list.append(number) 

    return upload_list 

def update_current_driver(request):

    vehicles=Vehicle.objects.all()
    for v in vehicles:
        current_driver = v.get_current_driver()
        if current_driver != "Not Allocated":        
            v.current_driver=v.get_current_driver()
        else:
            v.current_driver=None
        v.save()
        print (v.licence_plate, v.current_driver,' updated')

def update_fuel_card_allocation(request):
    allocations = VehicleAllocation.objects.all()
    for a in allocations:
        ca = CardAllocation()
        if a.transaction_type=="Allocated":
            ca.allocation_type = "Allocate Fuel Card"
        if a.transaction_type=="Returned" or a.transaction_type=="Returned_To_SP":
            ca.allocation_type = "Return Fuel Card"
        ca.allocation_date = a.allocation_date
        ca.employee = a.driver
        ca.fuel_card = a.fuel_card
        des = a.driver.designation
        if des =="Sales Manager" or des=="Regional Manager" or des=="Regional Sales Manager":
            ca.fuel_cycle_limit=5000
        else:
            ca.fuel_cycle_limit=7000
        ca.save()
        print('card allocation saved for ',ca.fuel_card)


def employee_contacts(request, import_file):
    upload_list = []
    dataReader = csv.reader(open(import_file), delimiter=';', quotechar='"')   
    capture_date = date.today()
    for row in dataReader:
        if not row[0] == "id":
            if not row[14]=="0":
                contact = Contact()
                contact.id = row[0]           
                contact.email = row[1]
                contact.celphone =row[2]
                contact.telephone = row[3]
                contact.fax = row[4]           
                contact.res_address1 = row[5] 
                contact.res_address2 = row[6]
                contact.res_address3 = row[7] 
                contact.res_address4 = row[8] 
                contact.res_address_postal_code = row[9]
                contact.postal_address1 = row[10]
                contact.postal_address2 = row[11]  
                contact.postal_address3 = row[12]
                contact.postal_postal_code = row[13]
                contact.employee = Employee.objects.get(pk=row[14]) 

                contact.save() 
                upload_list.append(contact) 

    return upload_list 

def update_employees(request, import_file):
    upload_list = []
    dataReader = csv.reader(open(import_file), delimiter=',', quotechar='"') 
    x=0  
    for row in dataReader:

        if "Extract" in row[0] or row[0] == "Extracted:" or "id" in row[0] or row[0] == "Code":
            continue

        employee = Employee.objects.get(pk=int(row[0]))
        
        # if row[1]:
        #     fn=row[1]
        # if row[2]:
        #     fn = fn + ' '+ row[2]
        # if row[3]:
        #     fn = fn + ' '+ row[3]                
        # employee.first_name=fn
        employee.commission_code=row[7]
        if row[8]:
            employee.national_id=row[8]

        if row[7]: 
            employee.branch = Branch.objects.get(id=row[10])                             
        employee.save()
        x +=1
        print (x, ' updated')

        upload_list.append(employee) 
      
            

    return upload_list 


def import_employees(request, import_file):
    upload_list = []
    dataReader = csv.reader(open(import_file), delimiter=',', quotechar='"') 
    flag = False 
    x=0
    des= request.POST.get('designation', None)
    for row in dataReader:
        if "Extract" in row[0] or "Extracted" in row[0]  or "Code" in row[0] or row[0]=="":
            continue
        employee = Employee.objects.filter(commission_code=row[0]) 
        if len(employee) > 0:
            employee = employee.first()            
            employee.commission_code=row[0].replace("'","")
            employee.first_name= row[2].replace("'","")
            employee.national_id=row[3].replace("'","")
            employee.designation=Designation.objects.get(id=des)
            if row[4]:
                region = Region.objects.get(region=row[4][5:])
            if not row[4]:
                employee.branch=Branch.objects.get(branch="Unknown Branch")
            elif region.region=="Western Cape":
                employee.branch=Branch.objects.get(branch="Head Office")
            else:
                employee.branch = Branch.objects.get(region=region, office_type="RO")
            if row[15]:
                code = row[15].replace("'","").split(' -', 1)[0]
                employee.regional_manager = Employee.objects.filter(commission_code=code).first()
            if row[16]:
                code = row[16].replace("'","").split(' -', 1)[0]
                employee.regional_sales_manager = Employee.objects.filter(commission_code=code).first()
            if row[17]:
                code = row[17].replace("'","").split(' -', 1)[0]
                employee.regional_admin_manager = Employee.objects.filter(commission_code=code).first()
            if row[18]:
                code = row[18].replace("'","").split(' -', 1)[0]
                employee.branch_manager = Employee.objects.filter(commission_code=code).first()
            if row[19]:
                code = row[19].replace("'","").split(' -', 1)[0]
                employee.district_manager = Employee.objects.filter(commission_code=code).first()
            if row[20]:
                code = row[20].replace("'","").split(' -', 1)[0]
                employee.assistant_district_manager = Employee.objects.filter(commission_code=code).first()   
                      
            employee.save()
            x +=1
            print (x, ' updated')

            upload_list.append(employee) 
        else: 

            employee = Employee()            
            employee.commission_code=row[0].replace("'","")
            employee.first_name= row[2].replace("'","")
            employee.national_id=row[3].replace("'","")
            employee.designation=Designation.objects.get(id=des)
            if row[4]:
                region = Region.objects.get(region=row[4][5:])
            if not row[4]:
                employee.branch=Branch.objects.get(branch="Unknown Branch")
            elif region.region=="Western Cape":
                employee.branch=Branch.objects.get(branch="Head Office")
            else:
                employee.branch = Branch.objects.get(region=region, office_type="RO")
            if row[15]:
                code = row[15].replace("'","").split(' -', 1)[0]
                employee.regional_manager = Employee.objects.filter(commission_code=code).first()
            if row[16]:
                code = row[16].replace("'","").split(' -', 1)[0]
                employee.regional_sales_manager = Employee.objects.filter(commission_code=code).first()
            if row[17]:
                code = row[17].replace("'","").split(' -', 1)[0]
                employee.regional_admin_manager = Employee.objects.filter(commission_code=code).first()
            if row[18]:
                code = row[18].replace("'","").split(' -', 1)[0]
                employee.branch_manager = Employee.objects.filter(commission_code=code).first()
            if row[19]:
                code = row[19].replace("'","").split(' -', 1)[0]
                employee.district_manager = Employee.objects.filter(commission_code=code).first()
            if row[20]:
                code = row[20].replace("'","").split(' -', 1)[0]
                employee.assistant_district_manager = Employee.objects.filter(commission_code=code).first()    

            employee.save()
            x +=1  
            print(x, ' imported')

            upload_list.append(employee) 

    return upload_list 


def import_designations(request, import_file):
    upload_list = []
    dataReader = csv.reader(open(import_file), delimiter=',', quotechar='"')
  
  
    for row in dataReader:
        if not row[0] == "id":
            designation = Designation.objects.filter(id=row[0])
            if len(designation)>0: 
                designation = Designation.objects.filter(id=row[0]).first()               
                designation.designation=row[1]
                designation.prefix=row[2]
                designation.save() 
                upload_list.append(designation) 
            else:
                designation = Designation()
                designation.designation=row[1]
                designation.prefix=row[2]
            
                designation.save() 

                upload_list.append(designation) 

    return upload_list 



def import_meters(request, import_file):
    upload_list = []
    dataReader = csv.reader(open(import_file), delimiter=';', quotechar='"')   
  
    for row in dataReader:
        if not row[0] == "id":
            meter = ElectricityMeterNumber()
            meter.meter_number=row[1]
            meter.meter_type=row[2]
            meter.service_provider=row[3]
            meter.branch = Branch.objects.get(pk=row[4])
            meter.save() 
            upload_list.append(meter) 

    return upload_list 


def import_sections(request, import_file):
    upload_list = []
    dataReader = csv.reader(open(import_file), delimiter=',', quotechar='"')   
  
    for row in dataReader:
        if not row[0] == "id":
            section = Section()
            section.section_no=row[1]
            section.description=row[2]
            section.floor = Floor.objects.get(pk=row[3])
            section.save() 
            upload_list.append(section) 

    return upload_list 


def import_floors(request, import_file):
    upload_list = []
    dataReader = csv.reader(open(import_file), delimiter=',', quotechar='"')   
  
    for row in dataReader:
        if not row[0] == "id":
            floor = Floor()
            floor.floor=row[1]
            floor.branch = Branch.objects.get(pk=row[2])
            floor.save() 
            upload_list.append(floor) 

    return upload_list 


def import_departments(request, import_file):
    upload_list = []
    dataReader = csv.reader(open(import_file), delimiter=';', quotechar='"')   
  
    for row in dataReader:
        if not row[0] == "id":
            department = Department()
            
            department.department = row[1]
            department.prefix = row[2]
           
            department.save() 
            upload_list.append(department) 

    return upload_list  


def import_branches(request, import_file):
    upload_list = []
    dataReader = csv.reader(open(import_file), delimiter=';', quotechar='"')   
  
    for row in dataReader:
        if not row[0] == "id":
            branch = Branch()
            branch.branch = row[1]
            branch.prefix = row[2]
            branch.office_type = row[3]
            branch.email = row[4]
            branch.celphone = row[5]
            branch.address = row[6]
            branch.street_address = row[7]
            branch.suburb = row[8]
            branch.city = row[9]
            branch.postal_code = row[10]
            branch.telephone = row[11]
            branch.telephone2 = row[12]
            branch.telephone3 = row[13]
            branch.telephone4 = row[14]
            branch.fax = row[15]
            branch.fax2 = row[16]
            branch.region = Region.objects.get(pk=row[17])
            branch.save() 
            upload_list.append(branch) 
    return upload_list 


def import_regions(request, import_file):
    upload_list = []
    dataReader = csv.reader(open(import_file), delimiter=';', quotechar='"')   
  
    for row in dataReader:
        if not row[0] == "id":
            region = Region()

            region.region = row[1]
            region.prefix = row[2]
            region.save() 
            upload_list.append(region) 

    return upload_list  



def import_assets(request, import_file):
    upload_list = []
    dataReader = csv.reader(open(import_file), delimiter=',', quotechar='"')   
  
    for row in dataReader:
        if not row[0] == "AssetsTag":
            existing_asset = Asset.objects.filter(serial=row[3])
            if existing_asset.count()==0:
                asset = Asset()
                           
                asset.description = unidecode(row[1].decode('utf-8'))
                asset.model = unidecode(row[2].decode('utf-8'))
                asset.serial = row[3] 
                category = row[4]
                asset.category = category 
                if category == "office furniture":
                    prefix = "OF"
                elif category == "office appliances":
                    prefix = "OA"
                elif category == "kitchen staff":
                    prefix = "KS"
                elif category == "decorations":
                    prefix = "DE"
                else :
                    prefix = "IT"

                asset.branch = Branch.objects.get(pk = int(row[11]))
                latest_id = str(Asset.objects.count()+1).zfill(6)
                asset.tag = asset.branch.prefix+prefix+latest_id
                asset.department = Department.objects.get(pk = int(row[9]))
                asset.active=int(row[12])
                if row[6]:
                    try:
                        asset.purchase_date = datetime.strptime(row[6], "%Y-%m-%d").date()
                    except:
                        asset.purchase_date = datetime.strptime(row[6], "%d-%m-%Y").date()

                if row[7]:                
                    asset.purchase_price = row[7]
                else:
                    asset.purchase_price = 0
                asset.invoice_number = row[5]  
                asset.supplier = row[8] 
                asset.warranty = row[10]
                asset.status = row[14]
                asset.condition = "brand new"
                asset.insured = True
                asset.accept= True
                asset.authorize="aproved"
                asset.created_by=request.user            
                asset.modified_by=request.user
                print(asset.tag +"-"+ asset.description +"-"+ asset.serial)

                asset.save() 
                upload_list.append(asset) 
           

    return upload_list  
    

def import_comments(request):
    import_list = []
    transactions = Incident.objects.all()
    for transaction in transactions:
        if not transaction.recomendations == "":
            comment = Comment()
            comment.comments = transaction.recomendations
            comment.vehicle = transaction.vehicle            
            comment.comment_type = "Incidences"
            comment.obj_id = transaction.id
            comment.created_by = request.user
            print(comment.vehicle, comment.comment_type)

            comment.save()
            import_list.append(comment)
        return import_list



def import_claims(request, import_file):
    upload_list = []
    dataReader = csv.reader(open(import_file), delimiter=',', quotechar='"')   
    capture_date = date.today()
    for row in dataReader:
        if not row[0] == "SubmissionDate":
            claim = InsuranceClaim()
            employee = row[9]
            drivers = Employee.objects.filter(employee_old_id = employee)
            if len(drivers) > 0:
                driver = drivers.first()
                claim.driver = driver          

            licence_plate = str(row[10])
            vehicles = Vehicle.objects.filter(licence_plate = licence_plate)
            print(licence_plate, ": Data Imported")
            if len(vehicles) > 0:
                vehicle = vehicles.first()
                claim.vehicle = vehicle

            submission_date = datetime.strptime(row[0], "%Y-%m-%d").date() 
            claim.submission_date = submission_date
            claim_number = row[1]
            if claim_number == "":
                claim_number = "%s-%s-%s"%(driver.id,vehicle.id,row[0])
            claim.claim_number = claim_number

            payout_date = datetime.strptime(row[2], "%Y-%m-%d").date() 
            claim.payout_date = payout_date
            claim.payout_amount = row[3]
            sp_payout_date = datetime.strptime(row[4], "%Y-%m-%d").date() 
            claim.sp_payout_date = sp_payout_date
            claim.sp_payout_amount = row[5]
            claim.excess = row[6]
            claim.comments = row[7]
            claim.claim_status = row[8]
           


            claim.save() 
            upload_list.append(claim) 

    return upload_list  

def import_traffic_fines(request, import_file):
    upload_list = []
    dataReader = csv.reader(open(import_file), delimiter=',', quotechar='"')   
    capture_date = date.today()
    for row in dataReader:
        if not row[0] == "NoticeNumber":
            notice_number = row[0]
            existing = Trafficfine.objects.filter(notice_number=notice_number).count()
            if existing == 0:
                fine = Trafficfine()               
                fine.notice_number = row[0]
               
                offence_date = datetime.strptime(row[1], "%Y-%m-%d").date()
                fine.offence_date = offence_date

                due_date = datetime.strptime(row[2], "%Y-%m-%d").date()            
                fine.due_date = due_date

                fine.description = str(row[3])
                fine.location = row[4]           
                fine.amount = row[5]

                court_date = datetime.strptime(row[6], "%Y-%m-%d").date()            
                fine.court_date = court_date

                fine.serious_offence = int(row[7])
                fine.awaiting_summons = int(row[8])
                fine.court_appearance = int(row[9])
                fine.court_attended = int(row[10])
                fine.paid = int(row[11])

                date_paid = datetime.strptime(row[12], "%Y-%m-%d").date()
                if row[12] == "1900-01-01":
                    date_paid = due_date       
                fine.payment_date = date_paid             

                employee = row[13]
                drivers = Employee.objects.filter(employee_old_id = employee)
                if len(drivers) > 0:
                    driver = drivers.first()
                    fine.driver = driver          

                licence_plate = str(row[14])
                vehicles = Vehicle.objects.filter(licence_plate = licence_plate)
                print("Vehicle:>>",licence_plate, notice_number, ":>>Data Imported")
                if len(vehicles) > 0:
                    vehicle = vehicles.first()
                    fine.vehicle = vehicle

                fine.save() 
                upload_list.append(fine) 

    return upload_list  


def  import_service_bookings(request, import_file):
    upload_list = []
    dataReader = csv.reader(open(import_file), delimiter=',', quotechar='"')   
    capture_date = date.today()
    for row in dataReader:
        # if not row[0] == "ServiceType":
            service = ServiceBooking()
           
            service.service_type = "Major Service"
            service.sevice_description = row[2]

            booking_date = datetime.strptime(row[1], "%Y-%m-%d").date()            
            service.booking_date = booking_date

            svc_date = datetime.strptime(row[1], "%Y-%m-%d").date()            
            service.service_date = svc_date

            service.garage = row[4]
            service.mileage = row[7]
           
            service.wheel_alignment = True
            service.wheel_balancing = True
            service.change_cam_belt = False
            service.air_con_regass = False
            service.created_by = request.user
            service.modified_by = request.user

            employee = row[10]
            drivers = Employee.objects.filter(employee_old_id = employee)
            if len(drivers) > 0:
                driver = drivers.first()
                service.driver = driver          

            licence_plate = str(row[0])
            vehicles = Vehicle.objects.filter(licence_plate = licence_plate)
            print(licence_plate, ": Data Imported")
            if len(vehicles) > 0:
                vehicle = vehicles.first()
                service.vehicle = vehicle
            svi = VehicleMakeAndModel.objects.get(pk=vehicle.make_n_model_id)
            service_interval=svi.service_interval
            service.next_service_mileage = round(int(service.mileage) + int(service_interval), 4)

            service.save() 
            upload_list.append(service) 

    return upload_list  


def import_maintenance(request, import_file):
    upload_list = []
    dataReader = csv.reader(open(import_file), delimiter=',', quotechar='"')   
    capture_date = date.today()
    for row in dataReader:
        # if not row[0] == "MaintDate":
            maintenance = VehicleMaintenance()
            employee = row[10]
            drivers = Employee.objects.filter(employee_old_id = employee)
            if len(drivers) > 0:
                driver = drivers.first()
                maintenance.driver = driver          

            licence_plate = str(row[0])
            vehicles = Vehicle.objects.filter(licence_plate = licence_plate)
            print(licence_plate, ": Data Imported")
            if len(vehicles) > 0:
                vehicle = vehicles.first()
                maintenance.vehicle = vehicle

            maint_date = datetime.strptime(row[1], "%Y-%m-%d").date() 
            maintenance.maint_date = maint_date
            maintenance.maint_type = row[8]
            maintenance.current_mileage = row[7]
            maintenance.description = row[2]
            maintenance.projected_cost = row[11]
            maintenance.actual_cost = row[12]
            maintenance.difference = row[13]
            maintenance.status = "Good Condition"
            maintenance.invoice_number = row[3]
            maintenance.service_provider = row[4]
            maintenance.created_by=request.user
            maintenance.modified_by=request.user
            maintenance.accept=True
            maintenance.authorize="Aproved"
            if "Service" in str(row[8]):
	            service = ServiceBooking.objects.filter(vehicle=maintenance.vehicle, booking_date=maintenance.maint_date, mileage=maintenance.current_mileage ).order_by('-id')[0]	          
	            maintenance.service_booking_number = service


            maintenance.save() 
            upload_list.append(maintenance) 

    return upload_list  



def import_incidences(request, import_file):
    upload_list = []
    dataReader = csv.reader(open(import_file), delimiter=',', quotechar='"')   
    capture_date = date.today()
    for row in dataReader:
        if not row[0] == "IncidentDate":
            incident = Incident()
            employee = row[59]
            drivers = Employee.objects.filter(employee_old_id = employee)
            if len(drivers) > 0:
                driver = drivers.first()
                incident.driver = driver          

            licence_plate = str(row[60])
            vehicles = Vehicle.objects.filter(licence_plate = licence_plate)
            print(licence_plate, ": Data Imported")
            if len(vehicles) > 0:
                vehicle = vehicles.first()
                incident.vehicle = vehicle
            inc_date = datetime.strptime(row[0], "%Y-%m-%d").date() 
            incident.incident_date = inc_date
            inc_time = datetime.strptime(row[1], "%H:%M").time() 
            incident.time_of_incident = inc_time
            incident.incident_type = row[2]
            case_number = row[3]
            if case_number == "":
                case_number = "%s-%s-%s"%(driver.id,vehicle.id,row[0])
            incident.case_number = case_number
            incident.location = row[4]
            incident.Description = row[5]
            incident.recomendations = row[6]
            incident.date_reported = row[7]
            incident.police_station = row[8]
            incident.damage_extent = row[9]

            incident.right_rear_fender =row[10]
            incident.right_rear_wheel = row[11]
            incident.right_rear_door = row[12]
            incident.right_rear_lamp = row[13]
            incident.right_rear_window = row[14]
            incident.right_rear_door_window = row[15]
            incident.right_rear_viewmirror = row[16]
            incident.right_front_door_window = row[17]
            incident.right_front_door = row[18]
            incident.right_front_wheel = row[19]
            incident.right_front_fender = row[20]
            incident.right_head_lamp = row[21]

            incident.left_rear_fender =row[22]
            incident.left_rear_wheel = row[23]
            incident.left_rear_door = row[24]
            incident.left_rear_lamp = row[25]
            incident.left_rear_window = row[26]
            incident.left_rear_door_window = row[27]
            incident.left_rear_viewmirror = row[28]
            incident.left_front_door_window = row[29]
            incident.left_front_door = row[30]
            incident.left_front_wheel = row[31]
            incident.left_front_fender = row[32]
            incident.left_head_lamp = row[33]

            incident.rear_bumper = row[34]
            incident.boot_door = row[35]
            incident.rear_wind_screen = row[36]
            incident.car_top = row[37]
            incident.wind_screen = row[38]
            incident.hood = row[39]
            incident.grill = row[40]
            incident.front_bumper = row[41]
            incident.chasis = row[42]
            incident.suspension = row[43]
            incident.engine = row[44]
            incident.gear_box = row[45]

            incident.dashboard = row[46]
            incident.dashboard_controls = row[47]
            incident.sound_system = row[48]
            incident.steering = row[49]
            incident.left_front_seat = row[50]
            incident.rear_seat = row[51]
            incident.right_front_seat = row[52]
            incident.door_panels = row[53]
            incident.foot_pedals = row[54]
            incident.hand_brake = row[55]
            incident.capets = row[56]
            incident.ceiling = row[57]

            incident.current_mileage = row[58] 
           

            incident.save() 
            upload_list.append(incident) 

    return upload_list  


def import_inspections(request, import_file):
    upload_list = []
    dataReader = csv.reader(open(import_file), delimiter=',', quotechar='"')   
    capture_date = date.today()
    for row in dataReader:
        # if not row[0] == "LogDate":
            insepction = MileageLog()
            log_date = datetime.strptime(row[0], "%Y-%m-%d").date() 
            insepction.log_date = log_date
            insepction.starting_mileage = float(row[4])            
            insepction.current_mileage = float(row[5])
            insepction.mileage = float(row[6])
            insepction.fuel_balance_bf = 0
            insepction.fuel_used = 0
            insepction.fuel_balance = 0
            insepction.doors = 1
            insepction.seats = 1
            insepction.body = 1
            insepction.tires = 1
            insepction.interior = 1
            insepction.boot = 1
            insepction.under_hood = 1
            insepction.engine_check = 1
            insepction.exhaust_check = 1
            insepction.features_check = 1
            insepction.sound_system = 1
            insepction.steering = 1
            insepction.brakes = 1
            insepction.transmission = 1
            insepction.overall_feel = 1
            start_date = datetime.strptime(row[7], "%Y-%m-%d").date()
            insepction.start_date = start_date
            end_date = datetime.strptime(row[8], "%Y-%m-%d").date()
            insepction.end_date = end_date 
            employee = row[10]
            insepction.created_by=request.user
            insepction.modified_by=request.user  
            drivers = Employee.objects.filter(employee_old_id = employee)
            if len(drivers) > 0:
                driver = drivers.first()
                insepction.driver = driver          

            licence_plate = str(row[1])
            vehicles = Vehicle.objects.filter(licence_plate = licence_plate)
            print(licence_plate, ": Data Imported")
            if len(vehicles) > 0:
                vehicle = vehicles.first()
                insepction.vehicle = vehicle

            insepction.save() 
            upload_list.append(insepction) 

    return upload_list  





def import_vehicle_allocations(request, import_file):
    upload_list = []
    dataReader = csv.reader(open(import_file), delimiter=',', quotechar='"')   
    capture_date = date.today()
    for row in dataReader:
        # if not row[0] == "TransactionType":
            allocation = VehicleAllocation()
            allocation.transaction_type = row[1]
            allo_date = datetime.strptime(row[0], "%Y-%m-%d").date() 
            allocation.allocation_date = allo_date
            allocation.cycle_limit = 5000
            allocation.mileage = float(row[8])
            allocation.status = row[5] 
            allocation.accept=True
            allocation.authorize=True
            allocation.created_by=request.user
            allocation.modified_by=request.user              
            
            employee = row[3]
            drivers = Employee.objects.filter(employee_old_id = employee)
            if len(drivers) > 0:
                driver = drivers.first()
                allocation.driver = driver

            card = row[4]
            petrol_cards = FuelCard.objects.filter(card_number =card)
            if len(petrol_cards) > 0:
                petrol_card = petrol_cards.first()          
                allocation.fuel_card = petrol_card

            licence_plate = row[2]
            vehicles = Vehicle.objects.filter(licence_plate = licence_plate)
            if len(vehicles) > 0:
                vehicle = vehicles.first()
                allocation.vehicle = vehicle

            allocation.save() 
            upload_list.append(vehicle) 

    return upload_list  


def import_vehicle(request, import_file):
    upload_list = []
    dataReader = csv.reader(open(import_file), delimiter=',', quotechar='"')   
    capture_date = date.today()
    for row in dataReader:
        if not row[0] == "LicencePlate":
            vehicle= Vehicle()
            vehicle.vehicle = row[0]
            vehicle.ownership_type = row[1]
            vehicle.vin_number = row[2]
            vehicle.model_year = row[3]
            vehicle.signing_mileage = float(row[4])
            licence_date = datetime.strptime(row[5], "%Y-%m-%d").date() 
            vehicle.licence_disk_expiry = licence_date
            vehicle.color = row[6]
            vehicle.status = row[7]
            vehicle.available = int(row[8])
            vehicle.active = int(row[9])
            re_start_date = datetime.strptime(row[10], "%Y-%m-%d").date()
            vehicle.rental_start_date = re_start_date
            re_end_date = datetime.strptime(row[11], "%Y-%m-%d").date() 
            vehicle.rental_end_date = re_end_date
            purchase_date = datetime.strptime(row[12], "%Y-%m-%d").date() 
            vehicle.purchase_date = purchase_date
            vehicle.purchase_amount = float(row[13])
            vehicle.supplier = row[14]
            vehicle.condition = row[15]
            vehicle.invoice_number = row[16]
            vehicle.warranty_expiry = row[17]
            vehicle.financier = row[18]
            vehicle.on_sp = int(row[19])
            vehicle.on_mo = int(row[20])
            vehicle.plan_provider = row[21]
            vehicle.period = row[22]
            start_date = datetime.strptime(row[23], "%Y-%m-%d").date()
            vehicle.start_date = start_date
            end_date = datetime.strptime(row[24], "%Y-%m-%d").date()
            vehicle.end_date = end_date
            vehicle.mileage_covered = float(row[25])
            vehicle.fuel_balance = float(row[26])
            vehicle.current_driver_id = row[28]
            vehicle.make_n_model_id = row[29]            
            vehicle.save() 
            upload_list.append(vehicle) 

    return upload_list


# def imports(request):
#     upload_file_form = fileUploadForm(request.POST or None, request.FILES or None, prefix='doc')


#     context = {
#         "upload_file_form": upload_file_form,

#     }


#     post = request.POST
#     if request.POST:        
#         if u'upload' in post:
#             # services = ServiceBooking.objects.all()
#             # for service in services:
#             #     service.next_service_mileage = service.mileage + 10000
#             #     service.save()

#             #     print("Saved")

#             validated = upload_file_form.is_valid()             
#             if validated:                   
#                 uploaded = upload_file_form.save(commit=False)              
#                 uploaded.file_name = uploaded.file.name
#                 uploaded.transaction = "Data Imports"
#                 uploaded.save()

#                 file = '%s/%s'% (settings.MEDIA_ROOT, uploaded.file) 
#                 # import_vehicle(request, file)
#                 # import_vehicle_allocations(request, file)
#                 # import_fuel_cards(request, file) 
#                 # import_inspections(request, file)  
#                 # import_incidences(request, file) 
#                 # import_maintenance(request, file)
#                 # import_service_bookings(request, file)
#                 # import_traffic_fines(request, file) 
#                 # import_claims(request, file)
#                 employee_contacts(request, file)
            
#             # transactions = VehicleMaintenance.objects.all()
#             # for transaction in transactions:
#             #     if not transaction.comments == "":
#             #         comment = Comment()
#             #         comment.comments = transaction.comments
#             #         comment.vehicle = transaction.vehicle            
#             #         comment.comment_type = "VehicleMaintenance"
#             #         comment.obj_id = transaction.id
#             #         comment.created_by = request.user
#             #         print(comment.vehicle, comment.comment_type)                  
#             #         comment.save()
                    

#         return HttpResponseRedirect(reverse('fleet:vehiclesList'))
#     return render(request, "imports.html", context)


# def employee_contacts(request, import_file):
#     upload_list = []
#     dataReader = csv.reader(open(import_file), delimiter=',', quotechar='"')   
#     capture_date = date.today()
#     for row in dataReader:
#         if not row[0] == "FullName":
#             contact = Contact()
#             employee = row[11]
#             drivers = Employee.objects.filter(employee_old_id = employee)
#             if len(drivers) > 0:
#                 driver = drivers.first()
#                 contact.employee = driver
#                 contact.email = row[6]
#                 contact.celphone ='0%s'%(row[7]) 
#                 contact.res_address1 = row[5]           


#             contact.save() 
#             upload_list.append(contact) 

#     return upload_list  


# def import_comments(request):
#     import_list = []
#     transactions = Incident.objects.all()
#     for transaction in transactions:
#         if not transaction.recomendations == "":
#             comment = Comment()
#             comment.comments = transaction.recomendations
#             comment.vehicle = transaction.vehicle            
#             comment.comment_type = "Incidences"
#             comment.obj_id = transaction.id
#             comment.created_by = request.user
#             print(comment.vehicle, comment.comment_type)

#             comment.save()
#             import_list.append(comment)
#         return import_list



# def import_claims(request, import_file):
#     upload_list = []
#     dataReader = csv.reader(open(import_file), delimiter=',', quotechar='"')   
#     capture_date = date.today()
#     for row in dataReader:
#         if not row[0] == "SubmissionDate":
#             claim = InsuranceClaim()
#             employee = row[9]
#             drivers = Employee.objects.filter(employee_old_id = employee)
#             if len(drivers) > 0:
#                 driver = drivers.first()
#                 claim.driver = driver          

#             licence_plate = str(row[10])
#             vehicles = Vehicle.objects.filter(vehicle = licence_plate)
#             print(licence_plate, ">>>>>>>Data Imported")
#             if len(vehicles) > 0:
#                 vehicle = vehicles.first()
#                 claim.vehicle = vehicle

#             submission_date = datetime.strptime(row[0], "%Y-%m-%d").date() 
#             claim.submission_date = submission_date
#             claim_number = row[1]
#             if claim_number == "":
#                 claim_number = "%s-%s-%s"%(driver.id,vehicle.id,row[0])
#             claim.claim_number = claim_number

#             payout_date = datetime.strptime(row[2], "%Y-%m-%d").date() 
#             claim.payout_date = payout_date
#             claim.payout_amount = row[3]
#             sp_payout_date = datetime.strptime(row[4], "%Y-%m-%d").date() 
#             claim.sp_payout_date = sp_payout_date
#             claim.sp_payout_amount = row[5]
#             claim.excess = row[6]
#             claim.comments = row[7]
#             claim.claim_status = row[8]
           


#             claim.save() 
#             upload_list.append(claim) 

#     return upload_list  

# def import_traffic_fines(request, import_file):
#     upload_list = []
#     dataReader = csv.reader(open(import_file), delimiter=',', quotechar='"')   
#     capture_date = date.today()
#     for row in dataReader:
#         if not row[0] == "NoticeNumber":
#             notice_number = row[0]
#             existing = Trafficfine.objects.filter(notice_number=notice_number).count()
#             if existing == 0:
#                 fine = Trafficfine()               
#                 fine.notice_number = row[0]
               
#                 offence_date = datetime.strptime(row[1], "%Y-%m-%d").date()
#                 fine.offence_date = offence_date

#                 due_date = datetime.strptime(row[2], "%Y-%m-%d").date()            
#                 fine.due_date = due_date

#                 fine.description = str(row[3])
#                 fine.location = row[4]           
#                 fine.amount = row[5]

#                 court_date = datetime.strptime(row[6], "%Y-%m-%d").date()            
#                 fine.court_date = court_date

#                 fine.serious_offence = int(row[7])
#                 fine.awaiting_summons = int(row[8])
#                 fine.court_appearance = int(row[9])
#                 fine.court_attended = int(row[10])
#                 fine.paid = int(row[11])

#                 date_paid = datetime.strptime(row[12], "%Y-%m-%d").date()
#                 if row[12] == "1900-01-01":
#                     date_paid = due_date       
#                 fine.payment_date = date_paid             

#                 employee = row[13]
#                 drivers = Employee.objects.filter(employee_old_id = employee)
#                 if len(drivers) > 0:
#                     driver = drivers.first()
#                     fine.driver = driver          

#                 licence_plate = str(row[14])
#                 vehicles = Vehicle.objects.filter(vehicle = licence_plate)
#                 print("Vehicle:>>",licence_plate, notice_number, ":>>Data Imported")
#                 if len(vehicles) > 0:
#                     vehicle = vehicles.first()
#                     fine.vehicle = vehicle

#                 fine.save() 
#                 upload_list.append(fine) 

#     return upload_list  


# def  import_service_bookings(request, import_file):
#     upload_list = []
#     dataReader = csv.reader(open(import_file), delimiter=',', quotechar='"')   
#     capture_date = date.today()
#     for row in dataReader:
#         if not row[0] == "ServiceType":
#             service = ServiceBooking()
           
#             service.service_type = row[0]
#             service.sevice_description = row[1]

#             booking_date = datetime.strptime(row[2], "%Y-%m-%d").date()            
#             service.booking_date = booking_date

#             svc_date = datetime.strptime(row[3], "%Y-%m-%d").date()            
#             service.service_date = svc_date

#             service.garage = row[4]
#             service.mileage = row[5]
#             service.next_service_mileage = row[6]
#             service.wheel_alignment = row[7]
#             service.wheel_balancing = row[8]
#             service.change_cam_belt = row[9]
#             service.air_con_regass = row[10]           

#             employee = row[11]
#             drivers = Employee.objects.filter(employee_old_id = employee)
#             if len(drivers) > 0:
#                 driver = drivers.first()
#                 service.driver = driver          

#             licence_plate = str(row[12])
#             vehicles = Vehicle.objects.filter(vehicle = licence_plate)
#             print(licence_plate, ">>>>>>>Data Imported")
#             if len(vehicles) > 0:
#                 vehicle = vehicles.first()
#                 service.vehicle = vehicle

#             service.save() 
#             upload_list.append(service) 

#     return upload_list  


# def import_maintenance(request, import_file):
#     upload_list = []
#     dataReader = csv.reader(open(import_file), delimiter=',', quotechar='"')   
#     capture_date = date.today()
#     for row in dataReader:
#         if not row[0] == "MaintDate":
#             maintenance = VehicleMaintenance()
#             employee = row[11]
#             drivers = Employee.objects.filter(employee_old_id = employee)
#             if len(drivers) > 0:
#                 driver = drivers.first()
#                 maintenance.driver = driver          

#             licence_plate = str(row[12])
#             vehicles = Vehicle.objects.filter(vehicle = licence_plate)
#             print(licence_plate, ">>>>>>>Data Imported")
#             if len(vehicles) > 0:
#                 vehicle = vehicles.first()
#                 maintenance.vehicle = vehicle

#             maint_date = datetime.strptime(row[0], "%Y-%m-%d").date() 
#             maintenance.maint_date = maint_date
#             maintenance.maint_type = row[1]
#             maintenance.current_mileage = row[2]
#             maintenance.description = row[3]
#             maintenance.projected_cost = row[4]
#             maintenance.actual_cost = row[5]
#             maintenance.difference = row[6]
#             maintenance.status = row[7]
#             maintenance.comments = row[8]
#             maintenance.invoice_number = row[9]
#             maintenance.service_provider = row[10]


#             maintenance.save() 
#             upload_list.append(maintenance) 

#     return upload_list  



# def import_incidences(request, import_file):
#     upload_list = []
#     dataReader = csv.reader(open(import_file), delimiter=',', quotechar='"')   
#     capture_date = date.today()
#     for row in dataReader:
#         if not row[0] == "IncidentDate":
#             incident = Incident()
#             employee = row[59]
#             drivers = Employee.objects.filter(employee_old_id = employee)
#             if len(drivers) > 0:
#                 driver = drivers.first()
#                 incident.driver = driver          

#             licence_plate = str(row[60])
#             vehicles = Vehicle.objects.filter(vehicle = licence_plate)
#             print(licence_plate, ">>>>>>>Data Imported")
#             if len(vehicles) > 0:
#                 vehicle = vehicles.first()
#                 incident.vehicle = vehicle
#             inc_date = datetime.strptime(row[0], "%Y-%m-%d").date() 
#             incident.incident_date = inc_date
#             inc_time = datetime.strptime(row[1], "%H:%M").time() 
#             incident.time_of_incident = inc_time
#             incident.incident_type = row[2]
#             case_number = row[3]
#             if case_number == "":
#                 case_number = "%s-%s-%s"%(driver.id,vehicle.id,row[0])
#             incident.case_number = case_number
#             incident.location = row[4]
#             incident.Description = row[5]
#             incident.recomendations = row[6]
#             incident.date_reported = row[7]
#             incident.police_station = row[8]
#             incident.damage_extent = row[9]

#             incident.right_rear_fender =row[10]
#             incident.right_rear_wheel = row[11]
#             incident.right_rear_door = row[12]
#             incident.right_rear_lamp = row[13]
#             incident.right_rear_window = row[14]
#             incident.right_rear_door_window = row[15]
#             incident.right_rear_viewmirror = row[16]
#             incident.right_front_door_window = row[17]
#             incident.right_front_door = row[18]
#             incident.right_front_wheel = row[19]
#             incident.right_front_fender = row[20]
#             incident.right_head_lamp = row[21]

#             incident.left_rear_fender =row[22]
#             incident.left_rear_wheel = row[23]
#             incident.left_rear_door = row[24]
#             incident.left_rear_lamp = row[25]
#             incident.left_rear_window = row[26]
#             incident.left_rear_door_window = row[27]
#             incident.left_rear_viewmirror = row[28]
#             incident.left_front_door_window = row[29]
#             incident.left_front_door = row[30]
#             incident.left_front_wheel = row[31]
#             incident.left_front_fender = row[32]
#             incident.left_head_lamp = row[33]

#             incident.rear_bumper = row[34]
#             incident.boot_door = row[35]
#             incident.rear_wind_screen = row[36]
#             incident.car_top = row[37]
#             incident.wind_screen = row[38]
#             incident.hood = row[39]
#             incident.grill = row[40]
#             incident.front_bumper = row[41]
#             incident.chasis = row[42]
#             incident.suspension = row[43]
#             incident.engine = row[44]
#             incident.gear_box = row[45]

#             incident.dashboard = row[46]
#             incident.dashboard_controls = row[47]
#             incident.sound_system = row[48]
#             incident.steering = row[49]
#             incident.left_front_seat = row[50]
#             incident.rear_seat = row[51]
#             incident.right_front_seat = row[52]
#             incident.door_panels = row[53]
#             incident.foot_pedals = row[54]
#             incident.hand_brake = row[55]
#             incident.capets = row[56]
#             incident.ceiling = row[57]

#             incident.current_mileage = row[58] 
           

#             incident.save() 
#             upload_list.append(incident) 

#     return upload_list  


# def import_inspections(request, import_file):
#     upload_list = []
#     dataReader = csv.reader(open(import_file), delimiter=',', quotechar='"')   
#     capture_date = date.today()
#     for row in dataReader:
#         if not row[0] == "LogDate":
#             insepction = MileageLog()
#             log_date = datetime.strptime(row[0], "%Y-%m-%d").date() 
#             insepction.log_date = log_date
#             insepction.starting_mileage = float(row[1])            
#             insepction.current_mileage = float(row[2])
#             insepction.mileage = float(row[3])
#             insepction.fuel_balance_bf = float(row[4])
#             insepction.fuel_used = float(row[5]) 
#             insepction.fuel_balance = float(row[6])
#             start_date = datetime.strptime(row[7], "%Y-%m-%d").date()
#             insepction.start_date = start_date
#             end_date = datetime.strptime(row[8], "%Y-%m-%d").date()
#             insepction.end_date = end_date               
#             insepction.comments = row[9]
#             employee = row[10]
#             drivers = Employee.objects.filter(employee_old_id = employee)
#             if len(drivers) > 0:
#                 driver = drivers.first()
#                 insepction.driver = driver          

#             licence_plate = str(row[11])
#             vehicles = Vehicle.objects.filter(vehicle = licence_plate)
#             print(licence_plate, ">>>>>>>Data Imported")
#             if len(vehicles) > 0:
#                 vehicle = vehicles.first()
#                 insepction.vehicle = vehicle

#             insepction.save() 
#             upload_list.append(insepction) 

#     return upload_list  



# def import_fuel_cards(request, import_file):
#     upload_list = []
#     dataReader = csv.reader(open(import_file), delimiter=',', quotechar='"')   
#     capture_date = date.today()
#     for row in dataReader:
#         if not row[0] == "TransactionType":
#             fuel_card_count = FuelCard.objects.filter(card_number=row[0]).count()
#             if fuel_card_count ==0:
#                 fuel_card = FuelCard()
#                 fuel_card.card_number = row[0]
#                 fuel_card.card_type = row[1]
#                 fuel_card.save() 
#                 upload_list.append(fuel_card) 

#     return upload_list  


# def import_vehicle_allocations(request, import_file):
#     upload_list = []
#     dataReader = csv.reader(open(import_file), delimiter=',', quotechar='"')   
#     capture_date = date.today()
#     for row in dataReader:
#         if not row[0] == "TransactionType":
#             allocation = VehicleAllocation()
#             allocation.transaction_type = row[0]
#             allo_date = datetime.strptime(row[1], "%Y-%m-%d").date() 
#             allocation.allocation_date = allo_date
#             allocation.cycle_limit = float(row[2])
#             allocation.mileage = float(row[3])
#             allocation.status = row[4]
#             allocation.authorizer = row[5] 
#             allocation.comments = row[6]               
            
#             employee = row[7]
#             drivers = Employee.objects.filter(employee_old_id = employee)
#             if len(drivers) > 0:
#                 driver = drivers.first()
#                 allocation.driver = driver

#             card = row[8]
#             petrol_cards = FuelCard.objects.filter(card_number =card)
#             if len(petrol_cards) > 0:
#                 petrol_card = petrol_cards.first()          
#                 allocation.fuel_card = petrol_card

#             licence_plate = row[9]
#             vehicles = Vehicle.objects.filter(vehicle = licence_plate)
#             if len(vehicles) > 0:
#                 vehicle = vehicles.first()
#                 allocation.vehicle = vehicle

#             allocation.save() 
#             upload_list.append(vehicle) 

#     return upload_list  


# def import_vehicle(request, import_file):
#     upload_list = []
#     dataReader = csv.reader(open(import_file), delimiter=',', quotechar='"')   
#     capture_date = date.today()
#     for row in dataReader:
#         if not row[0] == "LicencePlate":
#             vehicle= Vehicle()
#             vehicle.vehicle = row[0]
#             vehicle.ownership_type = row[1]
#             vehicle.vin_number = row[2]
#             vehicle.model_year = row[3]
#             vehicle.signing_mileage = float(row[4])
#             licence_date = datetime.strptime(row[5], "%Y-%m-%d").date() 
#             vehicle.licence_disk_expiry = licence_date
#             vehicle.color = row[6]
#             vehicle.status = row[7]
#             vehicle.available = int(row[8])
#             vehicle.active = int(row[9])
#             re_start_date = datetime.strptime(row[10], "%Y-%m-%d").date()
#             vehicle.rental_start_date = re_start_date
#             re_end_date = datetime.strptime(row[11], "%Y-%m-%d").date() 
#             vehicle.rental_end_date = re_end_date
#             purchase_date = datetime.strptime(row[12], "%Y-%m-%d").date() 
#             vehicle.purchase_date = purchase_date
#             vehicle.purchase_amount = float(row[13])
#             vehicle.supplier = row[14]
#             vehicle.condition = row[15]
#             vehicle.invoice_number = row[16]
#             vehicle.warranty_expiry = row[17]
#             vehicle.financier = row[18]
#             vehicle.on_sp = int(row[19])
#             vehicle.on_mo = int(row[20])
#             vehicle.plan_provider = row[21]
#             vehicle.period = row[22]
#             start_date = datetime.strptime(row[23], "%Y-%m-%d").date()
#             vehicle.start_date = start_date
#             end_date = datetime.strptime(row[24], "%Y-%m-%d").date()
#             vehicle.end_date = end_date
#             vehicle.mileage_covered = float(row[25])
#             vehicle.fuel_balance = float(row[26])
#             vehicle.current_driver_id = row[28]
#             vehicle.make_n_model_id = row[29]            
#             vehicle.save() 
#             upload_list.append(vehicle) 

#     return upload_list
