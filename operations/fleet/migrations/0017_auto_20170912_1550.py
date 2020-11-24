# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from fleet.models import *

class Migration(migrations.Migration):

	def clear_blanks(apps, schema_editor):
		logs = MileageLog.objects.all()
		for log in logs:
			if not log.mileage:
				log.mileage=0
				log.save()

	dependencies = [
		('fleet', '0016_auto_20170907_1148'),
	]

	operations = [
		migrations.RunPython(clear_blanks)
	]
