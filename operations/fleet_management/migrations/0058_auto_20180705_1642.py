# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-07-05 14:42
from __future__ import unicode_literals

from django.db import migrations
from fleet_management.models import InsuranceClaimDocumentUploads
def populate_upload_types(apps, schema_editor):
	upload = InsuranceClaimDocumentUploads.objects.get_or_create(insurance_claim_type="Insurance Claim", description="Affidavit")
	upload = InsuranceClaimDocumentUploads.objects.get_or_create(insurance_claim_type="Insurance Claim", description="Police Report")
	upload = InsuranceClaimDocumentUploads.objects.get_or_create(insurance_claim_type="Insurance Claim", description="Drivers Licence")
	upload = InsuranceClaimDocumentUploads.objects.get_or_create(insurance_claim_type="Insurance Claim", description="Claim Form")
	upload = InsuranceClaimDocumentUploads.objects.get_or_create(insurance_claim_type="Insurance Claim", description="Pictures of Damage")
	upload = InsuranceClaimDocumentUploads.objects.get_or_create(insurance_claim_type="Insurance Claim", description="Quotation")
	upload = InsuranceClaimDocumentUploads.objects.get_or_create(insurance_claim_type="Insurance Claim", description="Incident and Accident Report")

class Migration(migrations.Migration):

    dependencies = [
        ('fleet_management', '0057_auto_20180705_1026'),
    ]

    operations = [
    ]