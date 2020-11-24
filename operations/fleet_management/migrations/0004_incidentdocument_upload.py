# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-11 12:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleet_management', '0003_incidentdocument'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidentdocument',
            name='upload',
            field=models.CharField(choices=[(b'claim form', b'Claim Form'), (b'submission date', b'Submission Date'), (b'claim number', b'Claim Number')], default=1, max_length=255),
            preserve_default=False,
        ),
    ]
