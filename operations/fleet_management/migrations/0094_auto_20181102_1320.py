# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-11-02 10:59
from __future__ import unicode_literals

from django.db import migrations
from fleet_management.models import VehicleStatusType

def populate_status_types(apps, schema_editor):
    st = VehicleStatusType.objects.get_or_create(description="Active")
    st = VehicleStatusType.objects.get_or_create(description="Unallocated")
    st = VehicleStatusType.objects.get_or_create(description="Service (<24 Hours)")
    st = VehicleStatusType.objects.get_or_create(description="Maintenance (>24 Hours)")
    st = VehicleStatusType.objects.get_or_create(description="Insurance Claim")
    st = VehicleStatusType.objects.get_or_create(description="Written Off")
    st = VehicleStatusType.objects.get_or_create(description="Pending Write-Off")
    st = VehicleStatusType.objects.get_or_create(description="Irrepairable")

class Migration(migrations.Migration):

    dependencies = [
        ('fleet_management', '0093_merge_20181102_1139'),
    ]

    operations = [
        migrations.RunPython(populate_status_types)
    ]
