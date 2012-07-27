# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Talk'
        db.create_table('vortraege_talk', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('speaker', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('organiser', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('presstext', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('poster', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('flyer', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('slides', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('audio', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('vortraege', ['Talk'])


    def backwards(self, orm):
        # Deleting model 'Talk'
        db.delete_table('vortraege_talk')


    models = {
        'vortraege.talk': {
            'Meta': {'object_name': 'Talk'},
            'audio': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'flyer': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organiser': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'poster': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'presstext': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'slides': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'speaker': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['vortraege']