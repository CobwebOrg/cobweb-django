# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-27 20:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('archives', '0001_initial'),
        ('webresources', '0001_initial'),
        ('core', '0001_initial'),
        ('metadata', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='holding',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webresources.Resource'),
        ),
        migrations.AddField(
            model_name='collection',
            name='metadata',
            field=models.ManyToManyField(to='metadata.Metadatum'),
        ),
        migrations.AddField(
            model_name='collection',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.Organization'),
        ),
        migrations.AddField(
            model_name='claim',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='archives.Collection'),
        ),
        migrations.AddField(
            model_name='claim',
            name='metadata',
            field=models.ManyToManyField(to='metadata.Metadatum'),
        ),
        migrations.AddField(
            model_name='claim',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webresources.Resource'),
        ),
    ]
