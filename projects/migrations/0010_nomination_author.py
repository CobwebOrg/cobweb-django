# Generated by Django 2.1.1 on 2018-09-17 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_auto_20180906_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='nomination',
            name='author',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
