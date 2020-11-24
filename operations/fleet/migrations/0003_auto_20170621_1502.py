# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fleet', '0002_auto_20170605_1143'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalrequisition',
            old_name='quote_number',
            new_name='quotation_1',
        ),
        migrations.RenameField(
            model_name='requisition',
            old_name='quote_number',
            new_name='quotation_1',
        ),
        migrations.AddField(
            model_name='historicalrequisition',
            name='amount',
            field=models.FloatField(default=0, max_length=20, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalrequisition',
            name='authorized',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalrequisition',
            name='authorized_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='historicalrequisition',
            name='budjeted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalrequisition',
            name='finalized',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalrequisition',
            name='finalized_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='historicalrequisition',
            name='mortivation',
            field=models.CharField(default=None, max_length=2000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalrequisition',
            name='quotation_2',
            field=models.CharField(default=None, max_length=120),
        ),
        migrations.AddField(
            model_name='requisition',
            name='amount',
            field=models.FloatField(default=0, max_length=20, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='requisition',
            name='authorized',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='requisition',
            name='authorized_by',
            field=models.ForeignKey(related_name='authorizer_requisitions', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='requisition',
            name='budjeted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='requisition',
            name='finalized',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='requisition',
            name='finalized_by',
            field=models.ForeignKey(related_name='finalizer_requisitions', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='requisition',
            name='mortivation',
            field=models.CharField(default=None, max_length=2000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='requisition',
            name='quotation_2',
            field=models.CharField(default=None, max_length=120),
        ),
    ]
