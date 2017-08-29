# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 21:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cobweb', '0005_auto_20170825_1217'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='institution',
            name='created',
        ),
        migrations.RemoveField(
            model_name='institution',
            name='deprecated',
        ),
        migrations.RemoveField(
            model_name='institution',
            name='description',
        ),
        migrations.AddField(
            model_name='institutionmd',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Date Created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='institutionmd',
            name='deprecated',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Date Deprecated'),
        ),
        migrations.AddField(
            model_name='institutionmd',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='institutionmd',
            name='institution_type',
            field=models.CharField(choices=[('arc', 'Archive'), ('dat', 'Datacenter'), ('dpt', 'Department'), ('div', 'Division'), ('lab', 'Laboratory'), ('lib', 'Library'), ('mus', 'Museum'), ('pro', 'Project'), ('oth', 'Other')], default='oth', max_length=3, verbose_name='Type'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='institutionmd',
            name='sector',
            field=models.CharField(choices=[('a', 'Academic'), ('c', 'Corporate'), ('g', 'Government'), ('n', 'Non-Profit'), ('o', 'Other')], default='o', max_length=1, verbose_name='Sector'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='agentidentifier',
            name='id_type',
            field=models.CharField(choices=[('ORC', 'ORCID'), ('RID', 'ResearcherID'), ('SCO', 'Scopus'), ('TWI', 'Twitter Handle'), ('OTH', 'Other')], max_length=3, verbose_name='Type'),
        ),
    ]