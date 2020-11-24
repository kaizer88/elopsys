# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_elopsysuser_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='elopsysuser',
            name='regional_staff',
            field=models.BooleanField(default=False),
        ),
    ]
