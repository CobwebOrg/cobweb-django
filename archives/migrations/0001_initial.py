# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-23 02:20
from __future__ import unicode_literals

import core.models
from django.db import migrations, models
import django.db.models.deletion
import webresources.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Claim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(verbose_name='Starting Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Ending Date')),
                ('max_links', models.IntegerField(blank=True, null=True, verbose_name='Maximum Links')),
                ('time_limit', models.DurationField(blank=True, null=True, verbose_name='Time Limit')),
                ('document_limit', models.IntegerField(blank=True, null=True, verbose_name='Document Limit')),
                ('data_limit', models.IntegerField(blank=True, null=True, verbose_name='Data Limit (GB)')),
                ('robot_exclusion_override', models.BooleanField(default=False, verbose_name='Override Robot Exclusion?')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('deprecated', models.DateTimeField(blank=True, null=True, verbose_name='Date Deprecated')),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('deprecated', models.DateTimeField(blank=True, null=True, verbose_name='Date Deprecated')),
                ('raw_metadata', models.TextField(blank=True, null=True)),
                ('identifier', webresources.models.NocryptoURLField(blank=True, null=True, unique=True)),
            ],
            bases=(core.models.ModelValidationMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Holding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raw_metadata', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('deprecated', models.DateTimeField(blank=True, null=True, verbose_name='Date Deprecated')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='archives.Collection')),
            ],
        ),
    ]
