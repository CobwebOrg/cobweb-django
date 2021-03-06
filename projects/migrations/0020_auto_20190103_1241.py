# Generated by Django 2.1.2 on 2019-01-03 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0019_auto_20181026_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claim',
            name='intended_crawling_tool',
            field=models.CharField(blank=True, choices=[('Archive-It', 'Archive-It'), ('Brozzler', 'Brozzler'), ('Heritrix 1', 'Heritrix 1'), ('Heritrix 3', 'Heritrix 3'), ('Webrecorder', 'Webrecorder'), ('Other', 'Other')], max_length=50, null=True, verbose_name='Crawling tool'),
        ),
        migrations.AlterField(
            model_name='nomination',
            name='intended_crawling_tool',
            field=models.CharField(blank=True, choices=[('Archive-It', 'Archive-It'), ('Brozzler', 'Brozzler'), ('Heritrix 1', 'Heritrix 1'), ('Heritrix 3', 'Heritrix 3'), ('Webrecorder', 'Webrecorder'), ('Other', 'Other')], max_length=50, null=True, verbose_name='Crawling tool'),
        ),
    ]
