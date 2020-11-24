# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-07-09 08:46
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import lib.fields


class Migration(migrations.Migration):

    dependencies = [
        ('fleet_management', '0059_auto_20180704_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fuelcard',
            name='vehicle_assigned',
            field=lib.fields.ProtectedForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vehicle_fuelcard', to='fleet_management.Vehicle'),
        ),
        migrations.AlterField(
            model_name='fuelcardusage',
            name='fuel_card',
            field=lib.fields.ProtectedForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='fuel_card_usage', to='fleet_management.FuelCard', verbose_name=b'Fuel Card Number'),
        ),
    ]