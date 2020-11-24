# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20170607_0932 '),
    ]

    operations = [
        migrations.AddField(
            model_name='elopsysuser',
            name='employee',
            field=models.ForeignKey(blank=True, to='employees.Employee', null=True),
        ),
    ]
