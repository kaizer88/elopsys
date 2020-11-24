# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('branch', models.CharField(default=None, max_length=120, null=True, blank=True)),
                ('prefix', models.CharField(default=None, max_length=2, null=True, blank=True)),
                ('office_type', models.CharField(default=None, max_length=20, null=True, blank=True, choices=[('HQ', 'Head Office'), ('RO', 'Regional Office'), ('SO', 'Satelite Office')])),
                ('email', models.CharField(default=None, max_length=120, null=True, blank=True)),
                ('celphone', models.CharField(default=None, max_length=20, null=True, blank=True)),
                ('address', models.CharField(default=None, max_length=200, null=True, blank=True)),
                ('street_address', models.CharField(default=None, max_length=200, null=True, blank=True)),
                ('suburb', models.CharField(default=None, max_length=200, null=True, blank=True)),
                ('city', models.CharField(default=None, max_length=200, null=True, blank=True)),
                ('postal_code', models.CharField(default=None, max_length=20, null=True, blank=True)),
                ('telephone', models.CharField(default=None, max_length=20, null=True, blank=True)),
                ('telephone2', models.CharField(default=None, max_length=20, null=True, blank=True)),
                ('telephone3', models.CharField(default=None, max_length=20, null=True, blank=True)),
                ('telephone4', models.CharField(default=None, max_length=20, null=True, blank=True)),
                ('fax', models.CharField(default=None, max_length=20, null=True, blank=True)),
                ('fax2', models.CharField(default=None, max_length=20, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('department', models.CharField(default=None, max_length=120, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_name', models.CharField(max_length=255, blank=True)),
                ('file', models.FileField(upload_to='uploads/fleet')),
                ('transaction_id', models.CharField(default=None, max_length=20, null=True, blank=True)),
                ('transaction', models.CharField(default=None, max_length=50, null=True, blank=True)),
                ('date_uploaded', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ElectricityMeterNumber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('meter_number', models.CharField(max_length=120, null=True, blank=True)),
                ('meter_type', models.CharField(default=None, max_length=20, null=True, blank=True, choices=[('prepaid', 'Prepaid Electricity Meter'), ('account', 'Metered Electricity Bill')])),
                ('service_provider', models.CharField(max_length=120, null=True, blank=True)),
                ('branch', models.ForeignKey(related_name='branch_electricitymeternumber', blank=True, to='offices.Branch', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ElectricityPurchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('purchase_date', models.DateField(null=True, blank=True)),
                ('amount', models.FloatField(default=0, max_length=20, null=True, blank=True)),
                ('token', models.CharField(max_length=120, null=True, blank=True)),
                ('accept', models.BooleanField(default=False)),
                ('authorize', models.CharField(default='Pending', max_length=20, null=True, blank=True, choices=[('Pending', 'Pending'), ('Aproved', 'Authorize'), ('Declined', 'Decline')])),
                ('meter_number', models.ForeignKey(related_name='meter_electricitypurchase', blank=True, to='offices.ElectricityMeterNumber', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('floor', models.CharField(default=None, max_length=120, null=True, blank=True)),
                ('branch', models.ForeignKey(related_name='branch_floor', blank=True, to='offices.Branch', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MobilePurchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('purchase_date', models.DateField(null=True, blank=True)),
                ('mobile_option', models.CharField(default='Pending', max_length=20, null=True, blank=True, choices=[('airtime', 'Airtime Purchase'), ('data', 'Data Purchase')])),
                ('service_provider', models.CharField(blank=True, max_length=120, null=True, choices=[('cell_c', 'Cell C'), ('mtn', 'MTN'), ('telcom_mobile', 'Telcom Mobile'), ('virgin_mobile', 'Virgin Mobile'), ('vodacom', 'Vodacom')])),
                ('phone_number', models.CharField(max_length=120, null=True, blank=True)),
                ('units', models.CharField(max_length=120, null=True, blank=True)),
                ('price', models.FloatField(default=0, max_length=20, null=True, blank=True)),
                ('accept', models.BooleanField(default=False)),
                ('authorize', models.CharField(default='Pending', max_length=20, null=True, blank=True, choices=[('Pending', 'Pending'), ('Aproved', 'Authorize'), ('Declined', 'Decline')])),
                ('branch', models.ForeignKey(related_name='branch_mobilepurchase', blank=True, to='offices.Branch', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('region', models.CharField(default=None, max_length=120, null=True, blank=True)),
                ('prefix', models.CharField(default=None, max_length=2, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('section_no', models.CharField(default=None, max_length=120, null=True, blank=True)),
                ('description', models.CharField(default=None, max_length=120, null=True, blank=True)),
                ('floor', models.ForeignKey(related_name='floor_section', blank=True, to='offices.Floor', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TelcomPABXContract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('expiry_date', models.DateField(null=True, blank=True)),
                ('extensions', models.IntegerField()),
                ('price', models.FloatField(default=0, max_length=20, null=True, blank=True)),
                ('accept', models.BooleanField(default=False)),
                ('authorize', models.CharField(default='Pending', max_length=20, null=True, blank=True, choices=[('Pending', 'Pending'), ('Aproved', 'Authorize'), ('Declined', 'Decline')])),
                ('branch', models.ForeignKey(related_name='branch_telcomcontract', blank=True, to='offices.Branch', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TelcomPABXContractRenewal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_expired', models.DateField(null=True, blank=True)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('expiry_date', models.DateField(null=True, blank=True)),
                ('extensions', models.IntegerField()),
                ('price', models.FloatField(default=0, max_length=20, null=True, blank=True)),
                ('accept', models.BooleanField(default=False)),
                ('authorize', models.CharField(default='Pending', max_length=20, null=True, blank=True, choices=[('Pending', 'Pending'), ('Aproved', 'Authorize'), ('Declined', 'Decline')])),
                ('branch', models.ForeignKey(related_name='branch_telcomcontractrenewal', blank=True, to='offices.Branch', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='branch',
            name='region',
            field=models.ForeignKey(blank=True, to='offices.Region', null=True),
        ),
    ]
