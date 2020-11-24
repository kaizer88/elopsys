# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
	def insert_permissions(apps, schema_editor):
		Permission = apps.get_model("auth", "Permission")
		ContentType = apps.get_model("contenttypes", "ContentType")
		# content_type = ContentType.objects.get_or_create(app_label="policies", model="policy")[0]

		models_list = ['Branch', 'Document', 'ElectricityMeterNumber', 'ElectricityPurchase', 'Floor', 'MobilePurchase', 'Region', 'Section',
		'TelcomPABXContract', 'TelcomPABXContractRenewal']

		p_types = ['view', 'create', 'edit', 'authorize']
		for m in models_list:
			content_type = ContentType.objects.get_or_create(app_label="offices", model=m)[0]
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
		ops_executive.permissions.add(Permission.objects.get(codename='view_telcompabxcontractrenewal').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_telcompabxcontractrenewal').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_telcompabxcontractrenewal').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_telcompabxcontractrenewal').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_telcompabxcontract').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_telcompabxcontract').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_telcompabxcontract').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_telcompabxcontract').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_section').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_section').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_section').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_section').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_region').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_region').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_region').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_region').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_mobilepurchase').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_mobilepurchase').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_mobilepurchase').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_mobilepurchase').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_floor').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_floor').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_floor').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_floor').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_electricitypurchase').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_electricitypurchase').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_electricitypurchase').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_electricitypurchase').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_electricitymeternumber').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_electricitymeternumber').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_electricitymeternumber').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_electricitymeternumber').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_document').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_document').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_document').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_document').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_branch').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_branch').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_branch').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_branch').pk)


		# Operations Manager
		ops_manager.permissions.add(Permission.objects.get(codename='view_telcompabxcontractrenewal').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_telcompabxcontractrenewal').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_telcompabxcontractrenewal').pk)		

		ops_manager.permissions.add(Permission.objects.get(codename='view_telcompabxcontract').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_telcompabxcontract').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_telcompabxcontract').pk)
		
		ops_manager.permissions.add(Permission.objects.get(codename='view_section').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_section').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_section').pk)		

		ops_manager.permissions.add(Permission.objects.get(codename='view_region').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_region').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_region').pk)		

		ops_manager.permissions.add(Permission.objects.get(codename='view_mobilepurchase').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_mobilepurchase').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_mobilepurchase').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_floor').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_floor').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_floor').pk)		

		ops_manager.permissions.add(Permission.objects.get(codename='view_electricitypurchase').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_electricitypurchase').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_electricitypurchase').pk)		

		ops_manager.permissions.add(Permission.objects.get(codename='view_electricitymeternumber').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_electricitymeternumber').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_electricitymeternumber').pk)		

		ops_manager.permissions.add(Permission.objects.get(codename='view_document').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_document').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_document').pk)		

		ops_manager.permissions.add(Permission.objects.get(codename='view_branch').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_branch').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_branch').pk)	


		# Operations Assistant
		ops_assistant.permissions.add(Permission.objects.get(codename='view_telcompabxcontractrenewal').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_telcompabxcontractrenewal').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_telcompabxcontractrenewal').pk)		

		ops_assistant.permissions.add(Permission.objects.get(codename='view_telcompabxcontract').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_telcompabxcontract').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_telcompabxcontract').pk)
		
		ops_assistant.permissions.add(Permission.objects.get(codename='view_section').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_section').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_section').pk)		

		ops_assistant.permissions.add(Permission.objects.get(codename='view_region').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_region').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_region').pk)		

		ops_assistant.permissions.add(Permission.objects.get(codename='view_mobilepurchase').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_mobilepurchase').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_mobilepurchase').pk)

		ops_assistant.permissions.add(Permission.objects.get(codename='view_floor').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_floor').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_floor').pk)		

		ops_assistant.permissions.add(Permission.objects.get(codename='view_electricitypurchase').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_electricitypurchase').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_electricitypurchase').pk)		

		ops_assistant.permissions.add(Permission.objects.get(codename='view_electricitymeternumber').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_electricitymeternumber').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_electricitymeternumber').pk)		

		ops_assistant.permissions.add(Permission.objects.get(codename='view_document').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_document').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_document').pk)		

		ops_assistant.permissions.add(Permission.objects.get(codename='view_branch').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_branch').pk) 
		ops_assistant.permissions.add(Permission.objects.get(codename='edit_branch').pk)


		# Operations Offices
		ops_offices.permissions.add(Permission.objects.get(codename='view_telcompabxcontractrenewal').pk)
		ops_offices.permissions.add(Permission.objects.get(codename='create_telcompabxcontractrenewal').pk) 
		ops_offices.permissions.add(Permission.objects.get(codename='edit_telcompabxcontractrenewal').pk)		

		ops_offices.permissions.add(Permission.objects.get(codename='view_telcompabxcontract').pk)
		ops_offices.permissions.add(Permission.objects.get(codename='create_telcompabxcontract').pk) 
		ops_offices.permissions.add(Permission.objects.get(codename='edit_telcompabxcontract').pk)
		
		ops_offices.permissions.add(Permission.objects.get(codename='view_section').pk)
		ops_offices.permissions.add(Permission.objects.get(codename='create_section').pk) 
		ops_offices.permissions.add(Permission.objects.get(codename='edit_section').pk)		

		ops_offices.permissions.add(Permission.objects.get(codename='view_region').pk)
		ops_offices.permissions.add(Permission.objects.get(codename='create_region').pk) 
		ops_offices.permissions.add(Permission.objects.get(codename='edit_region').pk)		

		ops_offices.permissions.add(Permission.objects.get(codename='view_mobilepurchase').pk)
		ops_offices.permissions.add(Permission.objects.get(codename='create_mobilepurchase').pk) 
		ops_offices.permissions.add(Permission.objects.get(codename='edit_mobilepurchase').pk)

		ops_offices.permissions.add(Permission.objects.get(codename='view_floor').pk)
		ops_offices.permissions.add(Permission.objects.get(codename='create_floor').pk) 
		ops_offices.permissions.add(Permission.objects.get(codename='edit_floor').pk)		

		ops_offices.permissions.add(Permission.objects.get(codename='view_electricitypurchase').pk)
		ops_offices.permissions.add(Permission.objects.get(codename='create_electricitypurchase').pk) 
		ops_offices.permissions.add(Permission.objects.get(codename='edit_electricitypurchase').pk)		

		ops_offices.permissions.add(Permission.objects.get(codename='view_electricitymeternumber').pk)
		ops_offices.permissions.add(Permission.objects.get(codename='create_electricitymeternumber').pk) 
		ops_offices.permissions.add(Permission.objects.get(codename='edit_electricitymeternumber').pk)		

		ops_offices.permissions.add(Permission.objects.get(codename='view_document').pk)
		ops_offices.permissions.add(Permission.objects.get(codename='create_document').pk) 
		ops_offices.permissions.add(Permission.objects.get(codename='edit_document').pk)		

		ops_offices.permissions.add(Permission.objects.get(codename='view_branch').pk)
		ops_offices.permissions.add(Permission.objects.get(codename='create_branch').pk) 
		ops_offices.permissions.add(Permission.objects.get(codename='edit_branch').pk)	


		# Operations Property And Facilities
		ops_property.permissions.add(Permission.objects.get(codename='view_telcompabxcontractrenewal').pk)
		ops_property.permissions.add(Permission.objects.get(codename='create_telcompabxcontractrenewal').pk) 
		ops_property.permissions.add(Permission.objects.get(codename='edit_telcompabxcontractrenewal').pk)		

		ops_property.permissions.add(Permission.objects.get(codename='view_telcompabxcontract').pk)
		ops_property.permissions.add(Permission.objects.get(codename='create_telcompabxcontract').pk) 
		ops_property.permissions.add(Permission.objects.get(codename='edit_telcompabxcontract').pk)
		
		ops_property.permissions.add(Permission.objects.get(codename='view_section').pk)
		ops_property.permissions.add(Permission.objects.get(codename='create_section').pk) 
		ops_property.permissions.add(Permission.objects.get(codename='edit_section').pk)		

		ops_property.permissions.add(Permission.objects.get(codename='view_region').pk)
		ops_property.permissions.add(Permission.objects.get(codename='create_region').pk) 
		ops_property.permissions.add(Permission.objects.get(codename='edit_region').pk)		

		ops_property.permissions.add(Permission.objects.get(codename='view_mobilepurchase').pk)
		ops_property.permissions.add(Permission.objects.get(codename='create_mobilepurchase').pk) 
		ops_property.permissions.add(Permission.objects.get(codename='edit_mobilepurchase').pk)

		ops_property.permissions.add(Permission.objects.get(codename='view_floor').pk)
		ops_property.permissions.add(Permission.objects.get(codename='create_floor').pk) 
		ops_property.permissions.add(Permission.objects.get(codename='edit_floor').pk)		

		ops_property.permissions.add(Permission.objects.get(codename='view_electricitypurchase').pk)
		ops_property.permissions.add(Permission.objects.get(codename='create_electricitypurchase').pk) 
		ops_property.permissions.add(Permission.objects.get(codename='edit_electricitypurchase').pk)		

		ops_property.permissions.add(Permission.objects.get(codename='view_electricitymeternumber').pk)
		ops_property.permissions.add(Permission.objects.get(codename='create_electricitymeternumber').pk) 
		ops_property.permissions.add(Permission.objects.get(codename='edit_electricitymeternumber').pk)		

		ops_property.permissions.add(Permission.objects.get(codename='view_document').pk)
		ops_property.permissions.add(Permission.objects.get(codename='create_document').pk) 
		ops_property.permissions.add(Permission.objects.get(codename='edit_document').pk)		

		ops_property.permissions.add(Permission.objects.get(codename='view_branch').pk)
		ops_property.permissions.add(Permission.objects.get(codename='create_branch').pk) 
		ops_property.permissions.add(Permission.objects.get(codename='edit_branch').pk)					
	

	dependencies = [
	    ('accounts', '0002_auto_20170516_0932'),
	]

	operations = [
		migrations.RunPython(insert_permissions)
	]
