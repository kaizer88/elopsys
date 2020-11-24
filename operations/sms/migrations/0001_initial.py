# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
        ('fleet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmsMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=350, verbose_name='Content')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Phone Number')),
                ('created', models.DateTimeField()),
                ('sent', models.NullBooleanField(default=None, verbose_name='Sent', editable=False)),
                ('last_attempt', models.DateTimeField(verbose_name='Last attempt', null=True, editable=False, blank=True)),
                ('error_msg', models.TextField(null=True, verbose_name='Last error', blank=True)),
                ('driver', models.ForeignKey(related_name='driver_smses', blank=True, to='employees.Employee', null=True)),
                ('vehicle', models.ForeignKey(related_name='vehicle_smses', blank=True, to='fleet.Vehicle', null=True)),
            ],
        ),
    ]
