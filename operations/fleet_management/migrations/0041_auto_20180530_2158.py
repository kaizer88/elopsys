# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-30 19:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleet_management', '0040_auto_20180530_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicebooking',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]