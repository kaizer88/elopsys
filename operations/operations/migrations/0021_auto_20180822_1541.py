# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-08-22 13:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import lib.fields


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0020_auto_20180820_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='address',
            field=lib.fields.ProtectedForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='branch_address', to='operations.Address'),
        ),
        migrations.AddField(
            model_name='branch',
            name='contact_person',
            field=lib.fields.ProtectedForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='branch_contact', to='operations.Contact'),
        ),
        migrations.AddField(
            model_name='branch',
            name='office_type',
            field=models.CharField(blank=True, choices=[(b'Head Office', b'Head Office'), (b'Regional', b'Regional'), (b'Satelite', b'Satelite')], db_index=True, default=b'new', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='tel_number_2',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Telephone Number 2'),
        ),
        migrations.AddField(
            model_name='contact',
            name='tel_number_3',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Telephone Number 3'),
        ),
    ]
