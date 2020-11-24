# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0005_auto_20170628_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='prefix',
            field=models.CharField(default=None, max_length=20, null=True, blank=True),
        ),
    ]
