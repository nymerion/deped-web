# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-10 08:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vacancy', '0010_auto_20160310_0847'),
    ]

    operations = [
        migrations.RenameField(
            model_name='position',
            old_name='qs',
            new_name='qualification',
        ),
        migrations.RenameField(
            model_name='qualificationvalue',
            old_name='qs',
            new_name='qualification',
        ),
    ]
