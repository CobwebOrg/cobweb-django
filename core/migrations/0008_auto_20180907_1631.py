# Generated by Django 2.1.1 on 2018-09-07 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_organization_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]