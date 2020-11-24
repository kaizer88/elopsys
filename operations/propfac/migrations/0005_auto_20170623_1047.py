# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('propfac', '0004_auto_20170623_0905'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalpfrequisition',
            old_name='quotation1',
            new_name='quotation_1',
        ),
        migrations.RenameField(
            model_name='historicalpfrequisition',
            old_name='quotation2',
            new_name='quotation_2',
        ),
        migrations.RenameField(
            model_name='pfrequisition',
            old_name='quotation1',
            new_name='quotation_1',
        ),
        migrations.RenameField(
            model_name='pfrequisition',
            old_name='quotation2',
            new_name='quotation_2',
        ),
    ]
