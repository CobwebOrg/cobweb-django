# Generated by Django 2.0.1 on 2018-01-23 19:02

from django.db import migrations
import metadata.models


class Migration(migrations.Migration):

    dependencies = [
        ('archives', '0004_auto_20180115_1120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='raw_metadata',
        ),
        migrations.RemoveField(
            model_name='holding',
            name='raw_metadata',
        ),
        migrations.AlterField(
            model_name='collection',
            name='metadata',
            field=metadata.models.MetadataJSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='holding',
            name='metadata',
            field=metadata.models.MetadataJSONField(blank=True, null=True),
        ),
    ]
