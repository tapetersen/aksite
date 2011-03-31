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
