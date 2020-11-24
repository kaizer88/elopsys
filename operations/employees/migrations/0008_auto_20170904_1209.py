# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def update_role_prefix(apps, schema_editor):
    Designation = apps.get_registered_model('employees', 'Designation')

    des = Designation.objects.filter(prefix='AGT')

    if des.count() == 1:
        d = des.first()
        d.prefix = 'AG'
        d.save()


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0007_employee_email'),
    ]

    operations = [
        migrations.RunPython(update_role_prefix)
    ]
