# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-07-03 11:47
from __future__ import unicode_literals

from django.db import migrations
from fleet_management.models import VehicleMake, VehicleModel, Vehicle

class Migration(migrations.Migration):

    def create_make_and_models(apps, schema_editor):
        vehicles = Vehicle.objects.all()
        for v in vehicles:
            vmake = VehicleMake.objects.get_or_create(make_name=v.make)
            vmodel = VehicleModel.objects.get_or_create(model_name=v.model, make=vmake[0])

            v.vehicle_make = vmake[0]
            v.vehicle_model = vmodel[0]
            v.save()

    dependencies = [
        ('operations', '0016_auto_20180703_1345'),
    ]

    operations = [
        migrations.RunPython(create_make_and_models)
    ]
