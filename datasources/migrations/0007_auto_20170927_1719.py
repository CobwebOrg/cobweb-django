# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-28 00:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasources', '0006_apiendpoint_metadata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiendpoint',
            name='metadata',
            field=models.ManyToManyField(blank=True, to='metadata.Metadatum'),
        ),
    ]
