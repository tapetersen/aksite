#coding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _
from feincms.module.page.models import Page
from feincms.module.page.extensions.navigation import NavigationExtension, \
		PagePretender

# Templates

Page.register_templates({
	'title': _('Main template'),
	'path': '1col.html',
	'regions': (
		('main', _('Main content area')),
		('footer', _('Footer'), 'inherited'),
	),
})

Page.register_templates({
	'title': _('2 column template'),
	'path': '2col.html',
	'regions': (
		('col1', _('Column 1')),
		('col2', _('Column 2')),
		('footer', _('Footer'), 'inherited'),
	),
})

# Content types

from feincms.utils import get_object


Page.create_content_type(
	get_object("feincms.content.richtext.models.RichTextContent"))

from feincms.content.medialibrary.models import MediaFileContent
Page.create_content_type(MediaFileContent, POSITION_CHOICES=(
	('block', _('Block')),
	('left', _('Left')),
	('right', _('Right')),
))

from feincms.content.rss.models import RSSContent
Page.create_content_type(RSSContent)

from feincms.content.table.models import TableContent
Page.create_content_type(TableContent)

from feincms.content.template.models import TemplateContent
Page.create_content_type(TemplateContent)

from feincms.content.video.models import VideoContent
Page.create_content_type(VideoContent)


from feincms.content.application.models import ApplicationContent
Page.create_content_type(ApplicationContent, APPLICATIONS=(
    ("kamerer_urls", "Address Register"),
))

Page.register_extensions('datepublisher', 'navigation', 'titles')

# Models

from ak import instrument_choices, section_choices
import datetime

class Rehearsal(models.Model):
	location = models.CharField(max_length=128, default = u"Hålan")
	date = models.DateField()
	time_hole = models.TimeField(default = datetime.time(19,00), blank=True, null=True)
	time_location = models.TimeField(blank=True, null=True)
	info = models.TextField(blank=True)
	insiderinfo = models.TextField(blank=True)
	signup = models.BooleanField()
	fika = models.CharField(max_length=2, choices=section_choices)

	def __unicode__(self):
		return self.location + u" - " + str(self.date)

class Gig(models.Model):
	name = models.CharField(max_length=128)
	location = models.CharField(max_length=128)
	date = models.DateField()
	time_hole = models.TimeField(blank=True, null=True)
	time_location = models.TimeField(blank=True, null=True)
	time_playing = models.TimeField(blank=True, null=True)
	signup = models.BooleanField()
	insiderinfo = models.TextField(blank=True)
	info = models.TextField(blank=True)
	
	def __unicode__(self):
		return self.name + u" - " + str(self.date)


from django.contrib.auth.models import User
class Kamerer(models.Model):
	user = models.ForeignKey(User, unique=True)

	address = models.CharField(max_length=128)
	zip = models.CharField(max_length=5)
	city = models.CharField(max_length=128)
	phone = models.CharField(max_length=16)
	nation = models.CharField(max_length=128)
	instrument = models.CharField(max_length=2, choices=instrument_choices)

from django.db.models.signals import post_save
from django.dispatch import receiver
@receiver(post_save, sender=User)
def user_modification_handler(sender, instance, created, **kwargs):
	if created:
		Kamerer(user=instance).save()
		

