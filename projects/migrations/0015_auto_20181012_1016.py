# Generated by Django 2.1.1 on 2018-10-12 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0014_auto_20181002_2036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='claim',
            name='active',
        ),
        migrations.RemoveField(
            model_name='claim',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='nomination',
            name='deleted',
        ),
    ]
