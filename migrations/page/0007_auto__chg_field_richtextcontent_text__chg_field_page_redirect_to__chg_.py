# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'RichTextContent.text'
        db.alter_column(u'page_page_richtextcontent', 'text', self.gf('feincms.contrib.richtext.RichTextField')())

        # Changing field 'Page.redirect_to'
        db.alter_column(u'page_page', 'redirect_to', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Page.override_url'
        db.alter_column(u'page_page', 'override_url', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Page._cached_url'
        db.alter_column(u'page_page', '_cached_url', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Page._page_title'
        db.alter_column(u'page_page', '_page_title', self.gf('django.db.models.fields.CharField')(max_length=69))

    def backwards(self, orm):

        # Changing field 'RichTextContent.text'
        db.alter_column(u'page_page_richtextcontent', 'text', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Page.redirect_to'
        db.alter_column(u'page_page', 'redirect_to', self.gf('django.db.models.fields.CharField')(max_length=300))

        # Changing field 'Page.override_url'
        db.alter_column(u'page_page', 'override_url', self.gf('django.db.models.fields.CharField')(max_length=300))

        # Changing field 'Page._cached_url'
        db.alter_column(u'page_page', '_cached_url', self.gf('django.db.models.fields.CharField')(max_length=300))

        # Changing field 'Page._page_title'
        db.alter_column(u'page_page', '_page_title', self.gf('django.db.models.fields.CharField')(max_length=100))

    models = {
        'app.album': {
            'Meta': {'object_name': 'Album'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'image'", 'to': u"orm['medialibrary.MediaFile']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
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
        },
        u'page.addressregistercontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'AddressRegisterContent', 'db_table': "u'page_page_addressregistercontent'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'addressregistercontent_set'", 'to': u"orm['page.Page']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'page.albumcontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'AlbumContent', 'db_table': "u'page_page_albumcontent'"},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app.Album']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'albumcontent_set'", 'to': u"orm['page.Page']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'page.gigscontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'GigsContent', 'db_table': "u'page_page_gigscontent'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gigscontent_set'", 'to': u"orm['page.Page']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'page.mediafilecontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'MediaFileContent', 'db_table': "u'page_page_mediafilecontent'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mediafile': ('feincms.module.medialibrary.fields.MediaFileForeignKey', [], {'related_name': "'+'", 'to': u"orm['medialibrary.MediaFile']"}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mediafilecontent_set'", 'to': u"orm['page.Page']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '20'})
        },
        u'page.page': {
            'Meta': {'ordering': "['tree_id', 'lft']", 'object_name': 'Page'},
            '_cached_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'db_index': 'True', 'blank': 'True'}),
            '_content_title': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            '_page_title': ('django.db.models.fields.CharField', [], {'max_length': '69', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_navigation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'only_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'override_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['page.Page']"}),
            'redirect_to': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'require_login': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'require_permission': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'template_key': ('django.db.models.fields.CharField', [], {'default': "'1col.html'", 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'page.richtextcontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'RichTextContent', 'db_table': "u'page_page_richtextcontent'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'richtextcontent_set'", 'to': u"orm['page.Page']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('feincms.contrib.richtext.RichTextField', [], {'blank': 'True'})
        },
        u'page.rsscontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'RSSContent', 'db_table': "u'page_page_rsscontent'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'max_items': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rsscontent_set'", 'to': u"orm['page.Page']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rendered_content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'page.templatecontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'TemplateContent', 'db_table': "u'page_page_templatecontent'"},
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'templatecontent_set'", 'to': u"orm['page.Page']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'page.upcomingcontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'UpcomingContent', 'db_table': "u'page_page_upcomingcontent'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'upcomingcontent_set'", 'to': u"orm['page.Page']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'page.videocontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'VideoContent', 'db_table': "u'page_page_videocontent'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'videocontent_set'", 'to': u"orm['page.Page']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'video': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['page']