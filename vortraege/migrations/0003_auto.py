# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field event on 'Talk'
        db.create_table('vortraege_talk_event', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('talk', models.ForeignKey(orm['vortraege.talk'], null=False)),
            ('event', models.ForeignKey(orm['vortraege.event'], null=False))
        ))
        db.create_unique('vortraege_talk_event', ['talk_id', 'event_id'])


    def backwards(self, orm):
        # Removing M2M table for field event on 'Talk'
        db.delete_table('vortraege_talk_event')


    models = {
        'vortraege.event': {
            'Meta': {'object_name': 'Event'},
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'vortraege.talk': {
            'Meta': {'object_name': 'Talk'},
            'audio': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['vortraege.Event']", 'symmetrical': 'False'}),
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