# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0003_auto_20170619_1406'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='distict_manager',
            new_name='district_manager',
        ),
    ]
