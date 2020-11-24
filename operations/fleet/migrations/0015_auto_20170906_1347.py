# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0014_auto_20170818_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaltrafficfine',
            name='offence_time',
            field=models.TimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='trafficfine',
            name='offence_time',
            field=models.TimeField(null=True, blank=True),
        ),
    ]
