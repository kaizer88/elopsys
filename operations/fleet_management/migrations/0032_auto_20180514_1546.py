# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-14 13:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleet_management', '0031_auto_20180514_1413'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalvehiclemaintenance',
            name='plan_type',
        ),
        migrations.RemoveField(
            model_name='servicebooking',
            name='plan_type',
        ),
        migrations.RemoveField(
            model_name='vehiclemaintenance',
            name='plan_type',
        ),
    ]
