# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-19 22:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webresources', '0004_auto_20171019_1406'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resource',
            old_name='location',
            new_name='url',
        ),
    ]