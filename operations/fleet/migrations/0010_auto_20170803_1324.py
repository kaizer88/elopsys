# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0009_auto_20170802_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalvehiclemaintenance',
            name='maint_type',
            field=models.CharField(default=None, max_length=200, null=True, blank=True, choices=[('Body Works', 'Body Works'), ('Electrical', 'Eloctronic'), ('Engine ', 'Engine'), ('Gearbox', 'Gearbox'), ('Service', 'Service'), ('Suspension', 'Suspension'), ('Tires', 'Tyres'), ('Towing', 'Towing')]),
        ),
        migrations.AlterField(
            model_name='vehiclemaintenance',
            name='maint_type',
            field=models.CharField(default=None, max_length=200, null=True, blank=True, choices=[('Body Works', 'Body Works'), ('Electrical', 'Eloctronic'), ('Engine ', 'Engine'), ('Gearbox', 'Gearbox'), ('Service', 'Service'), ('Suspension', 'Suspension'), ('Tires', 'Tyres'), ('Towing', 'Towing')]),
        ),
    ]
