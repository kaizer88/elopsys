# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-15 13:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0005_auto_20180111_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insurer',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name=b'Insurer Name'),
        ),
    ]