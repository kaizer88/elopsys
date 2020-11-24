# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-08-20 10:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0019_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='account_type',
            field=models.CharField(blank=True, choices=[(b'cash', b'Cash'), (b'credit', b'Credit'), (b'debit', b'Debit')], max_length=50, null=True, verbose_name=b'Account Type'),
        ),
        migrations.AddField(
            model_name='vendor',
            name='balance',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]
