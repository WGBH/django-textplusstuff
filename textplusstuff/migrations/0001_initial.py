# -*- coding: utf-8 -*-
# flake8: noqa
from __future__ import unicode_literals

from django.db import models, migrations
import textplusstuff.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
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
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL, help_text='The user who created this draft.')),
            ],
            options={
                'verbose_name': 'Text Plus Stuff Draft',
                'verbose_name_plural': 'Text Plus Stuff Drafts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TextPlusStuffLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parent_object_id', models.PositiveIntegerField()),
                ('object_id', models.CharField(max_length=25)),
                ('field', models.CharField(max_length=50, verbose_name='Field')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('parent_content_type', models.ForeignKey(related_name='textplusstufflink_parent_link', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Text Plus Stuff Links',
            },
            bases=(models.Model,),
        ),
    ]
