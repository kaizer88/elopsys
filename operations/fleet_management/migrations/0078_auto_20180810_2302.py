# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-08-10 21:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleet_management', '0077_auto_20180810_1136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='insuranceclaim',
            name='colour',
        ),
        migrations.RemoveField(
            model_name='insuranceclaim',
            name='district',
        ),
        migrations.RemoveField(
            model_name='insuranceclaim',
            name='division',
        ),
        migrations.RemoveField(
            model_name='insuranceclaim',
            name='drivers_licence',
        ),
        migrations.RemoveField(
            model_name='insuranceclaim',
            name='engine_number',
        ),
        migrations.RemoveField(
            model_name='insuranceclaim',
            name='expiry_date',
        ),
        migrations.RemoveField(
            model_name='insuranceclaim',
            name='make',
        ),
        migrations.RemoveField(
            model_name='insuranceclaim',
            name='model',
        ),
        migrations.RemoveField(
            model_name='insuranceclaim',
            name='ownership',
        ),
        migrations.RemoveField(
            model_name='insuranceclaim',
            name='region',
        ),
        migrations.RemoveField(
            model_name='insuranceclaim',
            name='vin_number',
        ),
        migrations.RemoveField(
            model_name='insuranceclaim',
            name='year_model',
        ),
    ]