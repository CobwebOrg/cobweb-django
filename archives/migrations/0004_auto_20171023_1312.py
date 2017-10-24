# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-23 20:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0001_initial'),
        ('archives', '0003_auto_20171017_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='collection',
            name='keywords',
            field=models.ManyToManyField(blank=True, to='metadata.Keyword'),
        ),
    ]
