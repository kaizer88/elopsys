# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_book_bookallocation_bookreplenishment_historicalbookallocation_historicalbookreplenishment'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookreplenishment',
            name='in_stock',
            field=models.FloatField(default=0, max_length=20, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalbookreplenishment',
            name='in_stock',
            field=models.FloatField(default=0, max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='book_type',
            field=models.CharField(max_length=120, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='written_by',
            field=models.CharField(default=None, max_length=20, null=True, blank=True, choices=[(b'sales', b'Sales Department'), (b'marketing', b'Marketing Departrment')]),
        ),
        migrations.AlterField(
            model_name='bookallocation',
            name='range_from',
            field=models.CharField(max_length=120, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bookallocation',
            name='range_to',
            field=models.CharField(max_length=120, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalbookallocation',
            name='range_from',
            field=models.CharField(max_length=120, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalbookallocation',
            name='range_to',
            field=models.CharField(max_length=120, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalstockitem',
            name='category',
            field=models.CharField(default=None, max_length=20, null=True, blank=True, choices=[(b'grocery', b'Grocery'), (b'sanitation', b'Sanitation'), (b'stationary', b'Stationary')]),
        ),
        migrations.AlterField(
            model_name='stockitem',
            name='category',
            field=models.CharField(default=None, max_length=20, null=True, blank=True, choices=[(b'grocery', b'Grocery'), (b'sanitation', b'Sanitation'), (b'stationary', b'Stationary')]),
        ),
    ]
