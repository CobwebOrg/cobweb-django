# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-13 22:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cobweb', '0017_auto_20170913_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='tag_property',
            field=models.TextField(default='tag'),
        ),
    ]
