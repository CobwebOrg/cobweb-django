# Generated by Django 2.0.8 on 2018-08-23 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_remove_project_any_user_can_nominate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='nomination_policy',
            field=models.CharField(choices=[('Public', "Public: anyone can nominate, even if they're not logged in."), ('Cobweb users', 'Cobweb users: anyone with a Cobweb account can nominate.'), ('Restricted', 'Restricted: only selected users and organizations can nominate.')], default='Public', max_length=12),
        ),
    ]
