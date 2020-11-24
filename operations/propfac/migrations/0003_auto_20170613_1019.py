# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('propfac', '0002_auto_20170612_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpfcomment',
            name='modified_by',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='pfcomment',
            name='modified_by',
            field=models.ForeignKey(related_name='user_modified_propfac_comments', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
