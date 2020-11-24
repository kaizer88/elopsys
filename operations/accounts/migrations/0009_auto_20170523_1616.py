# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
	def insert_permissions(apps, schema_editor):
		Permission = apps.get_model("auth", "Permission")
		ContentType = apps.get_model("contenttypes", "ContentType")

		models_list = ['STComment', 'STDocument', 'StockItem', 'StockReplenishment', 'StockTake', 'STRequisition', 
		'STRequisitionItem', 'BranchStock',]

		p_types = ['view', 'create', 'edit', 'authorize']
		for m in models_list:
			content_type = ContentType.objects.get_or_create(app_label="stock", model=m)[0]
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
		ops_stock, exists = Group.objects.get_or_create(name='Operations Stock')
		ops_offices, exists = Group.objects.get_or_create(name='Operations Offices')
		ops_property, exists = Group.objects.get_or_create(name='Operations Property And Facilities')

		# Operations Executive
		ops_executive.permissions.add(Permission.objects.get(codename='view_stcomment').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_stcomment').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_stcomment').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_stcomment').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_stdocument').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_stdocument').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_stdocument').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_stdocument').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_stockitem').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_stockitem').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_stockitem').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_stockitem').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_stockreplenishment').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_stockreplenishment').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_stockreplenishment').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_stockreplenishment').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_stocktake').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_stocktake').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_stocktake').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_stocktake').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_strequisition').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_strequisition').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_strequisition').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_strequisition').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_strequisitionitem').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_strequisitionitem').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_strequisitionitem').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_strequisitionitem').pk)

		ops_executive.permissions.add(Permission.objects.get(codename='view_branchstock').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='create_branchstock').pk) 
		ops_executive.permissions.add(Permission.objects.get(codename='edit_branchstock').pk)
		ops_executive.permissions.add(Permission.objects.get(codename='authorize_branchstock').pk)



		# Operations Manager
		ops_manager.permissions.add(Permission.objects.get(codename='view_stcomment').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_stcomment').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_stcomment').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_stdocument').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_stdocument').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_stdocument').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_stockitem').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_stockitem').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_stockitem').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_stockreplenishment').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_stockreplenishment').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_stockreplenishment').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_stocktake').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_stocktake').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_stocktake').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_strequisition').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_strequisition').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_strequisition').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_strequisitionitem').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_strequisitionitem').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_strequisitionitem').pk)

		ops_manager.permissions.add(Permission.objects.get(codename='view_branchstock').pk)
		ops_manager.permissions.add(Permission.objects.get(codename='create_branchstock').pk) 
		ops_manager.permissions.add(Permission.objects.get(codename='edit_branchstock').pk)


		# Operations assets
		ops_assets.permissions.add(Permission.objects.get(codename='view_stcomment').pk)
		ops_assets.permissions.add(Permission.objects.get(codename='create_stcomment').pk)

		ops_assets.permissions.add(Permission.objects.get(codename='view_stdocument').pk)
		ops_assets.permissions.add(Permission.objects.get(codename='create_stdocument').pk)

		ops_assets.permissions.add(Permission.objects.get(codename='view_stockitem').pk)
		ops_assets.permissions.add(Permission.objects.get(codename='create_stockitem').pk)

		ops_assets.permissions.add(Permission.objects.get(codename='view_stockreplenishment').pk)
		ops_assets.permissions.add(Permission.objects.get(codename='create_stockreplenishment').pk)

		ops_assets.permissions.add(Permission.objects.get(codename='view_stocktake').pk)
		ops_assets.permissions.add(Permission.objects.get(codename='create_stocktake').pk)

		ops_assets.permissions.add(Permission.objects.get(codename='view_strequisition').pk)
		ops_assets.permissions.add(Permission.objects.get(codename='create_strequisition').pk)

		ops_assets.permissions.add(Permission.objects.get(codename='view_strequisitionitem').pk)
		ops_assets.permissions.add(Permission.objects.get(codename='create_strequisitionitem').pk)

		ops_assets.permissions.add(Permission.objects.get(codename='view_branchstock').pk)
		ops_assets.permissions.add(Permission.objects.get(codename='create_branchstock').pk)


		# Operations stock
		ops_stock.permissions.add(Permission.objects.get(codename='view_stcomment').pk)
		ops_stock.permissions.add(Permission.objects.get(codename='create_stcomment').pk)

		ops_stock.permissions.add(Permission.objects.get(codename='view_stdocument').pk)
		ops_stock.permissions.add(Permission.objects.get(codename='create_stdocument').pk)

		ops_stock.permissions.add(Permission.objects.get(codename='view_stockitem').pk)
		ops_stock.permissions.add(Permission.objects.get(codename='create_stockitem').pk) 

		ops_stock.permissions.add(Permission.objects.get(codename='view_stockreplenishment').pk)
		ops_stock.permissions.add(Permission.objects.get(codename='create_stockreplenishment').pk)

		ops_stock.permissions.add(Permission.objects.get(codename='view_stocktake').pk)
		ops_stock.permissions.add(Permission.objects.get(codename='create_stocktake').pk)

		ops_stock.permissions.add(Permission.objects.get(codename='view_strequisition').pk)
		ops_stock.permissions.add(Permission.objects.get(codename='create_strequisition').pk)

		ops_stock.permissions.add(Permission.objects.get(codename='view_strequisitionitem').pk)
		ops_stock.permissions.add(Permission.objects.get(codename='create_strequisitionitem').pk)

		ops_stock.permissions.add(Permission.objects.get(codename='view_branchstock').pk)
		ops_stock.permissions.add(Permission.objects.get(codename='create_branchstock').pk)


		# Operations assistant
		ops_assistant.permissions.add(Permission.objects.get(codename='view_stcomment').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_stcomment').pk) 

		ops_assistant.permissions.add(Permission.objects.get(codename='view_stdocument').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_stdocument').pk)

		ops_assistant.permissions.add(Permission.objects.get(codename='view_stockitem').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_stockitem').pk)

		ops_assistant.permissions.add(Permission.objects.get(codename='view_stockreplenishment').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_stockreplenishment').pk) 

		ops_assistant.permissions.add(Permission.objects.get(codename='view_stocktake').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_stocktake').pk)

		ops_assistant.permissions.add(Permission.objects.get(codename='view_strequisition').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_strequisition').pk)

		ops_assistant.permissions.add(Permission.objects.get(codename='view_strequisitionitem').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_strequisitionitem').pk)

		ops_assistant.permissions.add(Permission.objects.get(codename='view_branchstock').pk)
		ops_assistant.permissions.add(Permission.objects.get(codename='create_branchstock').pk) 



		# Operations offices
		ops_offices.permissions.add(Permission.objects.get(codename='view_stcomment').pk)
		ops_offices.permissions.add(Permission.objects.get(codename='create_stcomment').pk)

		ops_offices.permissions.add(Permission.objects.get(codename='view_stdocument').pk)
		ops_offices.permissions.add(Permission.objects.get(codename='create_stdocument').pk)

		ops_offices.permissions.add(Permission.objects.get(codename='view_stockitem').pk)
		ops_offices.permissions.add(Permission.objects.get(codename='create_stockitem').pk) 

		ops_offices.permissions.add(Permission.objects.get(codename='view_stockreplenishment').pk)
		ops_offices.permissions.add(Permission.objects.get(codename='create_stockreplenishment').pk)

		ops_offices.permissions.add(Permission.objects.get(codename='view_stocktake').pk)
		ops_offices.permissions.add(Permission.objects.get(codename='create_stocktake').pk) 

		ops_offices.permissions.add(Permission.objects.get(codename='view_strequisition').pk)
		ops_offices.permissions.add(Permission.objects.get(codename='create_strequisition').pk) 

		ops_offices.permissions.add(Permission.objects.get(codename='view_strequisitionitem').pk)
		ops_offices.permissions.add(Permission.objects.get(codename='create_strequisitionitem').pk)

		ops_offices.permissions.add(Permission.objects.get(codename='view_branchstock').pk)
		ops_offices.permissions.add(Permission.objects.get(codename='create_branchstock').pk) 


		# Operations property
		ops_property.permissions.add(Permission.objects.get(codename='view_stcomment').pk)
		ops_property.permissions.add(Permission.objects.get(codename='create_stcomment').pk) 

		ops_property.permissions.add(Permission.objects.get(codename='view_stdocument').pk)
		ops_property.permissions.add(Permission.objects.get(codename='create_stdocument').pk)

		ops_property.permissions.add(Permission.objects.get(codename='view_stockitem').pk)
		ops_property.permissions.add(Permission.objects.get(codename='create_stockitem').pk)

		ops_property.permissions.add(Permission.objects.get(codename='view_stockreplenishment').pk)
		ops_property.permissions.add(Permission.objects.get(codename='create_stockreplenishment').pk) 

		ops_property.permissions.add(Permission.objects.get(codename='view_stocktake').pk)
		ops_property.permissions.add(Permission.objects.get(codename='create_stocktake').pk) 

		ops_property.permissions.add(Permission.objects.get(codename='view_strequisition').pk)
		ops_property.permissions.add(Permission.objects.get(codename='create_strequisition').pk)

		ops_property.permissions.add(Permission.objects.get(codename='view_strequisitionitem').pk)
		ops_property.permissions.add(Permission.objects.get(codename='create_strequisitionitem').pk)

		ops_property.permissions.add(Permission.objects.get(codename='view_branchstock').pk)
		ops_property.permissions.add(Permission.objects.get(codename='create_branchstock').pk)

	dependencies = [
		('accounts', '0008_auto_20170516_1100'),
	]

	operations = [
		migrations.RunPython(insert_permissions)
	]
