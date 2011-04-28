from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static

import feincms
import settings, os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^(favicon.ico)\/?$', 'django.views.static.serve', {
            'document_root': settings.STATICFILES_DIRS[0],
    }),

    url(r'', include('feincms.urls')),
)
# media served if DEBUG = True
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

