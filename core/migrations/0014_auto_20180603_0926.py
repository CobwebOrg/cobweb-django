# Generated by Django 2.0.5 on 2018-06-03 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20180603_0911'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subjectheading',
            old_name='subject',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='tag',
            old_name='text',
            new_name='title',
        ),
    ]