# Generated by Django 2.1.1 on 2018-09-28 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20180917_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='slug',
            field=models.SlugField(help_text='Choose a Cobweb URL for your organization.', unique=True),
        ),
    ]
