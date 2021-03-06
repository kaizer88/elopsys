# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-06 11:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import lib.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fleet_management', '0001_initial'),
        ('employees', '0002_auto_20171206_1331'),
        ('operations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicletyre',
            name='created_by',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_tyres', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vehicletyre',
            name='modified_by',
            field=lib.fields.ProtectedForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='modified_tyres', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vehicletyre',
            name='vehicle',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tyres', to='fleet_management.Vehicle'),
        ),
        migrations.AddField(
            model_name='vehiclemaintenance',
            name='created_by',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_vehicle_maintenance', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vehiclemaintenance',
            name='modified_by',
            field=lib.fields.ProtectedForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='modified_vehicle_maintenance', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vehiclemaintenance',
            name='vehicle',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='maintenance_plan', to='fleet_management.Vehicle'),
        ),
        migrations.AddField(
            model_name='vehicledriver',
            name='created_by',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_vehicle_drivers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vehicledriver',
            name='driver',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='driver_vehicle', to='employees.Employee'),
        ),
        migrations.AddField(
            model_name='vehicledriver',
            name='modified_by',
            field=lib.fields.ProtectedForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='modified_vehicle_drivers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vehicledriver',
            name='vehicle',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='vehicle_driver', to='fleet_management.Vehicle'),
        ),
        migrations.AddField(
            model_name='vehicledocument',
            name='created_by',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_documents', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vehicledocument',
            name='document',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, to='operations.Document'),
        ),
        migrations.AddField(
            model_name='vehicledocument',
            name='modified_by',
            field=lib.fields.ProtectedForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='modified_documents', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vehicledocument',
            name='vehicle',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='documents', to='fleet_management.Vehicle'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='created_by',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_vehicles', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='modified_by',
            field=lib.fields.ProtectedForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='modified_vehicles', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tracker',
            name='address',
            field=lib.fields.ProtectedForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tracker_address', to='operations.Address'),
        ),
        migrations.AddField(
            model_name='tracker',
            name='contact_person',
            field=lib.fields.ProtectedForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tracker_contact', to='operations.Contact'),
        ),
        migrations.AddField(
            model_name='tracker',
            name='vehicle',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tracker', to='fleet_management.Vehicle'),
        ),
        migrations.AddField(
            model_name='purchasedetail',
            name='created_by',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_purchase_detail', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='purchasedetail',
            name='dealership_address',
            field=lib.fields.ProtectedForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='dealership_address', to='operations.Address'),
        ),
        migrations.AddField(
            model_name='purchasedetail',
            name='dealership_contact_person',
            field=lib.fields.ProtectedForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='dealership_contact', to='operations.Contact'),
        ),
        migrations.AddField(
            model_name='purchasedetail',
            name='modified_by',
            field=lib.fields.ProtectedForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='modified_purchase_detail', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='purchasedetail',
            name='vehicle',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='purchase_detail', to='fleet_management.Vehicle'),
        ),
        migrations.AddField(
            model_name='insurance',
            name='broker_address',
            field=lib.fields.ProtectedForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='insurance_broker_address', to='operations.Address'),
        ),
        migrations.AddField(
            model_name='insurance',
            name='broker_contact_person',
            field=lib.fields.ProtectedForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='insurance_broker_contact', to='operations.Contact'),
        ),
        migrations.AddField(
            model_name='insurance',
            name='created_by',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_insurance', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='insurance',
            name='insurer',
            field=lib.fields.ProtectedForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='insurance_insurer', to='operations.Insurer'),
        ),
        migrations.AddField(
            model_name='insurance',
            name='modified_by',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='modified_insurance', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='insurance',
            name='vehicle',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='insurance', to='fleet_management.Vehicle'),
        ),
        migrations.AddField(
            model_name='incident',
            name='created_by',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_incidents', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='incident',
            name='modified_by',
            field=lib.fields.ProtectedForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='modified_incidents', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='incident',
            name='vehicle_driver',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='incident', to='fleet_management.VehicleDriver'),
        ),
        migrations.AddField(
            model_name='historicalvehicletyre',
            name='created_by',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalvehicletyre',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalvehicletyre',
            name='modified_by',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalvehicletyre',
            name='vehicle',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='fleet_management.Vehicle'),
        ),
        migrations.AddField(
            model_name='historicalvehiclemaintenance',
            name='created_by',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalvehiclemaintenance',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalvehiclemaintenance',
            name='modified_by',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalvehiclemaintenance',
            name='vehicle',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='fleet_management.Vehicle'),
        ),
        migrations.AddField(
            model_name='historicalvehicle',
            name='created_by',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalvehicle',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalvehicle',
            name='modified_by',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalpurchasedetail',
            name='created_by',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalpurchasedetail',
            name='dealership_address',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='operations.Address'),
        ),
        migrations.AddField(
            model_name='historicalpurchasedetail',
            name='dealership_contact_person',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='operations.Contact'),
        ),
        migrations.AddField(
            model_name='historicalpurchasedetail',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalpurchasedetail',
            name='modified_by',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalpurchasedetail',
            name='vehicle',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='fleet_management.Vehicle'),
        ),
        migrations.AddField(
            model_name='historicalinsurance',
            name='broker_address',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='operations.Address'),
        ),
        migrations.AddField(
            model_name='historicalinsurance',
            name='broker_contact_person',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='operations.Contact'),
        ),
        migrations.AddField(
            model_name='historicalinsurance',
            name='created_by',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalinsurance',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalinsurance',
            name='insurer',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='operations.Insurer'),
        ),
        migrations.AddField(
            model_name='historicalinsurance',
            name='modified_by',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalinsurance',
            name='vehicle',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='fleet_management.Vehicle'),
        ),
        migrations.AddField(
            model_name='historicalfuelcard',
            name='created_by',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalfuelcard',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalfuelcard',
            name='modified_by',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalfuelcard',
            name='vehicle',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='fleet_management.Vehicle'),
        ),
        migrations.AddField(
            model_name='historicalfinancedetail',
            name='created_by',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalfinancedetail',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalfinancedetail',
            name='modified_by',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalfinancedetail',
            name='purchase_detail',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='fleet_management.PurchaseDetail'),
        ),
        migrations.AddField(
            model_name='historicalbranding',
            name='created_by',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalbranding',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalbranding',
            name='installer_address',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='operations.Address'),
        ),
        migrations.AddField(
            model_name='historicalbranding',
            name='installer_contact_person',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='operations.Contact'),
        ),
        migrations.AddField(
            model_name='historicalbranding',
            name='modified_by',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalbranding',
            name='supplier_address',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='operations.Address'),
        ),
        migrations.AddField(
            model_name='historicalbranding',
            name='supplier_contact_person',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='operations.Contact'),
        ),
        migrations.AddField(
            model_name='historicalbranding',
            name='vehicle',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='fleet_management.Vehicle'),
        ),
        migrations.AddField(
            model_name='fuelcardusage',
            name='fuel_card',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fuel_card_usage', to='fleet_management.FuelCard'),
        ),
        migrations.AddField(
            model_name='fuelcard',
            name='created_by',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_fuel_cards', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='fuelcard',
            name='modified_by',
            field=lib.fields.ProtectedForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='modified_fuel_cards', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='fuelcard',
            name='vehicle',
            field=lib.fields.ProtectedForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='fuel_card', to='fleet_management.Vehicle'),
        ),
        migrations.AddField(
            model_name='financedetail',
            name='created_by',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_finance_detail', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='financedetail',
            name='modified_by',
            field=lib.fields.ProtectedForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='modified_finance_detail', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='financedetail',
            name='purchase_detail',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='finance_detail', to='fleet_management.PurchaseDetail'),
        ),
        migrations.AddField(
            model_name='branding',
            name='created_by',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_trackers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='branding',
            name='installer_address',
            field=lib.fields.ProtectedForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='branding_installer_address', to='operations.Address'),
        ),
        migrations.AddField(
            model_name='branding',
            name='installer_contact_person',
            field=lib.fields.ProtectedForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='branding_installer_contact', to='operations.Contact'),
        ),
        migrations.AddField(
            model_name='branding',
            name='modified_by',
            field=lib.fields.ProtectedForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='modified_trackers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='branding',
            name='supplier_address',
            field=lib.fields.ProtectedForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='branding_supplier_address', to='operations.Address'),
        ),
        migrations.AddField(
            model_name='branding',
            name='supplier_contact_person',
            field=lib.fields.ProtectedForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='branding_supplier_contact', to='operations.Contact'),
        ),
        migrations.AddField(
            model_name='branding',
            name='vehicle',
            field=lib.fields.ProtectedForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='branding', to='fleet_management.Vehicle'),
        ),
    ]
