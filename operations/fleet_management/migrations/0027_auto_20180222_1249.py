# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-22 10:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleet_management', '0026_auto_20180222_1129'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicebooking',
            name='address',
        ),
        migrations.RemoveField(
            model_name='servicebooking',
            name='contact_person',
        ),
    ]