# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0008_fuelusage_historicalfuelusage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalservicebooking',
            old_name='sevice_description',
            new_name='service_description',
        ),
        migrations.RenameField(
            model_name='servicebooking',
            old_name='sevice_description',
            new_name='service_description',
        ),
    ]
