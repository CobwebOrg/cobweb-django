# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-07 20:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cobweb', '0005_auto_20170906_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
    ]