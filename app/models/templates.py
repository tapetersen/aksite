from feincms.module.page.models import Page

from django.utils.translation import ugettext_lazy as _

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
