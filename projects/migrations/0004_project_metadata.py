# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-04 22:39
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20171004_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='metadata',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
