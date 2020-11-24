# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
	def insert_permissions(apps, schema_editor):
		Permission = apps.get_model("auth", "Permission")
		ContentType = apps.get_model("contenttypes", "ContentType")
		# content_type = ContentType.objects.get_or_create(app_label="policies", model="policy")[0]

		models_list = ['FileUpload', 'FuelAllocation', 'FuelCard', 'Incident', 'InsuranceClaim', 'MileageLog', 'RenewLicenceDisk', 'ServiceBooking',
		'Trafficfine', 'Trip', 'TripLog', 'Vehicle', 'VehicleAllocation', 'VehicleExtras', 'VehicleMaintenance', 'VehicleMakeAndModel', 'Comment','Requisition',
		'RequisitionItem']

		p_types = ['view', 'create', 'edit', 'authorize']
		for m in models_list:
			content_type = ContentType.objects.get_or_create(app_label="fleet", model=m)[0]
		        for p_type in p_types:
			        Permission.objects.get_or_create(codename='%s_%s' % (p_type, m.lower()),
		                                                 name='%s %s' % (p_type.upper(), m),
		                                                 content_type=content_type)


		Permission.objects.get_or_create(codename='view_reports', name='View Reports', content_type=content_type)


		Group = apps.get_model("auth", "Group")
		ops_executive, exists = Group.objects.get_or_create(name='Operations Executive')
		ops_manager, exists = Group.objects.get_or_create(name='Operations Manager')
		ops_fleet, exists = Group.objects.get_or_create(name='Operations Fleet') 
		ops_assistant, exists = Group.objects.get_or_create(name='Operations Assistant')
		ops_assets, exists = Group.objects.get_or_create(name='Operations Assets')
		ops_offices, exists = Group.objects.get_or_create(name='Operations Offices')
		ops_property, exists = Group.objects.get_or_create(name='Operations Property And Facilities')

#Operations Executive
		ops_executive.permissions.add(Permission.objects.get(codename='view_fileupload').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_fileupload').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_fileupload').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_fileupload').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_fuelallocation').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_fuelallocation').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='edit_fuelallocation').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_fuelallocation').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_fuelcard').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_fuelcard').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_fuelcard').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_fuelcard').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_incident').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_incident').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_incident').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_incident').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_insuranceclaim').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_insuranceclaim').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_insuranceclaim').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_insuranceclaim').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_mileagelog').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_mileagelog').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_mileagelog').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_mileagelog').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_renewlicencedisk').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_renewlicencedisk').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_renewlicencedisk').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_renewlicencedisk').pk) 

		ops_executive.permissions.add(Permission.objects.get(codename='view_servicebooking').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_servicebooking').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_servicebooking').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_servicebooking').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_trafficfine').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_trafficfine').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_trafficfine').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_trafficfine').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_trip').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_trip').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_trip').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_trip').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_triplog').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_triplog').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_triplog').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_triplog').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_vehicle').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_vehicle').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_vehicle').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_vehicle').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_vehicleallocation').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_vehicleallocation').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_vehicleallocation').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_vehicleallocation').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_vehiclemaintenance').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_vehiclemaintenance').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_vehiclemaintenance').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_vehiclemaintenance').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_comment').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_comment').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_comment').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_comment').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_requisition').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_requisition').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_requisition').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_requisition').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_requisitionitem').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_requisitionitem').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_requisitionitem').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_requisitionitem').pk)



#Operations Manager
		ops_manager.permissions.add(Permission.objects.get(codename='view_fileupload').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_fileupload').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_fileupload').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_fuelallocation').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_fuelallocation').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='edit_fuelallocation').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_fuelcard').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_fuelcard').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_fuelcard').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_incident').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_incident').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_incident').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_insuranceclaim').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_insuranceclaim').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_insuranceclaim').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_mileagelog').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_mileagelog').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_mileagelog').pk) 

		ops_manager.permissions.add(Permission.objects.get(codename='view_renewlicencedisk').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_renewlicencedisk').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_renewlicencedisk').pk) 

		ops_manager.permissions.add(Permission.objects.get(codename='view_servicebooking').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_servicebooking').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_servicebooking').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_trafficfine').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_trafficfine').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_trafficfine').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_trip').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_trip').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_trip').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_triplog').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_triplog').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_triplog').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_vehicle').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_vehicle').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_vehicle').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_vehicleallocation').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_vehicleallocation').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_vehicleallocation').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_vehiclemaintenance').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_vehiclemaintenance').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_vehiclemaintenance').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_comment').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_comment').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_comment').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_requisition').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_requisition').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_requisition').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_requisitionitem').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_requisitionitem').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_requisitionitem').pk)

