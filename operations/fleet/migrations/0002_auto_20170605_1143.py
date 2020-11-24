# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalvehicle',
            old_name='end_date',
            new_name='plan_ending',
        ),
        migrations.RenameField(
            model_name='historicalvehicle',
            old_name='start_date',
            new_name='plan_starting',
        ),
        migrations.RenameField(
            model_name='historicalvehicle',
            old_name='rental_end_date',
            new_name='rental_ending',
        ),
        migrations.RenameField(
            model_name='historicalvehicle',
            old_name='rental_start_date',
            new_name='rental_starting',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='end_date',
            new_name='plan_ending',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='start_date',
            new_name='plan_starting',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='rental_end_date',
            new_name='rental_ending',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='rental_start_date',
            new_name='rental_starting',
        ),
        migrations.AddField(
            model_name='historicalvehicle',
            name='account_number',
            field=models.CharField(default=None, max_length=120, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalvehicle',
            name='lease_ending',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalvehicle',
            name='lease_starting',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='account_number',
            field=models.CharField(default=None, max_length=120, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='lease_ending',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='lease_starting',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalvehicle',
            name='ownership_type',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[('EL Fleet', 'Emerald Life Fleet'), ('EL Leased', 'Emerald Life Leased'), ('EL Rental', 'Emerald Life Rental'), ('EL Staff', 'Emerald Life Staff')]),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='ownership_type',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[('EL Fleet', 'Emerald Life Fleet'), ('EL Leased', 'Emerald Life Leased'), ('EL Rental', 'Emerald Life Rental'), ('EL Staff', 'Emerald Life Staff')]),
        ),
    ]
