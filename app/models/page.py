from feincms.module.page.models import Page
from models import Album
from event import *
from user import User
from django.db import models
import datetime

from django.utils.translation import ugettext_lazy as _

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

        ctx = {'events': get_upcoming_events(kwargs['user'])}
        ctx.update(kwargs)
        return render_to_string("upcoming.html", ctx)
    
Page.create_content_type(UpcomingContent, regions=("special",))

Page.create_content_type(
    get_object("feincms.content.richtext.models.RichTextContent"),
    regions=common_regions)

from feincms.content.medialibrary.models import MediaFileContent
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


Page.register_extensions('feincms.module.page.extensions.titles')
