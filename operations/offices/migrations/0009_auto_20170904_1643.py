# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_elipsys_region_id(apps, schema_editor):
    Region = apps.get_registered_model('offices', 'Region')

    reg = Region.objects.get(prefix='WC')
    reg.elipsys_region_id = 9
    reg.save()

    reg = Region.objects.get(prefix='EC')
    reg.elipsys_region_id = 1
    reg.save()

    reg = Region.objects.get(prefix='NC')
    reg.elipsys_region_id = 8
    reg.save()

    reg = Region.objects.get(prefix='FS')
    reg.elipsys_region_id = 2
    reg.save()

    reg = Region.objects.get(prefix='GP')
    reg.elipsys_region_id = 3
    reg.save()

    reg = Region.objects.get(prefix='NW')
    reg.elipsys_region_id = 7
    reg.save()

    reg = Region.objects.get(prefix='MP')
    reg.elipsys_region_id = 6
    reg.save()

    reg = Region.objects.get(prefix='KZ')
    reg.elipsys_region_id = 4
    reg.save()

    reg = Region.objects.get(prefix='LP')
    reg.elipsys_region_id = 5
    reg.save()

    reg = Region.objects.get(prefix='SC')
    reg.elipsys_region_id = 10
    reg.save()

    reg = Region.objects.get(prefix='KC')
    reg.elipsys_region_id = 11
    reg.save()

    reg = Region.objects.get(prefix='HO')
    reg.elipsys_region_id = 0
    reg.save()


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0008_region_elipsys_region_id'),
    ]

    operations = [
        migrations.RunPython(add_elipsys_region_id)
    ]
