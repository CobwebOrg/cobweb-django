# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-11 21:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archives', '0006_auto_20171211_1251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='name',
        ),
    ]