#Operations Fleet
		ops_fleet.permissions.add(Permission.objects.get(codename='view_fileupload').pk)
		ops_fleet.permissions.add(Permission.objects.get(codename='create_fileupload').pk) 
		ops_fleet.permissions.add(Permission.objects.get(codename='edit_fileupload').pk)

		ops_fleet.permissions.add(Permission.objects.get(codename='view_fuelallocation').pk)
		ops_fleet.permissions.add(Permission.objects.get(codename='create_fuelallocation').pk)
		ops_fleet.permissions.add(Permission.objects.get(codename='edit_fuelallocation').pk)

		ops_fleet.permissions.add(Permission.objects.get(codename='view_fuelcard').pk)
		ops_fleet.permissions.add(Permission.objects.get(codename='create_fuelcard').pk) 
		ops_fleet.permissions.add(Permission.objects.get(codename='edit_fuelcard').pk)

		ops_fleet.permissions.add(Permission.objects.get(codename='view_incident').pk)
		ops_fleet.permissions.add(Permission.objects.get(codename='create_incident').pk) 
		ops_fleet.permissions.add(Permission.objects.get(codename='edit_incident').pk)

		ops_fleet.permissions.add(Permission.objects.get(codename='view_insuranceclaim').pk)
		ops_fleet.permissions.add(Permission.objects.get(codename='create_insuranceclaim').pk) 
		ops_fleet.permissions.add(Permission.objects.get(codename='edit_insuranceclaim').pk)

		ops_fleet.permissions.add(Permission.objects.get(codename='view_mileagelog').pk)
		ops_fleet.permissions.add(Permission.objects.get(codename='create_mileagelog').pk) 
		ops_fleet.permissions.add(Permission.objects.get(codename='edit_mileagelog').pk) 

		ops_fleet.permissions.add(Permission.objects.get(codename='view_renewlicencedisk').pk)
		ops_fleet.permissions.add(Permission.objects.get(codename='create_renewlicencedisk').pk) 
		ops_fleet.permissions.add(Permission.objects.get(codename='edit_renewlicencedisk').pk) 

		ops_fleet.permissions.add(Permission.objects.get(codename='view_servicebooking').pk)
		ops_fleet.permissions.add(Permission.objects.get(codename='create_servicebooking').pk) 
		ops_fleet.permissions.add(Permission.objects.get(codename='edit_servicebooking').pk)

		ops_fleet.permissions.add(Permission.objects.get(codename='view_trafficfine').pk)
		ops_fleet.permissions.add(Permission.objects.get(codename='create_trafficfine').pk) 
		ops_fleet.permissions.add(Permission.objects.get(codename='edit_trafficfine').pk)

		ops_fleet.permissions.add(Permission.objects.get(codename='view_trip').pk)
		ops_fleet.permissions.add(Permission.objects.get(codename='create_trip').pk) 
		ops_fleet.permissions.add(Permission.objects.get(codename='edit_trip').pk)

		ops_fleet.permissions.add(Permission.objects.get(codename='view_triplog').pk)
		ops_fleet.permissions.add(Permission.objects.get(codename='create_triplog').pk) 
		ops_fleet.permissions.add(Permission.objects.get(codename='edit_triplog').pk)

		ops_fleet.permissions.add(Permission.objects.get(codename='view_vehicle').pk)
		ops_fleet.permissions.add(Permission.objects.get(codename='create_vehicle').pk) 
		ops_fleet.permissions.add(Permission.objects.get(codename='edit_vehicle').pk)

		ops_fleet.permissions.add(Permission.objects.get(codename='view_vehicleallocation').pk)
		ops_fleet.permissions.add(Permission.objects.get(codename='create_vehicleallocation').pk) 
		ops_fleet.permissions.add(Permission.objects.get(codename='edit_vehicleallocation').pk)

		ops_fleet.permissions.add(Permission.objects.get(codename='view_vehiclemaintenance').pk)
		ops_fleet.permissions.add(Permission.objects.get(codename='create_vehiclemaintenance').pk) 
		ops_fleet.permissions.add(Permission.objects.get(codename='edit_vehiclemaintenance').pk)

		ops_fleet.permissions.add(Permission.objects.get(codename='view_comment').pk)
		ops_fleet.permissions.add(Permission.objects.get(codename='create_comment').pk) 
		ops_fleet.permissions.add(Permission.objects.get(codename='edit_comment').pk)

		ops_fleet.permissions.add(Permission.objects.get(codename='view_requisition').pk)
		ops_fleet.permissions.add(Permission.objects.get(codename='create_requisition').pk) 
		ops_fleet.permissions.add(Permission.objects.get(codename='edit_requisition').pk)

		ops_fleet.permissions.add(Permission.objects.get(codename='view_requisitionitem').pk)
		ops_fleet.permissions.add(Permission.objects.get(codename='create_requisitionitem').pk) 
		ops_fleet.permissions.add(Permission.objects.get(codename='edit_requisitionitem').pk)


		#Operations Assistant
		ops_assistant.permissions.add(Permission.objects.get(codename='view_fileupload').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_fileupload').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_fileupload').pk)

		ops_assistant.permissions.add(Permission.objects.get(codename='view_fuelallocation').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_fuelallocation').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_fuelallocation').pk)

		ops_assistant.permissions.add(Permission.objects.get(codename='view_fuelcard').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_fuelcard').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_fuelcard').pk)

		ops_assistant.permissions.add(Permission.objects.get(codename='view_incident').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_incident').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_incident').pk)

		ops_assistant.permissions.add(Permission.objects.get(codename='view_insuranceclaim').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_insuranceclaim').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_insuranceclaim').pk)

		ops_assistant.permissions.add(Permission.objects.get(codename='view_mileagelog').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_mileagelog').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_mileagelog').pk) 

		ops_assistant.permissions.add(Permission.objects.get(codename='view_renewlicencedisk').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_renewlicencedisk').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_renewlicencedisk').pk) 

		ops_assistant.permissions.add(Permission.objects.get(codename='view_servicebooking').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_servicebooking').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_servicebooking').pk)

		ops_assistant.permissions.add(Permission.objects.get(codename='view_trafficfine').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_trafficfine').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_trafficfine').pk)

		ops_assistant.permissions.add(Permission.objects.get(codename='view_trip').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_trip').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_trip').pk)

		ops_assistant.permissions.add(Permission.objects.get(codename='view_triplog').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_triplog').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_triplog').pk)

		ops_assistant.permissions.add(Permission.objects.get(codename='view_vehicle').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_vehicle').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_vehicle').pk)

		ops_assistant.permissions.add(Permission.objects.get(codename='view_vehicleallocation').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_vehicleallocation').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_vehicleallocation').pk)

		ops_assistant.permissions.add(Permission.objects.get(codename='view_vehiclemaintenance').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_vehiclemaintenance').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_vehiclemaintenance').pk)

		ops_assistant.permissions.add(Permission.objects.get(codename='view_comment').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_comment').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_comment').pk)

		ops_assistant.permissions.add(Permission.objects.get(codename='view_requisition').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_requisition').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_requisition').pk)

		ops_assistant.permissions.add(Permission.objects.get(codename='view_requisitionitem').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_requisitionitem').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_requisitionitem').pk)


	dependencies = [
		('accounts', '0001_initial'),
	]

	operations = [
		migrations.RunPython(insert_permissions)
	]
