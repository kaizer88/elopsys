# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-07-27 11:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockallocated',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stockitem',
            name='category',
            field=models.CharField(choices=[(b'consumables', b'Consumables'), (b'sanitary', b'Sanitary'), (b'stationery', b'Stationery')], max_length=255),
        ),
    ]
