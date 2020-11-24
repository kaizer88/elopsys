# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-15 09:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleet_management', '0033_auto_20180514_1616'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tracker',
            name='purchase_type',
        ),
        migrations.AlterField(
            model_name='tracker',
            name='previous_vehicle_reg_number',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Unit Serial Number'),
        ),
    ]