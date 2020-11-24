# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employees', '0004_auto_20170619_1422'),
        ('fleet', '0004_auto_20170622_1533'),
    ]

    operations = [
        migrations.CreateModel(
            name='FuelTransfer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transfer_date', models.DateField(null=True, blank=True)),
                ('from_balance', models.FloatField(default=0, max_length=20, null=True, blank=True)),
                ('from_amount_allocated', models.FloatField(default=0, max_length=20, null=True, blank=True)),
                ('from_new_balance', models.FloatField(default=0, max_length=20, null=True, blank=True)),
                ('to_balance', models.FloatField(default=0, max_length=20, null=True, blank=True)),
                ('to_amount_allocated', models.FloatField(default=0, max_length=20, null=True, blank=True)),
                ('to_new_balance', models.FloatField(default=0, max_length=20, null=True, blank=True)),
                ('accept', models.BooleanField(default=False)),
                ('authorize', models.CharField(default='Pending', max_length=20, null=True, blank=True, choices=[('Pending', 'Pending'), ('Aproved', 'Authorize'), ('Declined', 'Decline')])),
                ('created_by', models.ForeignKey(related_name='user_transfers', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('from_driver', models.ForeignKey(related_name='fromdriver_transfers', to='employees.Employee')),
                ('from_fuel_card', models.ForeignKey(related_name='fromfuelcard_transfers', blank=True, to='fleet.FuelCard', null=True)),
                ('from_vehicle', models.ForeignKey(related_name='fromvehicle_transferss', to='fleet.Vehicle')),
                ('modified_by', models.ForeignKey(related_name='user_modified_transfers', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('to_driver', models.ForeignKey(related_name='todriver_transfers', to='employees.Employee')),
                ('to_fuel_card', models.ForeignKey(related_name='tofuelcard_transfers', blank=True, to='fleet.FuelCard', null=True)),
                ('to_vehicle', models.ForeignKey(related_name='tovehicle_transferss', to='fleet.Vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalFuelTransfer',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('transfer_date', models.DateField(null=True, blank=True)),
                ('from_balance', models.FloatField(default=0, max_length=20, null=True, blank=True)),
                ('from_amount_allocated', models.FloatField(default=0, max_length=20, null=True, blank=True)),
                ('from_new_balance', models.FloatField(default=0, max_length=20, null=True, blank=True)),
                ('to_balance', models.FloatField(default=0, max_length=20, null=True, blank=True)),
                ('to_amount_allocated', models.FloatField(default=0, max_length=20, null=True, blank=True)),
                ('to_new_balance', models.FloatField(default=0, max_length=20, null=True, blank=True)),
                ('accept', models.BooleanField(default=False)),
                ('authorize', models.CharField(default='Pending', max_length=20, null=True, blank=True, choices=[('Pending', 'Pending'), ('Aproved', 'Authorize'), ('Declined', 'Decline')])),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('from_driver', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='employees.Employee', null=True)),
                ('from_fuel_card', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='fleet.FuelCard', null=True)),
                ('from_vehicle', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='fleet.Vehicle', null=True)),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('to_driver', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='employees.Employee', null=True)),
                ('to_fuel_card', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='fleet.FuelCard', null=True)),
                ('to_vehicle', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='fleet.Vehicle', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical fuel transfer',
            },
        ),
        migrations.RemoveField(
            model_name='historicalvehicleallocation',
            name='authorizer',
        ),
        migrations.RemoveField(
            model_name='vehicleallocation',
            name='authorizer',
        ),
    ]
