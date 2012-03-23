# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_table('app_calendarentry', 'app_event')
        db.rename_column('app_gig', 'calendarentry_ptr_id', 'event_ptr_id')
        db.rename_column('app_rehearsal', 'calendarentry_ptr_id', 'event_ptr_id')

    def backwards(self, orm):
        db.rename_table('app_event', 'app_calendarentry')
        db.rename_column('app_gig', 'event_ptr_id', 'calendarentry_ptr_id')
        db.rename_column('app_rehearsal', 'event_ptr_id', 'calendarentry_ptr_id')


    models = {
        'app.event': {
            'Meta': {'ordering': "['date']", 'object_name': 'Event'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'insiderinfo': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'time_location': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'app.gig': {
            'Meta': {'ordering': "['date']", 'object_name': 'Gig', '_ormbases': ['app.Event']},
            'event_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['app.Event']", 'unique': 'True', 'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'signup': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'time_hole': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'time_playing': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'app.mailverificationsent': {
            'Meta': {'object_name': 'MailVerificationSent'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sent': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'app.rehearsal': {
            'Meta': {'ordering': "['date']", 'object_name': 'Rehearsal', '_ormbases': ['app.Event']},
            'event_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['app.Event']", 'unique': 'True', 'primary_key': 'True'}),
            'fika': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "u'H\\xe5lan'", 'max_length': '128'}),
            'signup': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'time_hole': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(19, 0)'})
        }
    }

    complete_apps = ['app']
