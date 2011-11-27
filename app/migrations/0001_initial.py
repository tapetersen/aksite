# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'CalendarEntry'
        db.create_table('app_calendarentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('time_location', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('insiderinfo', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('info', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('app', ['CalendarEntry'])

        # Adding model 'Rehearsal'
        db.create_table('app_rehearsal', (
            ('calendarentry_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['app.CalendarEntry'], unique=True, primary_key=True)),
            ('fika', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('location', self.gf('django.db.models.fields.CharField')(default=u'H\xe5lan', max_length=128)),
            ('time_hole', self.gf('django.db.models.fields.TimeField')(default=datetime.time(19, 0))),
            ('signup', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('app', ['Rehearsal'])

        # Adding model 'Gig'
        db.create_table('app_gig', (
            ('calendarentry_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['app.CalendarEntry'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('time_playing', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('time_hole', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('signup', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('app', ['Gig'])


    def backwards(self, orm):
        
        # Deleting model 'CalendarEntry'
        db.delete_table('app_calendarentry')

        # Deleting model 'Rehearsal'
        db.delete_table('app_rehearsal')

        # Deleting model 'Gig'
        db.delete_table('app_gig')


    models = {
        'app.calendarentry': {
            'Meta': {'ordering': "['date']", 'object_name': 'CalendarEntry'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'insiderinfo': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'time_location': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'app.gig': {
            'Meta': {'ordering': "['date']", 'object_name': 'Gig', '_ormbases': ['app.CalendarEntry']},
            'calendarentry_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['app.CalendarEntry']", 'unique': 'True', 'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'signup': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'time_hole': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'time_playing': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'app.rehearsal': {
            'Meta': {'ordering': "['date']", 'object_name': 'Rehearsal', '_ormbases': ['app.CalendarEntry']},
            'calendarentry_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['app.CalendarEntry']", 'unique': 'True', 'primary_key': 'True'}),
            'fika': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "u'H\\xe5lan'", 'max_length': '128'}),
            'signup': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'time_hole': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(19, 0)'})
        }
    }

    complete_apps = ['app']
