# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0003_auto_20170621_1502'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalrequisition',
            old_name='budjeted',
            new_name='budgeted',
        ),
        migrations.RenameField(
            model_name='requisition',
            old_name='budjeted',
            new_name='budgeted',
        ),
    ]
