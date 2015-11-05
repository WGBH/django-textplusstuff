# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('textplusstuff', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textplusstufflink',
            name='object_id',
            field=models.CharField(max_length=25, db_index=True),
        ),
        migrations.AlterField(
            model_name='textplusstufflink',
            name='parent_object_id',
            field=models.PositiveIntegerField(db_index=True),
        ),
    ]
