# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0013_auto_20170814_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalvehicle',
            name='licence_plate',
            field=models.CharField(max_length=20, verbose_name='vehicle registration', db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalvehicle',
            name='model_year',
            field=models.CharField(default=None, max_length=4, null=True, verbose_name='year model', blank=True),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='licence_plate',
            field=models.CharField(unique=True, max_length=20, verbose_name='vehicle registration'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='make_n_model',
            field=models.ForeignKey(verbose_name='make &amp model', blank=True, to='fleet.VehicleMakeAndModel', null=True),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='model_year',
            field=models.CharField(default=None, max_length=4, null=True, verbose_name='year model', blank=True),
        ),
    ]
