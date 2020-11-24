
from __future__ import unicode_literals

from django.db import migrations
from fleet_management.models import Vehicle
def update_vehicles(apps, schema_editor):

    for v in Vehicle.objects.all():
        v.registration_number = v.registration_number.replace(' ','')
        v.save()

class Migration(migrations.Migration):

    dependencies = [
        ('fleet_management', '0084_merge_20180822_0906'),
    ]

    operations = [
        migrations.RunPython(update_vehicles)
    ]
