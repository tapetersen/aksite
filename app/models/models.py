#coding: utf-8
from django.db import models
from django.contrib.auth.models import User
import datetime

from model_utils.managers import InheritanceManager
from ..ak import section_choices

from django.utils.translation import ugettext_lazy as _

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
        app_label = "app"
    
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
        app_label = "app"


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
        app_label = "app"

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
        app_label = "app"
    
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
        app_label = "app"
        
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
