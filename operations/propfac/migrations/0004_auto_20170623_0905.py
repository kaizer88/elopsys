# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('propfac', '0003_auto_20170613_1019'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalpfrequisition',
            old_name='quote_number',
            new_name='quotation1',
        ),
        migrations.RenameField(
            model_name='pfrequisition',
            old_name='quote_number',
            new_name='quotation1',
        ),
        migrations.AddField(
            model_name='historicalpfrequisition',
            name='amount',
            field=models.FloatField(default=0, max_length=20, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalpfrequisition',
            name='authorized',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalpfrequisition',
            name='authorized_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='historicalpfrequisition',
            name='budgeted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalpfrequisition',
            name='finalized',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalpfrequisition',
            name='finalized_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='historicalpfrequisition',
            name='mortivation',
            field=models.CharField(default=None, max_length=2000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalpfrequisition',
            name='quotation2',
            field=models.CharField(default=None, max_length=120),
        ),
        migrations.AddField(
            model_name='pfrequisition',
            name='amount',
            field=models.FloatField(default=0, max_length=20, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='pfrequisition',
            name='authorized',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pfrequisition',
            name='authorized_by',
            field=models.ForeignKey(related_name='authorizer_propfac_requisitions', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='pfrequisition',
            name='budgeted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pfrequisition',
            name='finalized',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pfrequisition',
            name='finalized_by',
            field=models.ForeignKey(related_name='finalizer_propfac_requisitions', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='pfrequisition',
            name='mortivation',
            field=models.CharField(default=None, max_length=2000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='pfrequisition',
            name='quotation2',
            field=models.CharField(default=None, max_length=120),
        ),
    ]
