# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-11 02:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vacancy', '0014_auto_20160311_0204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qualificationvalue',
            name='position',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='qualification_standards', to='vacancy.Position'),
        ),
    ]