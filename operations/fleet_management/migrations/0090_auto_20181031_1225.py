# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-10-31 10:25
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fleet_management', '0089_merge_20180926_1004'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalVehicleStatus',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('comment', models.TextField(blank=True, default=None, null=True)),
                ('deleted', models.BooleanField(db_index=True, default=False)),
                ('changed_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('changed_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical vehicle status',
            },
        ),
        migrations.CreateModel(
            name='VehicleStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('comment', models.TextField(blank=True, default=None, null=True)),
                ('deleted', models.BooleanField(db_index=True, default=False)),
                ('changed_at', models.DateTimeField(auto_now=True, null=True)),
                ('changed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='status_changed_by', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='status_capture_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'default_permissions': [],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VehicleStatusType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('changed_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted', models.BooleanField(db_index=True, default=False)),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
            ],
            options={
                'default_permissions': [],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='historicalvehicle',
            name='service_area',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name=b'Service Area'),
        ),
        migrations.AddField(
            model_name='historicalvehicle',
            name='updated_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name=b'Odometer Updated Date'),
        ),
        migrations.AddField(
            model_name='historicalvehicle',
            name='updated_mileage',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name=b'Updated Odometer Mileage'),
        ),
        migrations.AddField(
            model_name='tracker',
            name='tracking_source',
            field=models.CharField(default=b'None', max_length=15),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='service_area',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name=b'Service Area'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='updated_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name=b'Odometer Updated Date'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='updated_mileage',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name=b'Updated Odometer Mileage'),
        ),
        migrations.AddField(
            model_name='vehicledriver',
            name='unassign_reason',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vehiclestatus',
            name='status_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_status_type', to='fleet_management.VehicleStatusType'),
        ),
        migrations.AddField(
            model_name='vehiclestatus',
            name='vehicle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_status', to='fleet_management.Vehicle'),
        ),
        migrations.AddField(
            model_name='historicalvehiclestatus',
            name='status_type',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='fleet_management.VehicleStatusType'),
        ),
        migrations.AddField(
            model_name='historicalvehiclestatus',
            name='vehicle',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='fleet_management.Vehicle'),
        ),
        migrations.AddField(
            model_name='historicalvehicle',
            name='status',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='fleet_management.VehicleStatusType'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fleet_management.VehicleStatusType'),
        ),
    ]