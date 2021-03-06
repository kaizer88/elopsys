# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-10-30 07:54
from __future__ import unicode_literals

from django.db import migrations
from fleet_management.models import FuelCardDocumentUploads

def populate_upload_types(apps, schema_editor):
    upload = FuelCardDocumentUploads.objects.get_or_create(description="Lost Card Documents")
    upload = FuelCardDocumentUploads.objects.get_or_create(description="Driver Acceptance")
    upload = FuelCardDocumentUploads.objects.get_or_create(description="Confirmation Email")

class Migration(migrations.Migration):

    dependencies = [
        ('fleet_management', '0089_merge_20180926_1004'),
    ]

    operations = [
        migrations.RunPython(populate_upload_types)
    ]
