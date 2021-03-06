# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-25 06:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import lib.fields


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0006_auto_20180206_1327'),
        ('fleet_management', '0052_vehiclefuelcard'),
    ]

    operations = [
        migrations.AddField(
            model_name='fuelcardusage',
            name='driver',
            field=lib.fields.ProtectedForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='fuel_usage_driver', to='employees.Employee'),
        ),
        migrations.AddField(
            model_name='fuelcardusage',
            name='vehicle',
            field=lib.fields.ProtectedForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='fuel_usage_vehicle', to='fleet_management.Vehicle'),
        ),
        migrations.AlterField(
            model_name='fuelcardusage',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
