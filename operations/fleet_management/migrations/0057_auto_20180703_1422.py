# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-07-03 12:22
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleet_management', '0056_auto_20180702_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalvehicle',
            name='delivery_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name=b'Date Delivered'),
        ),
        migrations.AddField(
            model_name='historicalvehicle',
            name='delivery_location',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Delivery Location'),
        ),
        migrations.AddField(
            model_name='historicalvehicle',
            name='rental_company',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Rental Company'),
        ),
        migrations.AddField(
            model_name='historicalvehicle',
            name='rental_contact_person',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Contact Person'),
        ),
        migrations.AddField(
            model_name='historicalvehicle',
            name='rental_reason',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Reason For Rental'),
        ),
        migrations.AddField(
            model_name='historicalvehicle',
            name='returned_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name=b'Date Returned'),
        ),
        migrations.AddField(
            model_name='historicalvehicle',
            name='returned_location',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Returned Location'),
        ),
        migrations.AddField(
            model_name='historicalvehicle',
            name='returned_mileage',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name=b'Returned Odometer Mileage'),
        ),
        migrations.AddField(
            model_name='historicalvehicle',
            name='vehicle_class',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Vehicle Class'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='delivery_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name=b'Date Delivered'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='delivery_location',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Delivery Location'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='rental_company',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Rental Company'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='rental_contact_person',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Contact Person'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='rental_reason',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Reason For Rental'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='returned_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name=b'Date Returned'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='returned_location',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Returned Location'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='returned_mileage',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name=b'Returned Odometer Mileage'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='vehicle_class',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Vehicle Class'),
        ),
        migrations.AlterField(
            model_name='historicalvehicle',
            name='fuel_type',
            field=models.CharField(blank=True, choices=[(b'diesel', b'Diesel'), (b'petrol', b'Petrol')], max_length=120, null=True, verbose_name=b'Fuel Type'),
        ),
        migrations.AlterField(
            model_name='historicalvehicle',
            name='make',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='historicalvehicle',
            name='model',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='historicalvehicle',
            name='ownership',
            field=models.CharField(choices=[(b'emerald', b'Emerald'), (b'private', b'Private'), (b'rental', b'Rental')], max_length=50),
        ),
        migrations.AlterField(
            model_name='historicalvehicle',
            name='registration_number',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Registration Number'),
        ),
        migrations.AlterField(
            model_name='historicalvehicle',
            name='status_at_create',
            field=models.CharField(blank=True, choices=[(b'new', b'New'), (b'used', b'Used')], max_length=50, null=True, verbose_name=b'Status at Create'),
        ),
        migrations.AlterField(
            model_name='historicalvehicle',
            name='transmission',
            field=models.CharField(blank=True, choices=[(b'automatic', b'Automatic'), (b'manual', b'Manual')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='fuel_type',
            field=models.CharField(blank=True, choices=[(b'diesel', b'Diesel'), (b'petrol', b'Petrol')], max_length=120, null=True, verbose_name=b'Fuel Type'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='make',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='model',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='ownership',
            field=models.CharField(choices=[(b'emerald', b'Emerald'), (b'private', b'Private'), (b'rental', b'Rental')], max_length=50),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='registration_number',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Registration Number'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='status_at_create',
            field=models.CharField(blank=True, choices=[(b'new', b'New'), (b'used', b'Used')], max_length=50, null=True, verbose_name=b'Status at Create'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='transmission',
            field=models.CharField(blank=True, choices=[(b'automatic', b'Automatic'), (b'manual', b'Manual')], max_length=50, null=True),
        ),
    ]