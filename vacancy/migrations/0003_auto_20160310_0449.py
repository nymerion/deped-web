# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-10 04:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vacancy', '0002_auto_20160310_0445'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='registry',
            options={'verbose_name': 'RQA Entry', 'verbose_name_plural': 'RQA Entries'},
        ),
    ]
