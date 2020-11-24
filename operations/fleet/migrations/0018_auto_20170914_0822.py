# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from fleet.models import *
from offices.models import *


class Migration(migrations.Migration):

	def update_division(apps, schema_editor):
		vehicles = Vehicle.objects.all()
		for vehicle in vehicles:
			if not vehicle.division:
				if vehicle.current_driver:
					dept =  Department.objects.filter(id=vehicle.current_driver.department_id)
					if dept :
						dept = dept.first()
						vehicle.division= dept.department
						vehicle.save()

	dependencies = [
		('fleet', '0017_auto_20170912_1550'),
	]

	operations = [
		migrations.RunPython(update_division)
	]
