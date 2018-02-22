# -*- coding: utf-8 -*-
# flake8: noqa

from django.conf import settings
from django.db import models, migrations
import django.db.models.deletion
import textplusstuff.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextPlusStuffDraft',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='Draft Title')),
                ('date_created', models.DateTimeField(help_text='The date this draft was originally created.', verbose_name='Date Created', auto_now_add=True)),
                ('date_modified', models.DateTimeField(help_text='The date this draft was updated.', verbose_name='Date Modified', auto_now=True)),
                ('content', textplusstuff.fields.TextPlusStuffField(verbose_name='Content', blank=True)),
                ('content_ported', models.BooleanField(default=False, help_text='Signifies whether or not this draft has been used to populate a TextPlusStuffField on another model.', verbose_name='Content Ported')),
                ('user', models.ForeignKey(help_text='The user who created this draft.', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Text Plus Stuff Draft',
                'verbose_name_plural': 'Text Plus Stuff Drafts',
            },
        ),
        migrations.CreateModel(
            name='TextPlusStuffLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parent_object_id', models.PositiveIntegerField()),
                ('object_id', models.CharField(max_length=25)),
                ('field', models.CharField(max_length=50, verbose_name='Field')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('parent_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='textplusstufflink_parent_link', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Text Plus Stuff Links',
            },
        ),
    ]
