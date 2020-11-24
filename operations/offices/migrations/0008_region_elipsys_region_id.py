# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0007_auto_20170727_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='elipsys_region_id',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
