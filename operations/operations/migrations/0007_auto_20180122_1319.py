# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-22 11:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0006_auto_20180115_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
