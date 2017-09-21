# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-21 15:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cobweb', '0031_auto_20170921_0845'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='parents',
            field=models.ManyToManyField(related_name='children', to='cobweb.Institution'),
        ),
    ]
