# Generated by Django 2.1.1 on 2018-10-12 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20181002_2022'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='terms_accepted',
            field=models.BooleanField(default=False, verbose_name="By establishing a Cobweb account, I have read and agree to Cobweb's Terms of Use"),
        ),
    ]
