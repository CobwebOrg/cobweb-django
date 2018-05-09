# Generated by Django 2.0.4 on 2018-04-21 22:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('archives', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='holding',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='holdings', to='core.Resource'),
        ),
        migrations.AddField(
            model_name='collection',
            name='administrators',
            field=models.ManyToManyField(blank=True, related_name='collections_administered', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='collection',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='collections', to='core.Organization'),
        ),
    ]