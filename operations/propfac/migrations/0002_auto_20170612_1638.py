# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('propfac', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pfdocument',
            name='branch',
            field=models.ForeignKey(related_name='branch_propfac_documents', blank=True, to='offices.Branch', null=True),
        ),
    ]
