#coding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _
from feincms.module.page.models import Page
from django.contrib.auth.models import User

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

Page.register_templates({
    'title': _('Special page'),
    'path': 'special.html',
    'regions': (
        ('special', _("Special content")),
    ),
})

Page.register_templates({
    'title': _('Music player'),
    'path': 'music.html',
    'regions': (
        ('albums', _("Albums")),
    ),
})

# Models

from ak import instrument_choices, section_choices
import datetime
from model_utils.managers import InheritanceManager

class Event(models.Model):   
    date = models.DateField(_("date"))
    time_location = models.TimeField(_("time location"), blank=True, null=True)
    info = models.TextField(_("info"), blank=True)
    
    objects = InheritanceManager()
    
    last_modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    name = u"Event"
    
    def get_signup(self, user):
        signup = Signup.objects.filter(user=user, event=self)
        if signup.exists(): return signup[0]
        return None
    
    def num_signed_up(self):
        return Signup.objects.filter(event=self).count()
    
    class Meta:
        ordering = ["date"]
        verbose_name = _("event")
        verbose_name_plural = _('events')
    
    def __unicode__(self):
        return u"%s - %s" % (self.name, self.date)
    
    
class Rehearsal(Event):
    fika = models.CharField(_("fika"), max_length=2, choices=section_choices)
    
    location = models.CharField(_("location"), max_length=128, default=u"Hålan")
    time_hole = models.TimeField(_("time hole"), default=datetime.time(19,00))
    signup = models.BooleanField(_("signup"), default=False)
            
    name = u"Rep"
    
    def isGig(self): return False
    
    def present(self, request):
        columns = ([],[],[])
        columns[0].append()
    
    class Meta:
        verbose_name = _("rehearsal")
        verbose_name_plural = _('rehearsals')


class Gig(Event):
    name = models.CharField(_("name"), max_length=128)
    time_playing = models.TimeField(_("time playing"), blank=True, null=True)
    
    location = models.CharField(_("location"), max_length=128, blank=True, null=True)
    time_hole = models.TimeField(_("time hole"), blank=True, null=True)
    signup = models.BooleanField(_("signup"), default=True)
    
    public_info = models.TextField(_("public info"), blank=True)
    
    secret = models.BooleanField(_("secret"), default=False)
        
        
    def isGig(self): return True
    
    class Meta:
        verbose_name = _("gig")
        verbose_name_plural = _('gigs')

