# Generated by Django 2.1.1 on 2018-09-14 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webarchives', '0006_auto_20180910_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importedrecord',
            name='resource',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='imported_records', to='core.Resource'),
        ),
    ]
