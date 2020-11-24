# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
	def insert_permissions(apps, schema_editor):
		Permission = apps.get_model("auth", "Permission")
		ContentType = apps.get_model("contenttypes", "ContentType")

		
		Group = apps.get_model("auth", "Group")
		ops_executive, exists = Group.objects.get_or_create(name='Operations Executive')
		ops_manager, exists = Group.objects.get_or_create(name='Operations Manager')
		ops_fleet, exists = Group.objects.get_or_create(name='Operations Fleet') 
		ops_assistant, exists = Group.objects.get_or_create(name='Operations Assistant')
		ops_assets, exists = Group.objects.get_or_create(name='Operations Assets')
		ops_stock, exists = Group.objects.get_or_create(name='Operations Stock')
		ops_offices, exists = Group.objects.get_or_create(name='Operations Offices')
		ops_property, exists = Group.objects.get_or_create(name='Operations Property And Facilities')

		r_perms = Permission.objects.filter(codename='view_reports').values_list('id', flat=True)
		for perm in r_perms:
			ops_executive.permissions.add(perm)	
			ops_manager.permissions.add(perm)
		s_perms = Permission.objects.filter(codename='send_sms').values_list('id', flat=True)
		for perm in s_perms:
			ops_executive.permissions.add(perm)
			ops_manager.permissions.add(perm)
			ops_fleet.permissions.add(perm)
			ops_assistant.permissions.add(perm) 
			ops_assets.permissions.add(perm)
			ops_stock.permissions.add(perm)
			ops_offices.permissions.add(perm)
			ops_property.permissions.add(perm) 
		

	dependencies = [
		('accounts', '0009_auto_20170523_1616'),
	]

	operations = [
		migrations.RunPython(insert_permissions)
	]
