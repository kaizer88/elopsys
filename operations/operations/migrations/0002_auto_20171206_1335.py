# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-06 11:35
from __future__ import unicode_literals

from django.db import migrations


def create_groups(apps, schema):
    from django.core.management import call_command
    call_command('create_ops_groups')


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups)
    ]
