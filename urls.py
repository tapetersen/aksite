from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static

from django.views.generic.edit import UpdateView, CreateView
from django.contrib import auth
from django.contrib.auth.decorators import login_required

import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from app import views, mailinglists, forms, models
import datetime


urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^(favicon\.ico|robots\.txt|apple-touch-icon\.png)\/?$', 
        'django.views.static.serve', {
            'document_root': settings.STATICFILES_DIRS[0],
    }),
    
    (r"^mailsender/$", mailinglists.mailsender),
    
    (r"^upcoming/$", views.FeinListView.as_view(
        context_object_name="events",
        template_name = "upcoming.html",
        queryset = models.Event.objects.filter(
            date__gte=datetime.date.today()).select_subclasses())),
                       
    (r"^gigs/$", views.FeinListView.as_view(
        context_object_name="events",
        template_name = "gigs.html",
        queryset = models.Gig.objects.filter(
            date__gte=datetime.date.today()))),
                       
    (r"^members/$", views.FeinListView.as_view(
        context_object_name="kamerers",
        template_name = "address_register.html",
        queryset = models.User.objects.all().order_by("instrument", 
                                                      "last_name", 
                                                      "first_name"))),
    
    (r'^users/', include('registration.backends.simple.urls')),
    (r'^users/login/$', 'django.contrib.auth.views.login'),
    (r'^users/logout/$', login_required('django.contrib.auth.views.logout')),
    (r'^users/profile/$', login_required(lambda request: UpdateView.as_view(
         model=auth.models.User, form_class=forms.UserForm,
         success_url="/users/profile/")(
         request, pk=request.user.pk))),
                       
    (r'^event/signup/(?P<event_pk>\d+)$', login_required(views.EventSignup.as_view(
         success_url="/upcoming/"))),

    (r'^sentry/', include('sentry.web.urls')),
    
    (r'', include('feincms.urls')),
)
# media served if DEBUG = True
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

