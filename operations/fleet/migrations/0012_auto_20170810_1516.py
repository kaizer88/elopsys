# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0011_auto_20170810_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalvehicle',
            name='division',
            field=models.CharField(default=None, max_length=20, null=True, blank=True, choices=[('Marketing', 'Marketing'), ('Sales', 'Sales')]),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='division',
            field=models.CharField(default=None, max_length=20, null=True, blank=True, choices=[('Marketing', 'Marketing'), ('Sales', 'Sales')]),
        ),
    ]
