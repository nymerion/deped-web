# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-02 09:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vacancy', '0028_auto_20160502_0900'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='person',
            unique_together=set([('first_name', 'last_name', 'name_ext')]),
        ),
    ]
