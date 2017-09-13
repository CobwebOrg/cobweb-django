# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-13 20:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cobweb', '0014_auto_20170913_1321'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='tag_property',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.TextField(max_length=200),
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set([('tag_property', 'name')]),
        ),
    ]
