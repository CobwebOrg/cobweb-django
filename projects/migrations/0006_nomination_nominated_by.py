# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-10 22:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0005_auto_20180110_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='nomination',
            name='nominated_by',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
