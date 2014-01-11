from django.conf.urls import patterns, include
from django.conf.urls.static import static

from django.views.generic.edit import UpdateView
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from feincms.module.page.sitemap import PageSitemap
from feincms.module.page.models import Page

import settings

from app import models

from django.contrib import admin
admin.autodiscover()

from app import views, mailinglists, forms, ical

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/', include(admin.site.urls)),

    (r'^(favicon\.ico|robots\.txt|apple-touch-icon\.png)\/?$', 
        'django.views.static.serve', {
            'document_root': settings.STATICFILES_DIRS[0],
    }),
    
    (r"^mailsender/$", mailinglists.mailsender),
                       
    (r"^ical(.php|.ics)?/$", ical.CalEvents()),
    
    (r'^users/login/$', 'django.contrib.auth.views.login', 
        dict(authentication_form=forms.LoginForm)),
    (r'^users/logout/$', login_required(auth.views.logout)),
    (r'^users/profile/$', views.is_active_required(
        lambda request: UpdateView.as_view(
            model=auth.models.User, form_class=forms.UserForm,
            success_url="/users/profile/")
        (request, pk=request.user.pk))),
                       
    (r'^event/signup/(?P<event_pk>\d+)$', views.is_active_required(
        views.EventSignup.as_view(success_url="/upcoming/"))),

    #(r'^sentry/', include('sentry.web.urls')),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', 
        {'sitemaps': {'pages': PageSitemap(
            queryset=Page.objects.filter(require_login=False,
                                         require_permission=False))}}),
    
    (r'', include('feincms.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

