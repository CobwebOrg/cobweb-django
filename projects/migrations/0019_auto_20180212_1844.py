# Generated by Django 2.0.1 on 2018-02-13 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0018_auto_20180206_1530'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nomination',
            name='metadata',
        ),
        migrations.AddField(
            model_name='nomination',
            name='status',
            field=models.CharField(choices=[('Rejected', 'The site should not be crawled for this project.'), ('Unclaimed', 'No archive has committed to crawling this site.'), ('Underclaimed', 'Needs more claiming archives or more frequent crawling.'), ('Claimed', 'Current claims are enough for this site.')], default='Unclaimed', max_length=11),
        ),
    ]
