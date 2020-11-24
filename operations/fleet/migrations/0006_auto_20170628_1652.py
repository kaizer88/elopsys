# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0005_auto_20170626_1014'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fueltransfer',
            old_name='to_driver',
            new_name='driver',
        ),
        migrations.RenameField(
            model_name='fueltransfer',
            old_name='to_vehicle',
            new_name='vehicle',
        ),
        migrations.RenameField(
            model_name='historicalfueltransfer',
            old_name='to_driver',
            new_name='driver',
        ),
        migrations.RenameField(
            model_name='historicalfueltransfer',
            old_name='to_vehicle',
            new_name='vehicle',
        ),
    ]
