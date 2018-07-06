# Generated by Django 2.0.5 on 2018-06-09 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('webarchives', '0002_auto_20180608_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='importedrecord',
            name='resource',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.Resource'),
        ),
    ]