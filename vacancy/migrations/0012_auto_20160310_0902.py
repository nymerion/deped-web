# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-10 09:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancy', '0011_auto_20160310_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qualificationvalue',
            name='education',
            field=models.CharField(max_length=256),
        ),
    ]