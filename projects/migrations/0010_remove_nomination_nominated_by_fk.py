# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-11 00:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_auto_20180110_1621'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nomination',
            name='nominated_by_fk',
        ),
    ]
