# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0006_auto_20170628_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalvehicle',
            name='inspected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalvehicle',
            name='last_inspected',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='inspected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='last_inspected',
            field=models.DateField(null=True, blank=True),
        ),
    ]
