# Generated by Django 2.1.1 on 2018-09-06 21:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_auto_20180823_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nomination',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='nominations', to='core.Resource', verbose_name='URL'),
        ),
    ]
