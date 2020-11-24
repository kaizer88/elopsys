# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0006_department_prefix'),
        ('employees', '0005_auto_20170714_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='department',
            field=models.ForeignKey(blank=True, to='offices.Department', null=True),
        ),
    ]
