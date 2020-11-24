# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0006_department_prefix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalmobilenumber',
            name='phone_number',
            field=models.CharField(default=datetime.datetime(2017, 7, 27, 11, 10, 46, 890883, tzinfo=utc), max_length=120, db_index=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mobilenumber',
            name='phone_number',
            field=models.CharField(default=datetime.datetime(2017, 7, 27, 11, 11, 37, 915368, tzinfo=utc), unique=True, max_length=120),
            preserve_default=False,
        ),
    ]
