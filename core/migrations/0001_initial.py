# Generated by Django 2.0.5 on 2018-06-04 22:22

import cobweb.models
import core.models
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('languages_plus', '0004_auto_20171214_0004'),
        ('auth', '0009_alter_user_last_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=200, null=True)),
                ('last_name', models.CharField(max_length=200, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('professional_title', models.CharField(blank=True, max_length=200, null=True)),
                ('url', core.models.NormalizedURLField(blank=True, null=True)),
                ('get_notification_emails', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=(cobweb.models.CobwebModelMixin, models.Model),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='CrawlScope',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('max_time', models.PositiveIntegerField(blank=True, null=True)),
                ('max_size', models.PositiveIntegerField(blank=True, null=True)),
                ('max_resources', models.PositiveIntegerField(blank=True, null=True)),
                ('override_robot_exclusion', models.NullBooleanField(default=False)),
                ('boundary_behavior', models.CharField(blank=True, choices=[('Page', 'Page'), ('Site', 'Site'), ('Host', 'Host'), ('Domain', 'Domain')], max_length=200, null=True)),
                ('max_embedded_links', models.PositiveIntegerField(blank=True, null=True)),
                ('max_content_links', models.PositiveIntegerField(blank=True, null=True)),
                ('format_behavior', models.CharField(blank=True, choices=[('All', 'All'), ('PDF-Only', 'PDF-Only')], default='All', max_length=200, null=True)),
                ('technology', models.CharField(blank=True, choices=[('Archive-It', 'Archive-It'), ('Brozzler', 'Brozzler'), ('Crawler4j', 'Crawler4j'), ('Crawljax', 'Crawljax'), ('Heritrix', 'Heritrix'), ('HTTrack', 'HTTrack'), ('NetarchiveSuite', 'NetarchiveSuite'), ('Nutch', 'Nutch'), ('Social Feed Manager', 'Social Feed Manager'), ('WebRecorder', 'WebRecorder'), ('Wget', 'Wget'), ('Other', 'Other'), ('Unknown', 'Unknown')], default='Unknown', max_length=200, null=True)),
            ],
            bases=(cobweb.models.CobwebModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when_created', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.PositiveIntegerField()),
                ('visibility', models.CharField(choices=[('Public', 'Public'), ('Project Members', 'Project Members'), ('Project Admins', 'Project Administrators')], default='Public', max_length=20)),
                ('text', models.TextField()),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notes', to=settings.AUTH_USER_MODEL)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            bases=(cobweb.models.CobwebModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=2000, unique=True, verbose_name='full legal name')),
                ('short_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='short name, nickname, or acronym')),
                ('address', models.TextField(blank=True, null=True)),
                ('telephone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True)),
                ('url', core.models.NormalizedURLField(blank=True, null=True)),
                ('email_address', models.EmailField(blank=True, max_length=254, null=True)),
                ('description', models.TextField(blank=True, null=True, verbose_name='description of mission and collecting policy')),
                ('identifier', core.models.NormalizedURLField(blank=True, editable=False, null=True, unique=True, verbose_name='Archive-It.org Identifier')),
                ('administrators', models.ManyToManyField(related_name='organizations_administered', to=settings.AUTH_USER_MODEL)),
                ('contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contact_for', to=settings.AUTH_USER_MODEL)),
                ('parent_organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Organization')),
            ],
            bases=(cobweb.models.CobwebModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', core.models.NormalizedURLField(max_length=1000, unique=True)),
                ('when_checked', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Redirected', 'Redirected'), ('Inactive', 'Inactive'), ('Unknown', 'Unknown')], default='Unknown', max_length=50)),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='languages_plus.Language')),
            ],
            bases=(cobweb.models.CobwebModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ResourceDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('asserted_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='languages_plus.Language')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Resource')),
            ],
            bases=(cobweb.models.CobwebModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SubjectHeading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
            ],
            bases=(cobweb.models.CobwebModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=200, unique=True)),
            ],
            bases=(cobweb.models.CobwebModelMixin, models.Model),
        ),
        migrations.AddField(
            model_name='resourcedescription',
            name='subject_headings',
            field=models.ManyToManyField(blank=True, to='core.SubjectHeading'),
        ),
        migrations.AddField(
            model_name='resourcedescription',
            name='tags',
            field=models.ManyToManyField(blank=True, to='core.Tag'),
        ),
        migrations.AddField(
            model_name='crawlscope',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Organization'),
        ),
        migrations.AddField(
            model_name='user',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='affiliated_users', to='core.Organization'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='resourcedescription',
            unique_together={('resource', 'asserted_by')},
        ),
        migrations.AlterUniqueTogether(
            name='crawlscope',
            unique_together={('title', 'organization')},
        ),
    ]
