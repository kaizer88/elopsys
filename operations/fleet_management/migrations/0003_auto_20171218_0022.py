# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-17 22:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleet_management', '0002_auto_20171206_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalvehiclemaintenance',
            name='service_interval',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='vehiclemaintenance',
            name='service_interval',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
