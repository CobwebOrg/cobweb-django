# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-28 00:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metadatum',
            name='name',
            field=models.CharField(db_index=True, max_length=200),
        ),
    ]
