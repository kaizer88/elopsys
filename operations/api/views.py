from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.six import BytesIO
from django.db import transaction, IntegrityError
from django.contrib.auth.decorators import user_passes_test
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import datetime

from operations.models import Region, Branch
from fleet_management.models import Vehicle, VehicleDriver
from employees.models import Employee
from django.conf import settings


GET, PUT, POST, DELETE = 'GET', 'PUT', 'POST', 'DELETE'


@api_view([POST])
@user_passes_test(lambda u: u.username == settings.EMERALD_API_USER)
def push_agent_data(request):

    if request.method == POST:

        success = True
        message = ''
        agent = request.data.get('agent', None)
        address = request.data.get('address', None)
        lic = request.data.get('licence', None)
        region = request.data.get('region', None)
        employee = None

        rm = None
        rsm = None
        ram = None
        bm = None
        dm = None
        adm = None
        dept = None
        branch = None

        try:
            region = Region.objects.get(code=region['code'])
        except Region.DoesNotExist:
            if region.get('code', False) and region.get('name', False):
                region = Region.objects.create(code=region['code'],name=region['name'])
            pass

        if region:
            try:
                branch = Branch.objects.get(code__in=['HQ', 'RO'])
            except Branch.DoesNotExist:
                pass

        try:
            rm = Employee.objects.get(commission_code__icontains=agent['rm_code']) if agent['rm_code'] else None
        except Employee.DoesNotExist:
            pass
        try:
            rsm = Employee.objects.get(commission_code__icontains=agent['rsm_code']) if agent['rsm_code'] else None
        except Employee.DoesNotExist:
            pass
        try:
            ram = Employee.objects.get(commission_code__icontains=agent['ram_code']) if agent['ram_code'] else None
        except Employee.DoesNotExist:
            pass
        try:
            bm = Employee.objects.get(commission_code__icontains=agent['bm_code']) if agent['bm_code'] else None
        except Employee.DoesNotExist:
            pass
        try:
            dm = Employee.objects.get(commission_code__icontains=agent['dm_code']) if agent['dm_code'] else None
        except Employee.DoesNotExist:
            pass
        try:
            adm = Employee.objects.get(commission_code__icontains=agent['adm_code']) if agent['adm_code'] else None
        except Employee.DoesNotExist:
            pass

        try:
            with transaction.atomic():

                employees = Employee.objects.filter(commission_code=agent['code'])
                if employees.count() == 1:
                    employee = employees.first()
                elif employees.count() > 1:
                    success = False
                    message = 'Duplicate employees exist under this code [%s] - fix your shit' % agent['code']
                elif employees.count() < 1:
                    employee = Employee()

                employee.commission_code = agent['code']
                employee.first_name = agent['name']
                employee.last_name = agent['surname']
                employee.id_number = agent['id_number']

                roles = agent['role']

                employee.email = agent['email']
                employee.region = region
                employee.save()

        except IntegrityError as e:
            success = False
            message = 'Employee could not be saved on elopsys. Detail: %s' % e.message
        print 'Agents updated'
        return JsonResponse({'success': success, 'message': message}, status=200, content_type='application/json')


@api_view([GET])
@user_passes_test(lambda u: u.username == 'elipsys_api_user')
def get_vehicle_info(request):
    if request.method == GET:
        agent_code = request.data.get('agent_code', None)
        if agent_code:
            try:
                employee = Employee.objects.get(commission_code=agent_code)
            except Employee.DoesNotExist:
                return JsonResponse({
                        'success': False,
                        'message': 'Agent could not be found on Operations system',
                        'vehicle_info': None
                        }, status=400, content_type='application/json')

            try:
                vehicle_driver = VehicleDriver.objects.filter(driver=employee,
                                                              start_date__lte=datetime.now(),
                                                              end_date__isnull=True)
            except VehicleDriver.DoesNotExist:
                return  JsonResponse({
                        'success': False,
                        'message': 'No vehicle information for this agent',
                        'vehicle_info': None
                        }, status=400, content_type='application/json')

            vehicle_list = []
            for vd in vehicle_driver:
                vehicle = vd.vehicle
                vehicle_info = {
                    'make': vehicle.vehicle_model.make.make_name if vehicle.vehicle_model
                                                                 else '',
                    'model': vehicle.vehicle_model.model_name if vehicle.vehicle_model
                                                              else '',
                    'class': '',
                    'licence_plate': vehicle.registration_number,
                    'ownership_type': vehicle.ownership,
                    'vin_number': vehicle.vin_number,
                    'model_year': vehicle.year_model,
                    'color': vehicle.colour,
                    'status': vehicle.status_at_create,
                    'condition': ''
                }
                vehicle_list.append(vehicle_info)

            call_result = {
                'success': True,
                'message': '',
                'vehicle_info': vehicle_list
            }

            return JsonResponse(call_result, status=200, content_type='application/json')
        else:
            return JsonResponse({'success': False,
                                 'message': 'No agent code provided'},
                                status=400, content_type='application/json')



@api_view([POST])
@user_passes_test(lambda u: u.username == settings.EMERALD_API_USER)
def push_region_data(request):
    try:
        if request.method == POST:
            region = request.data.get('region', None)
            code = region.get('code', None)
            name = region.get('name', None)

            print region
            if code and name:
                region = Region.objects.filter(code=code)
                if region.exists():
                    region = region.first()
                    region.name = name
                    region.save()
                else:
                    Region.objects.create(code=code,name=name)


            else:
                print "Failed"
                return JsonResponse({'success': False, 'message': 'Code and Name are required for a Region'}, status=400, content_type='application/json')
    except Exception, e:
        print 'Exception: {}'.format(e)
        return JsonResponse({'success': False, 'message': 'Exception: {}'.format(e)},
                            status=400, content_type='application/json')

    return JsonResponse({'success': True, 'message': 'Region successfully created/updated'}, status=200, content_type='application/json')



@api_view([POST])
@user_passes_test(lambda u: u.username == settings.EMERALD_API_USER)
def push_branch_data(request):

    if request.method == POST:
        branch = request.data.get('branch', None)
        code = branch.get('code', None)
        description = branch.get('description', None)
        print branch
        if code and description:
            branch = Branch.objects.filter(code=code)
            if branch.exists():
                branch = branch.first()
                branch.description = description
                branch.save()
            else:
                Branch.objects.create(code=code,description=description)

        else:
            print "failed"
            return JsonResponse({'success': False, 'message': 'Code and Description are required for a Branch'}, status=400, content_type='application/json')


    return JsonResponse({'success': True, 'message': 'Branch successfully created/updated'}, status=200, content_type='application/json')
