# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employees', '0007_employee_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='DrivingLicence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('licence_number', models.CharField(default=None, max_length=120, null=True, blank=True)),
                ('date_of_issue', models.DateField(null=True, blank=True)),
                ('expiry_date', models.DateField(null=True, blank=True)),
                ('code', models.CharField(default=None, max_length=120, null=True, blank=True, choices=[('A', 'A-Motor Cycle'), ('A1', 'A1-Motor Cycle LTE 125cc'), ('B', 'B-Light Motor Vehicle LTE 3500kg '), ('EB', 'EB-Articulated vehicles LTE 3500kg'), ('C1', 'C1-Minibuses, Buses and Goods vehicles LTE 16000kg'), ('C', 'C-Buses and goods vehicles GTE 16000kg'), ('EC1', 'EC1-Articulated vehicles LTE 16000kg'), ('EC', 'EC-Articulated vehicles GTE 18000kg')])),
                ('vehicle_restrictions', models.CharField(default=None, max_length=120, null=True, blank=True, choices=[('0', 'None'), ('1', 'Automatic transmission'), ('2', 'Electrically powered'), ('3', 'Physically disabled'), ('4', 'Bus GTE 16000kg (GVM) permited')])),
                ('driver_restrictions', models.CharField(default=None, max_length=120, null=True, blank=True, choices=[('0', 'None'), ('1', 'Glasses or Contact lenses'), ('2', 'Artificial limb')])),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(related_name='user_driving_licence', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('driver', models.ForeignKey(related_name='driver_driving_licence', blank=True, to='employees.Employee', null=True)),
                ('modified_by', models.ForeignKey(related_name='user_modified_driving_licence', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalDrivingLicence',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('licence_number', models.CharField(default=None, max_length=120, null=True, blank=True)),
                ('date_of_issue', models.DateField(null=True, blank=True)),
                ('expiry_date', models.DateField(null=True, blank=True)),
                ('code', models.CharField(default=None, max_length=120, null=True, blank=True, choices=[('A', 'A-Motor Cycle'), ('A1', 'A1-Motor Cycle LTE 125cc'), ('B', 'B-Light Motor Vehicle LTE 3500kg '), ('EB', 'EB-Articulated vehicles LTE 3500kg'), ('C1', 'C1-Minibuses, Buses and Goods vehicles LTE 16000kg'), ('C', 'C-Buses and goods vehicles GTE 16000kg'), ('EC1', 'EC1-Articulated vehicles LTE 16000kg'), ('EC', 'EC-Articulated vehicles GTE 18000kg')])),
                ('vehicle_restrictions', models.CharField(default=None, max_length=120, null=True, blank=True, choices=[('0', 'None'), ('1', 'Automatic transmission'), ('2', 'Electrically powered'), ('3', 'Physically disabled'), ('4', 'Bus GTE 16000kg (GVM) permited')])),
                ('driver_restrictions', models.CharField(default=None, max_length=120, null=True, blank=True, choices=[('0', 'None'), ('1', 'Glasses or Contact lenses'), ('2', 'Artificial limb')])),
                ('date_added', models.DateTimeField(editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('driver', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='employees.Employee', null=True)),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical driving licence',
            },
        ),
    ]
