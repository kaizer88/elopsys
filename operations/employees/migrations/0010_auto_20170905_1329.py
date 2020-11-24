# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def remove_quotes(apps, schema_editor):
    Employee = apps.get_registered_model('employees', 'Employee')

    emps = Employee.objects.filter(commission_code__icontains="'")

    for e in emps:
        e.commission_code = e.commission_code.replace("'", "")
        e.save()


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0009_merge'),
    ]

    operations = [
        migrations.RunPython(remove_quotes)
    ]