class Signup(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event, editable=False)
    COMING_CHOICES = (
        ("H", u"Kommer till hålan"),
        ("D", u"Kommer direkt"),
        ("I", u"Kan inte komma"),
    )
    coming = models.CharField(_("coming"), max_length=1, choices=COMING_CHOICES, default="H")
    car = models.BooleanField(_("can bring car"))
    comment = models.CharField(_("comment"), max_length=128, blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ("user", "event")
        
        verbose_name = _("signup")
        verbose_name_plural = _('signups')
    
from mailinglists import MailVerificationSent

from feincms.module.medialibrary.models import MediaFile, Category
from feincms.models import create_base_model
class Album(create_base_model()):
    name = models.CharField(_("name"), max_length=128)
    image = models.ForeignKey(MediaFile, 
                              limit_choices_to={"type":"image"},
                              related_name="image")
    description = models.TextField(_("description"), blank=True)
    year = models.IntegerField()
    
    class Meta:
        verbose_name = _("album")
        verbose_name_plural = _('albums')
        
    def __unicode__(self):
        return u"%d - %s" % (self.year, self.name)
    
Album.register_regions(
    ("tunes", _("Tunes")),
)

class Tune(models.Model):
    audio = models.ForeignKey(MediaFile, 
                              limit_choices_to={"type":"audio"})
    
    class Meta:
        abstract = True
        verbose_name = _("tune")
        verbose_name_plural = _('tunes')
        
Album.create_content_type(Tune)

# User

User.__unicode__ = lambda self: u"%s %s" % (self.first_name, self.last_name)
User._meta.fields[2].blank = False # First name
User._meta.fields[3].blank = False # Last name
User._meta.fields[4].blank = False # Email
User.add_to_class("address", models.CharField(_("address"), max_length=128, blank=True, null=True))
User.add_to_class("zip", models.CharField(_("zip"), max_length=5, blank=True, null=True))
User.add_to_class("city", models.CharField(_("city"), max_length=128, blank=True, null=True))
User.add_to_class("phone", models.CharField(_("phone"), max_length=16, blank=True, null=True))
User.add_to_class("second_phone", models.CharField(_("second phone"), max_length=16, blank=True, null=True))
User.add_to_class("nation", models.CharField(_("nation"), max_length=128, blank=True, null=True))
User.add_to_class("instrument", models.CharField(_("instrument"), max_length=2, choices=instrument_choices))
User.add_to_class("has_key", models.BooleanField(_("has key"), default=False))
User.add_to_class("medals_earned", models.IntegerField(_("medals earned"), default=0))
User.add_to_class("medals_awarded", models.IntegerField(_("medals awarded"), default=0))

# Page
Page.add_to_class("require_login", models.BooleanField(_("require login"), default=False))
Page.add_to_class("require_permission", models.BooleanField(_("require permission"), default=False))
Page.add_to_class("only_public", models.BooleanField(_("only public"), default=False))

# Content types
from feincms.utils import get_object
from django.template.loader import render_to_string

common_regions = ("main", "col1", "col2", "footer")

class AlbumContent(models.Model):
    album = models.ForeignKey(Album)
    class Meta:
        abstract = True
        verbose_name = _("album")
        verbose_name_plural = _('albums')
Page.create_content_type(AlbumContent, regions=("albums",))


class AddressRegisterContent(models.Model):
    class Meta:
        abstract = True
        verbose_name = _("address register")
        
    def render(self, **kwargs):
        ctx = dict(kamerers=User.objects.filter(is_active=True).order_by(
                                                        "instrument", 
                                                        "last_name", 
                                                        "first_name"))
        ctx.update(kwargs)
        return render_to_string("address_register.html", ctx)
    
Page.create_content_type(AddressRegisterContent, regions=("special",))

class GigsContent(models.Model):
    class Meta:
        abstract = True
        verbose_name = _("gigs")
        
    def render(self, **kwargs):
        ctx = dict(
            events=Gig.objects.filter(date__gte=datetime.date.today())
        )
        ctx.update(kwargs)
        return render_to_string("gigs.html", ctx)
    
Page.create_content_type(GigsContent, regions=("special",))

class UpcomingContent(models.Model):
    class Meta:
        abstract = True
        verbose_name = _("upcoming")
        
    def render(self, **kwargs):
        ctx = dict(
            events=Event.objects.filter(
                date__gte=datetime.date.today()
            ).select_subclasses()
        )
        ctx.update(kwargs)
        return render_to_string("upcoming.html", ctx)
    
Page.create_content_type(UpcomingContent, regions=("special",))

Page.create_content_type(
    get_object("feincms.content.richtext.models.RichTextContent"),
    regions=common_regions)

from feincms.content.medialibrary.v2 import MediaFileContent
Page.create_content_type(MediaFileContent, TYPE_CHOICES=(
            ('default', _('Default')),
            ('left', _('Left')),
            ('right', _('Right')),
            ('download', _('Download')),
        ),
        regions=common_regions
)

from feincms.content.rss.models import RSSContent
Page.create_content_type(RSSContent, regions=common_regions)

from feincms.content.template.models import TemplateContent
Page.create_content_type(TemplateContent, regions=common_regions)

from feincms.content.video.models import VideoContent
Page.create_content_type(VideoContent, regions=common_regions)


Page.register_extensions('titles')

