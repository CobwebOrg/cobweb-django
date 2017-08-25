# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 19:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cobweb', '0003_collection_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgentIdentifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_type', models.CharField(choices=[('SCO', 'Scopus'), ('OTH', 'Other'), ('RID', 'ResearcherID'), ('TWI', 'Twitter Handle'), ('ORC', 'ORCID')], max_length=2, verbose_name='Type')),
                ('value', models.CharField(max_length=200, verbose_name='Value')),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cobweb.Agent')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='claimmd',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='claimmd',
            name='asserted_by',
        ),
        migrations.RemoveField(
            model_name='claimmd',
            name='describes',
        ),
        migrations.DeleteModel(
            name='ClaimMD',
        ),
    ]
