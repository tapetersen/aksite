from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from feincms.views.generic.simple import direct_to_template

from django.views.generic import edit
from django.contrib import auth

import feincms
import settings, os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from app import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^(favicon.ico)\/?$', 'django.views.static.serve', {
            'document_root': settings.STATICFILES_DIRS[0],
    }),
    
    url(r"^upcoming/$", views.Upcoming.as_view()),
    
    url(r"^members/$", views.AddressRegister.as_view()),
    
    url(r'^users/', include('registration.backends.simple.urls')),
    
    url(r"^mailsender/$", views.mailsender),
    
    (r'^sentry/', include('sentry.web.urls')),
    
    url(r'^users/login/$', 'django.contrib.auth.views.login'),
    url(r'^users/logout/$', 'django.contrib.auth.views.logout'),
    url(r'^users/profile/$', lambda request: edit.UpdateView.as_view(
         model=auth.models.User, form_class=views.UserForm,
         success_url="/users/profile/")(
         request, pk=request.user.pk)),

    url(r'', include('feincms.urls')),
)
# media served if DEBUG = True
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

