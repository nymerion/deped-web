# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-21 05:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20150527_1555'),
        ('vacancy', '0021_auto_20160317_0221'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vacancy',
            options={'ordering': ('_order',), 'verbose_name': 'Vacancy', 'verbose_name_plural': 'Vacancies'},
        ),
        migrations.RemoveField(
            model_name='vacancy',
            name='id',
        ),
        migrations.AddField(
            model_name='vacancy',
            name='page_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pages.Page'),
            preserve_default=False,
        ),
    ]
