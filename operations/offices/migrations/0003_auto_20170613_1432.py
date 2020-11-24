# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0002_auto_20170612_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardallocation',
            name='allocation_type',
            field=models.CharField(default=None, max_length=50, null=True, blank=True, choices=[('Allocate Sim And Fuel Card', 'Allocate Sim And Fuel Card'), ('Allocate Sim Card', 'Allocate Sim Card'), ('Allocate Fuel Card', 'Allocate Fuel Card'), ('Return Sim And Fuel Card', 'Return Sim And Fuel Card'), ('Return Sim Card', 'Return Sim Card'), ('Return Fuel Card', 'Return Feul Card')]),
        ),
        migrations.AlterField(
            model_name='historicalcardallocation',
            name='allocation_type',
            field=models.CharField(default=None, max_length=50, null=True, blank=True, choices=[('Allocate Sim And Fuel Card', 'Allocate Sim And Fuel Card'), ('Allocate Sim Card', 'Allocate Sim Card'), ('Allocate Fuel Card', 'Allocate Fuel Card'), ('Return Sim And Fuel Card', 'Return Sim And Fuel Card'), ('Return Sim Card', 'Return Sim Card'), ('Return Fuel Card', 'Return Feul Card')]),
        ),
    ]
