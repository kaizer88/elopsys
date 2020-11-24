# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-26 13:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import lib.fields


class Migration(migrations.Migration):

    dependencies = [
        ('fleet_management', '0053_auto_20180625_0853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fuelcardusage',
            name='date_used',
            field=models.DateTimeField(verbose_name=b'Date Used'),
        ),
        migrations.AlterField(
            model_name='fuelcardusage',
            name='fuel_card',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fuel_card_usage', to='fleet_management.FuelCard', verbose_name=b'Fuel Card Number'),
        ),
        migrations.AlterField(
            model_name='fuelcardusage',
            name='transaction_type',
            field=models.CharField(choices=[(b'CARD FEE', b'CARD FEE'), (b'COURIER SERVICE', b'COURIER SERVICE'), (b'DAMAGED CRD_FEE', b'DAMAGED CRD_FEE'), (b'EFT', b'EFT'), (b'FUEL', b'FUEL'), (b'MAINTENANCE', b'MAINTENANCE'), (b'OIL', b'OIL'), (b'TOLL-GATE', b'TOLL-GATE'), (b'TRANSACTION FEE', b'TRANSACTION FEE'), (b'VAT OF SER FEES', b'VAT OF SER FEES')], default=b'FUEL', max_length=255, verbose_name=b'Transaction Type'),
        ),
        migrations.AlterField(
            model_name='fuelcardusage',
            name='usage_type',
            field=models.CharField(choices=[(b'import', b'Import'), (b'manual', b'Manual')], default=b'import', max_length=255, verbose_name=b'Usage Type'),
        ),
    ]
