# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0012_auto_20170810_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaltrafficfine',
            name='conversion_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='trafficfine',
            name='conversion_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
