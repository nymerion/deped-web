# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-30 10:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20150527_1555'),
        ('vacancy', '0025_auto_20160329_1022'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='schoolyear',
            options={'ordering': ('_order',)},
        ),
        migrations.RemoveField(
            model_name='schoolyear',
            name='id',
        ),
        migrations.AddField(
            model_name='schoolyear',
            name='page_ptr',
            field=models.OneToOneField(auto_created=True, default=-1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pages.Page'),
            preserve_default=False,
        ),
    ]
