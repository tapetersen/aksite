#coding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _
from feincms.module.page.models import Page
from django.template.loader import render_to_string

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

# Models

from ak import instrument_choices, section_choices
import datetime
from model_utils.managers import InheritanceManager

class CalendarEntry(models.Model):
    location = models.CharField(max_length=128, blank=True, null=True)
    date = models.DateField()
    time_hole = models.TimeField(blank=True, null=True)
    time_location = models.TimeField(blank=True, null=True)
    signup = models.BooleanField(default=True)
    insiderinfo = models.TextField(blank=True)
    info = models.TextField(blank=True)
    
    objects = InheritanceManager()
    
    class Meta:
        ordering = ["date"]
        app_label = "aksite"
    
    def __unicode__(self):
        return self.location + u" - " + str(self.date)
    
class Rehearsal(CalendarEntry):
    fika = models.CharField(max_length=2, choices=section_choices)
    
    class Meta:
        app_label = "aksite"
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('location', u"Hålan")
        kwargs.setdefault('time_hole', datetime.time(19,00))
        kwargs.setdefault('signup', False)
        super(Rehearsal, self).__init__(*args, **kwargs)
        
    def isGig(self): return False

class Gig(CalendarEntry):
    name = models.CharField(max_length=128)
    time_playing = models.TimeField(blank=True, null=True)
    
    class Meta:
        app_label = "aksite"
    
    def __unicode__(self):
        return self.name + u" - " + str(self.date)
        
    def isGig(self): return True

from django.contrib.auth.models import User
class Kamerer(models.Model):
    user = models.ForeignKey(User, unique=True)

    address = models.CharField(max_length=128)
    zip = models.CharField(max_length=5)
    city = models.CharField(max_length=128)
    phone = models.CharField(max_length=16)
    second_phone = models.CharField(max_length=16, blank=True, null=True)
    nation = models.CharField(max_length=128, blank=True, null=True)
    instrument = models.CharField(max_length=2, choices=instrument_choices)
    
    class Meta:
        app_label = "aksite"

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

@Page.create_content_type
class AddressRegister(models.Model):
    class Meta:
        abstract = True
        app_label = "aksite"

    def render(self, **kwargs):
        return render_to_string('content/address_register.html', {
            'kamerers': Kamerer.objects.all().order_by("instrument", 
                                                       "user__last_name", 
                                                       "user__first_name"),
        })

Page.register_extensions('datepublisher', 'titles')

