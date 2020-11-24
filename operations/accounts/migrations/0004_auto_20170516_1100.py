# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
	def insert_permissions(apps, schema_editor):
		Permission = apps.get_model("auth", "Permission")
		ContentType = apps.get_model("contenttypes", "ContentType")
		# content_type = ContentType.objects.get_or_create(app_label="policies", model="policy")[0]

		models_list = ['Document', 'LeaseAgreement', 'LeaseAgreementRenewal', 'PFComment', 'PFRequisition', 
		'PFRequisitionItem', 'PropertyMaintenance','OfficeInspection', 'ToiletInspection',]

		p_types = ['view', 'create', 'edit', 'authorize']
		for m in models_list:
			content_type = ContentType.objects.get_or_create(app_label="propfac", model=m)[0]
		        for p_type in p_types:
			        Permission.objects.get_or_create(codename='%s_%s' % (p_type, m.lower()),
		                                                 name='%s %s' % (p_type.upper(), m),
		                                                 content_type=content_type)


		Permission.objects.get_or_create(codename='view_reports', name='View Reports', content_type=content_type)
		Permission.objects.get_or_create(codename='send_sms', name='Send SMS', content_type=content_type)

		Group = apps.get_model("auth", "Group")
		ops_executive, exists = Group.objects.get_or_create(name='Operations Executive')
		ops_manager, exists = Group.objects.get_or_create(name='Operations Manager')
		ops_fleet, exists = Group.objects.get_or_create(name='Operations Fleet') 
		ops_assistant, exists = Group.objects.get_or_create(name='Operations Assistant')
		ops_assets, exists = Group.objects.get_or_create(name='Operations Assets')
		ops_offices, exists = Group.objects.get_or_create(name='Operations Offices')
		ops_property, exists = Group.objects.get_or_create(name='Operations Property And Facilities')

		# Operations Executive
		ops_executive.permissions.add(Permission.objects.get(codename='view_toiletinspection').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_toiletinspection').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_toiletinspection').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_toiletinspection').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_officeinspection').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_officeinspection').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_officeinspection').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_officeinspection').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_propertymaintenance').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_propertymaintenance').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_propertymaintenance').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_propertymaintenance').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_pfrequisitionitem').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_pfrequisitionitem').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_pfrequisitionitem').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_pfrequisitionitem').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_pfrequisition').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_pfrequisition').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_pfrequisition').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_pfrequisition').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_pfcomment').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_pfcomment').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_pfcomment').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_pfcomment').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_leaseagreementrenewal').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_leaseagreementrenewal').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_leaseagreementrenewal').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_leaseagreementrenewal').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_leaseagreement').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_leaseagreement').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_leaseagreement').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_leaseagreement').pk)
		


		# Operations Manager
		ops_manager.permissions.add(Permission.objects.get(codename='view_toiletinspection').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_toiletinspection').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_toiletinspection').pk)		

		ops_manager.permissions.add(Permission.objects.get(codename='view_officeinspection').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_officeinspection').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_officeinspection').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_propertymaintenance').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_propertymaintenance').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_propertymaintenance').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_pfrequisitionitem').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_pfrequisitionitem').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_pfrequisitionitem').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_pfrequisition').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_pfrequisition').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_pfrequisition').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_pfcomment').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_pfcomment').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_pfcomment').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_leaseagreementrenewal').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_leaseagreementrenewal').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_leaseagreementrenewal').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_leaseagreement').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_leaseagreement').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_leaseagreement').pk)


		# Operations Assistant
		ops_assistant.permissions.add(Permission.objects.get(codename='view_toiletinspection').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_toiletinspection').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_toiletinspection').pk)		

		ops_assistant.permissions.add(Permission.objects.get(codename='view_officeinspection').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_officeinspection').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_officeinspection').pk)

		ops_assistant.permissions.add(Permission.objects.get(codename='view_propertymaintenance').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_propertymaintenance').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_propertymaintenance').pk)

		ops_assistant.permissions.add(Permission.objects.get(codename='view_pfrequisitionitem').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_pfrequisitionitem').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_pfrequisitionitem').pk)

		ops_assistant.permissions.add(Permission.objects.get(codename='view_pfrequisition').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_pfrequisition').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_pfrequisition').pk)

		ops_assistant.permissions.add(Permission.objects.get(codename='view_pfcomment').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_pfcomment').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_pfcomment').pk)

		ops_assistant.permissions.add(Permission.objects.get(codename='view_leaseagreementrenewal').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_leaseagreementrenewal').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_leaseagreementrenewal').pk)

		ops_assistant.permissions.add(Permission.objects.get(codename='view_leaseagreement').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_leaseagreement').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_leaseagreement').pk)

		

		# Operations Property And Facilities
		ops_property.permissions.add(Permission.objects.get(codename='view_toiletinspection').pk)
		ops_property.permissions.add(Permission.objects.get(codename='create_toiletinspection').pk) 
		ops_property.permissions.add(Permission.objects.get(codename='edit_toiletinspection').pk)		

		ops_property.permissions.add(Permission.objects.get(codename='view_officeinspection').pk)
		ops_property.permissions.add(Permission.objects.get(codename='create_officeinspection').pk) 
		ops_property.permissions.add(Permission.objects.get(codename='edit_officeinspection').pk)

		ops_property.permissions.add(Permission.objects.get(codename='view_propertymaintenance').pk)
		ops_property.permissions.add(Permission.objects.get(codename='create_propertymaintenance').pk) 
		ops_property.permissions.add(Permission.objects.get(codename='edit_propertymaintenance').pk)

		ops_property.permissions.add(Permission.objects.get(codename='view_pfrequisitionitem').pk)
		ops_property.permissions.add(Permission.objects.get(codename='create_pfrequisitionitem').pk) 
		ops_property.permissions.add(Permission.objects.get(codename='edit_pfrequisitionitem').pk)

		ops_property.permissions.add(Permission.objects.get(codename='view_pfrequisition').pk)
		ops_property.permissions.add(Permission.objects.get(codename='create_pfrequisition').pk) 
		ops_property.permissions.add(Permission.objects.get(codename='edit_pfrequisition').pk)

		ops_property.permissions.add(Permission.objects.get(codename='view_pfcomment').pk)
		ops_property.permissions.add(Permission.objects.get(codename='create_pfcomment').pk) 
		ops_property.permissions.add(Permission.objects.get(codename='edit_pfcomment').pk)

		ops_property.permissions.add(Permission.objects.get(codename='view_leaseagreementrenewal').pk)
		ops_property.permissions.add(Permission.objects.get(codename='create_leaseagreementrenewal').pk) 
		ops_property.permissions.add(Permission.objects.get(codename='edit_leaseagreementrenewal').pk)

		ops_property.permissions.add(Permission.objects.get(codename='view_leaseagreement').pk)
		ops_property.permissions.add(Permission.objects.get(codename='create_leaseagreement').pk) 
		ops_property.permissions.add(Permission.objects.get(codename='edit_leaseagreement').pk)

		

		# Operations Offices
		ops_offices.permissions.add(Permission.objects.get(codename='view_toiletinspection').pk)
		ops_offices.permissions.add(Permission.objects.get(codename='create_toiletinspection').pk) 
		ops_offices.permissions.add(Permission.objects.get(codename='edit_toiletinspection').pk)		

		ops_offices.permissions.add(Permission.objects.get(codename='view_officeinspection').pk)
		ops_offices.permissions.add(Permission.objects.get(codename='create_officeinspection').pk) 
		ops_offices.permissions.add(Permission.objects.get(codename='edit_officeinspection').pk)

		ops_offices.permissions.add(Permission.objects.get(codename='view_propertymaintenance').pk)
		ops_offices.permissions.add(Permission.objects.get(codename='create_propertymaintenance').pk) 
		ops_offices.permissions.add(Permission.objects.get(codename='edit_propertymaintenance').pk)

		ops_offices.permissions.add(Permission.objects.get(codename='view_pfrequisitionitem').pk)
		ops_offices.permissions.add(Permission.objects.get(codename='create_pfrequisitionitem').pk) 
		ops_offices.permissions.add(Permission.objects.get(codename='edit_pfrequisitionitem').pk)

		ops_offices.permissions.add(Permission.objects.get(codename='view_pfrequisition').pk)
		ops_offices.permissions.add(Permission.objects.get(codename='create_pfrequisition').pk) 
		ops_offices.permissions.add(Permission.objects.get(codename='edit_pfrequisition').pk)

		ops_offices.permissions.add(Permission.objects.get(codename='view_pfcomment').pk)
		ops_offices.permissions.add(Permission.objects.get(codename='create_pfcomment').pk) 
		ops_offices.permissions.add(Permission.objects.get(codename='edit_pfcomment').pk)

		ops_offices.permissions.add(Permission.objects.get(codename='view_leaseagreementrenewal').pk)
		ops_offices.permissions.add(Permission.objects.get(codename='create_leaseagreementrenewal').pk) 
		ops_offices.permissions.add(Permission.objects.get(codename='edit_leaseagreementrenewal').pk)

		ops_offices.permissions.add(Permission.objects.get(codename='view_leaseagreement').pk)
		ops_offices.permissions.add(Permission.objects.get(codename='create_leaseagreement').pk) 
		ops_offices.permissions.add(Permission.objects.get(codename='edit_leaseagreement').pk)

		

	dependencies = [
	    ('accounts', '0003_auto_20170516_1001'),
	]

	operations = [
		migrations.RunPython(insert_permissions)
	]
