# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-27 20:01
from __future__ import unicode_literals

from django.db import migrations, models
import webresources.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', webresources.models.NocryptoURLField(unique=True)),
                ('nominated_projects', models.ManyToManyField(related_name='nominated_resources', through='projects.Nomination', to='projects.Project')),
            ],
        ),
    ]
