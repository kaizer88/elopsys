# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-17 10:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0013_auto_20180320_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='vendor_type',
            field=models.CharField(choices=[(b'branding', b'Branding'), (b'dealer', b'Dealer'), (b'fuel card supplier', b'Fuel Card Supplier'), (b'installer', b'Installer'), (b'insurance', b'Insurance'), (b'service provider', b'Service Provider'), (b'tracker', b'Tracker')], db_index=True, max_length=50, verbose_name=b'Vendor Type'),
        ),
    ]
