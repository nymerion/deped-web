# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-12 09:03
from __future__ import unicode_literals

from django.db import migrations
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('vacancy', '0034_auto_20160510_0830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qualificationvalue',
            name='education',
            field=mezzanine.core.fields.RichTextField(max_length=512),
        ),
        migrations.AlterField(
            model_name='qualificationvalue',
            name='notes',
            field=mezzanine.core.fields.RichTextField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='qualificationvalue',
            name='training',
            field=mezzanine.core.fields.RichTextField(help_text='Relevant training', max_length=512),
        ),
        migrations.AlterField(
            model_name='qualificationvalue',
            name='work_experience',
            field=mezzanine.core.fields.RichTextField(max_length=512),
        ),
    ]