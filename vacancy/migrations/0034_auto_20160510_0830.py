# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-10 08:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancy', '0033_auto_20160506_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qualificationvalue',
            name='eligibility',
            field=models.CharField(blank=True, choices=[('LET/PBET', 'LET/PBET'), ('RA1080', 'RA 1080'), ('PD907', 'PD 907'), ('CSC1', 'CSC LVL 1'), ('CSC2', 'CSC LVL 2'), ('CESO', 'CESO')], default='LET/PBET', max_length=8, null=True),
        ),
    ]
