# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('offices', '0004_auto_20170614_1633'),
        ('employees', '0004_auto_20170619_1422'),
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('book_type', models.CharField(default=b'Operational', max_length=120, null=True, blank=True)),
                ('written_by', models.CharField(default=b'Operational', max_length=20, null=True, blank=True, choices=[(b'sales', b'Sales Department'), (b'marketing', b'Marketing Departrment')])),
                ('quantity', models.FloatField(default=0, max_length=20, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='BookAllocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('range_from', models.CharField(default=b'Operational', max_length=120, null=True, blank=True)),
                ('range_to', models.CharField(default=b'Operational', max_length=120, null=True, blank=True)),
                ('quantity', models.FloatField(default=0, max_length=20, null=True, blank=True)),
                ('date_allocated', models.DateField(null=True, blank=True)),
                ('accept', models.BooleanField(default=False)),
                ('authorize', models.CharField(default=b'Pending', max_length=20, null=True, blank=True, choices=[(b'Pending', b'Pending'), (b'Aproved', b'Authorize'), (b'Declined', b'Decline')])),
                ('book', models.ForeignKey(related_name='book_bookallocations', to='stock.Book')),
                ('created_by', models.ForeignKey(related_name='user_bookallocations', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='user_modified_bookallocations', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('region', models.ForeignKey(related_name='region_bookallocations', to='offices.Region')),
                ('regional_admin_manager', models.ForeignKey(related_name='ram_bookallocations', to='employees.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='BookReplenishment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('range_from', models.CharField(default=b'Operational', max_length=120, null=True, blank=True)),
                ('range_to', models.CharField(default=b'Operational', max_length=120, null=True, blank=True)),
                ('quantity', models.FloatField(default=0, max_length=20, null=True, blank=True)),
                ('date_ordered', models.DateField(null=True, blank=True)),
                ('date_recieved', models.DateField(null=True, blank=True)),
                ('recieved', models.BooleanField(default=False)),
                ('accept', models.BooleanField(default=False)),
                ('authorize', models.CharField(default=b'Pending', max_length=20, null=True, blank=True, choices=[(b'Pending', b'Pending'), (b'Aproved', b'Authorize'), (b'Declined', b'Decline')])),
                ('book', models.ForeignKey(related_name='book_bookreplenishment', to='stock.Book')),
                ('created_by', models.ForeignKey(related_name='user_bookreplenishment', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='user_modified_bookreplenishment', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalBookAllocation',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('range_from', models.CharField(default=b'Operational', max_length=120, null=True, blank=True)),
                ('range_to', models.CharField(default=b'Operational', max_length=120, null=True, blank=True)),
                ('quantity', models.FloatField(default=0, max_length=20, null=True, blank=True)),
                ('date_allocated', models.DateField(null=True, blank=True)),
                ('accept', models.BooleanField(default=False)),
                ('authorize', models.CharField(default=b'Pending', max_length=20, null=True, blank=True, choices=[(b'Pending', b'Pending'), (b'Aproved', b'Authorize'), (b'Declined', b'Decline')])),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('book', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='stock.Book', null=True)),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('region', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='offices.Region', null=True)),
                ('regional_admin_manager', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='employees.Employee', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical book allocation',
            },
        ),
        migrations.CreateModel(
            name='HistoricalBookReplenishment',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('range_from', models.CharField(default=b'Operational', max_length=120, null=True, blank=True)),
                ('range_to', models.CharField(default=b'Operational', max_length=120, null=True, blank=True)),
                ('quantity', models.FloatField(default=0, max_length=20, null=True, blank=True)),
                ('date_ordered', models.DateField(null=True, blank=True)),
                ('date_recieved', models.DateField(null=True, blank=True)),
                ('recieved', models.BooleanField(default=False)),
                ('accept', models.BooleanField(default=False)),
                ('authorize', models.CharField(default=b'Pending', max_length=20, null=True, blank=True, choices=[(b'Pending', b'Pending'), (b'Aproved', b'Authorize'), (b'Declined', b'Decline')])),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('book', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='stock.Book', null=True)),
                ('created_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical book replenishment',
            },
        ),
    ]
