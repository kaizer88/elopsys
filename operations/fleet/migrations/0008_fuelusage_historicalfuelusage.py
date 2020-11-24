# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employees', '0006_employee_department'),
        ('fleet', '0007_auto_20170706_2045'),
    ]

    operations = [
        migrations.CreateModel(
            name='FuelUsage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fleet_node_number', models.CharField(default=None, max_length=250, null=True, blank=True)),
                ('fms_account_number', models.CharField(default=None, max_length=250, null=True, blank=True)),
                ('cost_center_number', models.CharField(default=None, max_length=250, null=True, blank=True)),
                ('cost_centre_name', models.CharField(default=None, max_length=250, null=True, blank=True)),
                ('client_reference_1', models.CharField(default=None, max_length=250, null=True, blank=True)),
                ('client_reference_2', models.CharField(default=None, max_length=250, null=True, blank=True)),
                ('transaction_date', models.DateField(null=True, blank=True)),
                ('transaction_number', models.CharField(default=None, max_length=250, null=True, blank=True)),
                ('merchant_name', models.CharField(default=None, max_length=250, null=True, blank=True)),
                ('transaction_code', models.CharField(default=None, max_length=25, null=True, blank=True)),
                ('transaction_description', models.CharField(default=None, max_length=250, null=True, blank=True)),
                ('odometer_reading', models.FloatField(default=0, max_length=20, null=True, blank=True)),
                ('distance_travelled', models.FloatField(default=0, max_length=20, null=True, blank=True)),
                ('quantity', models.FloatField(default=0, max_length=20, null=True, blank=True)),
                ('amount', models.FloatField(default=0, max_length=20, null=True, blank=True)),
                ('private_usage', models.CharField(default=None, max_length=25, null=True, blank=True)),
                ('inhouse_indicator', models.CharField(default=None, max_length=25, null=True, blank=True)),
                ('current_usage', models.CharField(default=None, max_length=250, null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='user_fuelusage', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('driver', models.ForeignKey(related_name='driver_fuelusage', to='employees.Employee')),
                ('fuel_card', models.ForeignKey(related_name='fuel_card_fuelusage', blank=True, to='fleet.FuelCard', null=True)),
                ('modified_by', models.ForeignKey(related_name='user_modified_fuelusage', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('vehicle', models.ForeignKey(related_name='vehicle_fuelusage', to='fleet.Vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalFuelUsage',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('fleet_node_number', models.CharField(default=None, max_length=250, null=True, blank=True)),
                ('fms_account_number', models.CharField(default=None, max_length=250, null=True, blank=True)),
                ('cost_center_number', models.CharField(default=None, max_length=250, null=True, blank=True)),
                ('cost_centre_name', models.CharField(default=None, max_length=250, null=True, blank=True)),
                ('client_reference_1', models.CharField(default=None, max_length=250, null=True, blank=True)),
                ('client_reference_2', models.CharField(default=None, max_length=250, null=True, blank=True)),
                ('transaction_date', models.DateField(null=True, blank=True)),
                ('transaction_number', models.CharField(default=None, max_length=250, null=True, blank=True)),
                ('merchant_name', models.CharField(default=None, max_length=250, null=True, blank=True)),
                ('transaction_code', models.CharField(default=None, max_length=25, null=True, blank=True)),
                ('transaction_description', models.CharField(default=None, max_length=250, null=True, blank=True)),
                ('odometer_reading', models.FloatField(default=0, max_length=20, null=True, blank=True)),
                ('distance_travelled', models.FloatField(default=0, max_length=20, null=True, blank=True)),
                ('quantity', models.FloatField(default=0, max_length=20, null=True, blank=True)),
                ('amount', models.FloatField(default=0, max_length=20, null=True, blank=True)),
                ('private_usage', models.CharField(default=None, max_length=25, null=True, blank=True)),
                ('inhouse_indicator', models.CharField(default=None, max_length=25, null=True, blank=True)),
                ('current_usage', models.CharField(default=None, max_length=250, null=True, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('driver', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='employees.Employee', null=True)),
                ('fuel_card', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='fleet.FuelCard', null=True)),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('vehicle', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='fleet.Vehicle', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical fuel usage',
            },
        ),
    ]
