# Generated by Django 2.1.1 on 2018-09-25 19:27

import itertools
from django.db import migrations, models


forward_map = {
    'Daily': "daily",
    'Weekly': "weekly",
    'Monthly': "monthly",
}

reverse_map = {v: k for k, v in forward_map.items()}

def migrate_data_forward(apps, schema_editor):
    instances = itertools.chain(
        apps.get_model('projects', 'Nomination').objects.all(),
        apps.get_model('projects', 'Nomination').objects.all(),
    )
    for instance in instances:
        if instance.crawl_frequency:
            instance.crawl_frequency = forward_map.get(instance.crawl_frequency)
            instance.save()

def migrate_data_backward(apps, schema_editor):
    instances = itertools.chain(
        apps.get_model('projects', 'Nomination').objects.all(),
        apps.get_model('projects', 'Nomination').objects.all(),
    )
    for instance in instances:
        if instance.crawl_frequency:
            instance.crawl_frequency = reverse_map.get(instance.crawl_frequency)
            instance.save()


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_nomination_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='claim',
            name='ignore_robots_txt',
            field=models.BooleanField(default=False, verbose_name="ignore 'robots.txt'"),
        ),
        migrations.AddField(
            model_name='claim',
            name='rights_considerations',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='nomination',
            name='ignore_robots_txt',
            field=models.BooleanField(default=False, verbose_name="ignore 'robots.txt'"),
        ),
        migrations.AddField(
            model_name='nomination',
            name='rights_considerations',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='claim',
            name='crawl_frequency',
            field=models.CharField(blank=True, choices=[('one time', 'one time'), ('twice daily', 'twice daily'), ('daily', 'daily'), ('weekly', 'weekly'), ('monthly', 'monthly'), ('quarterly', 'quarterly'), ('annually', 'annually')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='claim',
            name='follow_links',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2)], null=True),
        ),
        migrations.AlterField(
            model_name='claim',
            name='page_scope',
            field=models.CharField(blank=True, choices=[('Page', 'Page'), ('Domain', 'Domain')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='nomination',
            name='crawl_frequency',
            field=models.CharField(blank=True, choices=[('one time', 'one time'), ('twice daily', 'twice daily'), ('daily', 'daily'), ('weekly', 'weekly'), ('monthly', 'monthly'), ('quarterly', 'quarterly'), ('annually', 'annually')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='nomination',
            name='follow_links',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2)], null=True),
        ),
        migrations.AlterField(
            model_name='nomination',
            name='page_scope',
            field=models.CharField(blank=True, choices=[('Page', 'Page'), ('Domain', 'Domain')], max_length=50, null=True),
        ),
        migrations.RunPython(
            migrate_data_forward,
            migrate_data_backward,
        ),
    ]