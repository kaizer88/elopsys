# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0004_auto_20170614_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardallocation',
            name='parckage',
            field=models.CharField(default='UC5GB', max_length=20, null=True, blank=True, choices=[('UC5GB', 'Unlimited Calls 5GB Data'), ('UC10GB ', 'Unlimited Calls 10GB Data')]),
        ),
        migrations.AlterField(
            model_name='historicalcardallocation',
            name='parckage',
            field=models.CharField(default='UC5GB', max_length=20, null=True, blank=True, choices=[('UC5GB', 'Unlimited Calls 5GB Data'), ('UC10GB ', 'Unlimited Calls 10GB Data')]),
        ),
    ]
