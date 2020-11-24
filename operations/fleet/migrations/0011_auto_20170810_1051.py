# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0010_auto_20170803_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comments',
            field=models.CharField(default=None, max_length=2000),
        ),
        migrations.AlterField(
            model_name='historicalincident',
            name='incident_type',
            field=models.CharField(default=None, max_length=200, null=True, blank=True, choices=[('Road Accident', 'Road Accident'), ('Mechanical Breakdown', 'Mechanical Breakdown'), ('Tire Puncture', 'Tire Puncture'), ('Wind Screen Damages', 'Wind Screen Damages'), ('Head Lamp Damage', 'Head Lamp Damage'), ('Body Dants & Scratches', 'Body Dents & Scratches'), ('Car Theft & Hijacking', 'Car Theft & Hijacking'), ('Vandalism', 'Vandalism')]),
        ),
        migrations.AlterField(
            model_name='incident',
            name='incident_type',
            field=models.CharField(default=None, max_length=200, null=True, blank=True, choices=[('Road Accident', 'Road Accident'), ('Mechanical Breakdown', 'Mechanical Breakdown'), ('Tire Puncture', 'Tire Puncture'), ('Wind Screen Damages', 'Wind Screen Damages'), ('Head Lamp Damage', 'Head Lamp Damage'), ('Body Dants & Scratches', 'Body Dents & Scratches'), ('Car Theft & Hijacking', 'Car Theft & Hijacking'), ('Vandalism', 'Vandalism')]),
        ),
    ]
