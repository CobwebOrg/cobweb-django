# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-14 15:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasources', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apiendpoint',
            name='agent',
        ),
    ]