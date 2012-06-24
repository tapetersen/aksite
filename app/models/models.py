#coding: utf-8
import datetime, os

from django.db import models
from django.contrib.auth.models import User
from model_utils.managers import InheritanceManager
from django.utils.translation import ugettext_lazy as _

from event import Event

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


def MediaFile__unicode__(self):
    return os.path.basename(self.file.name)
MediaFile.__unicode__ = MediaFile__unicode__
