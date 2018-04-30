# Generated by Django 2.0.4 on 2018-04-30 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20180430_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='affiliations',
            field=models.ManyToManyField(blank=True, related_name='affiliated_users', through='core.Affiliation', to='core.Organization'),
        ),
    ]
