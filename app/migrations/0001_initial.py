# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table(u'app_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('time_location', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('app', ['Event'])

        # Adding model 'Rehearsal'
        db.create_table(u'app_rehearsal', (
            (u'event_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['app.Event'], unique=True, primary_key=True)),
            ('fika', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('location', self.gf('django.db.models.fields.CharField')(default=u'H\xe5lan', max_length=128)),
            ('time_hole', self.gf('django.db.models.fields.TimeField')(default=datetime.time(19, 0))),
            ('signup', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('app', ['Rehearsal'])

        # Adding model 'Gig'
        db.create_table(u'app_gig', (
            (u'event_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['app.Event'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('time_playing', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('time_hole', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('signup', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('public_info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('secret', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('app', ['Gig'])

        # Adding model 'Signup'
        db.create_table(u'app_signup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Event'])),
            ('coming', self.gf('django.db.models.fields.CharField')(default='H', max_length=1)),
            ('car', self.gf('django.db.models.fields.BooleanField')()),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('app', ['Signup'])

        # Adding unique constraint on 'Signup', fields ['user', 'event']
        db.create_unique(u'app_signup', ['user_id', 'event_id'])

        # Adding model 'Album'
        db.create_table(u'app_album', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(related_name='image', to=orm['medialibrary.MediaFile'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('app', ['Album'])

        # Adding model 'Tune'
        db.create_table(u'app_album_tune', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('audio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['medialibrary.MediaFile'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tune_set', to=orm['app.Album'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('app', ['Tune'])

        # Adding model 'MailVerificationSent'
        db.create_table(u'app_mailverificationsent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('sent', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'app', ['MailVerificationSent'])


    def backwards(self, orm):
        # Removing unique constraint on 'Signup', fields ['user', 'event']
        db.delete_unique(u'app_signup', ['user_id', 'event_id'])

        # Deleting model 'Event'
        db.delete_table(u'app_event')

        # Deleting model 'Rehearsal'
        db.delete_table(u'app_rehearsal')

        # Deleting model 'Gig'
        db.delete_table(u'app_gig')

        # Deleting model 'Signup'
        db.delete_table(u'app_signup')

        # Deleting model 'Album'
        db.delete_table(u'app_album')

        # Deleting model 'Tune'
        db.delete_table(u'app_album_tune')

        # Deleting model 'MailVerificationSent'
        db.delete_table(u'app_mailverificationsent')


    models = {
        'app.album': {
            'Meta': {'object_name': 'Album'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'image'", 'to': u"orm['medialibrary.MediaFile']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'app.event': {
            'Meta': {'ordering': "['date']", 'object_name': 'Event'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'time_location': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'app.gig': {
            'Meta': {'ordering': "['date']", 'object_name': 'Gig', '_ormbases': ['app.Event']},
            u'event_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['app.Event']", 'unique': 'True', 'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'public_info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'secret': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'signup': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'time_hole': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'time_playing': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'app.mailverificationsent': {
            'Meta': {'object_name': 'MailVerificationSent'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sent': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'app.rehearsal': {
            'Meta': {'ordering': "['date']", 'object_name': 'Rehearsal', '_ormbases': ['app.Event']},
            u'event_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['app.Event']", 'unique': 'True', 'primary_key': 'True'}),
            'fika': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "u'H\\xe5lan'", 'max_length': '128'}),
            'signup': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'time_hole': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(19, 0)'})
        },
        'app.signup': {
            'Meta': {'unique_together': "(('user', 'event'),)", 'object_name': 'Signup'},
            'car': ('django.db.models.fields.BooleanField', [], {}),
            'coming': ('django.db.models.fields.CharField', [], {'default': "'H'", 'max_length': '1'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'app.tune': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'Tune', 'db_table': "u'app_album_tune'"},
            'audio': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['medialibrary.MediaFile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tune_set'", 'to': "orm['app.Album']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            'has_key': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrument': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'medals_awarded': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'medals_earned': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nation': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'second_phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'medialibrary.category': {
            'Meta': {'ordering': "['parent__title', 'title']", 'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['medialibrary.Category']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'medialibrary.mediafile': {
            'Meta': {'ordering': "['-created']", 'object_name': 'MediaFile'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['medialibrary.Category']", 'null': 'True', 'blank': 'True'}),
            'copyright': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            'file_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        }
    }

    complete_apps = ['app']