# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RichTextLink'
        db.create_table(u'richtext_richtextlink', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='richtextlink_parent_link', to=orm['contenttypes.ContentType'])),
            ('parent_object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('field', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'richtext', ['RichTextLink'])


    def backwards(self, orm):
        # Deleting model 'RichTextLink'
        db.delete_table(u'richtext_richtextlink')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'richtext.richtextlink': {
            'Meta': {'object_name': 'RichTextLink'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'field': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'parent_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'richtextlink_parent_link'", 'to': u"orm['contenttypes.ContentType']"}),
            'parent_object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['richtext']