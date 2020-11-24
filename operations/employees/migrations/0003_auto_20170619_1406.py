# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_auto_20170606_0850'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='assistant_district_manager',
            field=models.ForeignKey(related_name='adm_Employee', blank=True, to='employees.Employee', null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='branch_manager',
            field=models.ForeignKey(related_name='bm_Employee', blank=True, to='employees.Employee', null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='distict_manager',
            field=models.ForeignKey(related_name='dm_Employee', blank=True, to='employees.Employee', null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='regional_admin_manager',
            field=models.ForeignKey(related_name='ram_Employee', blank=True, to='employees.Employee', null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='regional_manager',
            field=models.ForeignKey(related_name='rm_Employee', blank=True, to='employees.Employee', null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='regional_sales_manager',
            field=models.ForeignKey(related_name='rsm_Employee', blank=True, to='employees.Employee', null=True),
        ),
    ]
