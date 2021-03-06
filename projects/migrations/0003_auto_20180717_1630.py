# Generated by Django 2.0.5 on 2018-07-17 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20180604_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='claim',
            name='crawl_end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='claim',
            name='crawl_frequency',
            field=models.CharField(blank=True, choices=[('Hourly', 'Hourly'), ('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Monthly', 'Monthly')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='claim',
            name='crawl_start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='claim',
            name='follow_links',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='claim',
            name='page_scope',
            field=models.CharField(blank=True, choices=[('Page', 'Page'), ('Site', 'Site'), ('Domain', 'Domain')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='nomination',
            name='suggested_crawl_start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='nomination',
            name='suggested_follow_links',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='nomination',
            name='suggested_page_scope',
            field=models.CharField(blank=True, choices=[('Page', 'Page'), ('Site', 'Site'), ('Domain', 'Domain')], max_length=50, null=True),
        ),
    ]
