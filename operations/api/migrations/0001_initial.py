# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


def create_user(apps, schema_editor):
    User = apps.get_registered_model('accounts', 'ElopsysUser')
    u = User(username='elipsys_api_user',
             email='',
             password=make_password('QuUpRya8j3ewgH?@'),
             is_superuser=False,
             is_staff=False)
    u.save()


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(create_user)
    ]
