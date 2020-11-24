# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0015_auto_20170906_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaltrafficfine',
            name='conversion_date',
            field=models.DateField(null=True, verbose_name='Date converted to driver', blank=True),
        ),
        migrations.AlterField(
            model_name='historicaltrafficfine',
            name='offence_time',
            field=models.TimeField(null=True, verbose_name='Time', blank=True),
        ),
        migrations.AlterField(
            model_name='trafficfine',
            name='conversion_date',
            field=models.DateField(null=True, verbose_name='Date converted to driver', blank=True),
        ),
        migrations.AlterField(
            model_name='trafficfine',
            name='offence_time',
            field=models.TimeField(null=True, verbose_name='Time', blank=True),
        ),
    ]
