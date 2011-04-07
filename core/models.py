#coding: utf-8

from django.db import models
from feincms.content.medialibrary.models import MediaFileContent

# Create your models here.

from django.utils.translation import ugettext_lazy as _

from feincms.module.page.models import Page
from feincms.content.richtext.models import RichTextContent
from feincms.content.image.models import ImageContent

Page.register_extensions('datepublisher', 'navigation', 'titles') # Example set of

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

Page.create_content_type(RichTextContent)
Page.create_content_type(MediaFileContent, POSITION_CHOICES=(
	('block', _('Block')),
	('left', _('Left')),
	('right', _('Right')),
))

sections = (
	u"flöjt",
	u"klarinett",
	u"saxofon",
	u"trumpet",
	u"trombon",
	u"komp",
	u"balett"
)
section_choices = [(s[0]+s[-1], s) for s in sections]

instruments = {
	u"flöjt":u"flöjt",
	u"klarinett":u"klarinett",
	u"altsax":u"saxofon",
	u"tenorsax":u"saxofon",
	u"barytonsax":u"saxofon",
	u"trumpet":u"trumpet",
	u"trombon":u"trombon",
	u"tuba":u"komp",
	u"banjo":u"komp",
	u"slagverk":u"komp",
	u"euphonium":u"komp",
	u"horn":u"komp",
	u"balett":u"balett"
}
instrument_choices = [(i[0]+i[-1], i) for i in instruments.keys()]

import datetime

class Repetition(models.Model):
	location = models.CharField(max_length=128, default = u"Hålan")
	date = models.DateField()
	time_hole = models.TimeField(default = datetime.time(19,00), blank=True, null=True)
	time_location = models.TimeField(blank=True, null=True)
	info = models.TextField(blank=True)
	insiderinfo = models.TextField(blank=True)
	signup = models.BooleanField()
	fika = models.CharField(max_length=2, choices=section_choices)

	def __unicode__(self):
		return self.name

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
		return self.name

from django.contrib.auth.models import User
class Kamerer(models.Model):
	user = models.ForeignKey(User, unique=True)
	
	address = models.CharField(max_length=128)
	
from django.db.models.signals import post_save
from django.dispatch import receiver
@receiver(post_save, sender=User)
def user_modification_handler(sender, instance, created, **kwargs):
	if created:
		Kamerer(user=instance).save()