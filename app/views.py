# coding: utf-8

from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.utils.http import urlquote
from models import Event, Signup
import ak
import settings

from django.utils.translation import ugettext_lazy as _
import logging


from feincms.module.page.models import Page
from django.contrib.auth import REDIRECT_FIELD_NAME
def require_login_processor(page, request):
    if ((page.require_permission and not request.user.has_perm("page.can_view",
                                                              page))
    or (page.require_login and not request.user.is_authenticated())):
        return HttpResponseRedirect("%s?%s=%s" % (settings.LOGIN_URL, 
            REDIRECT_FIELD_NAME, urlquote(request.get_full_path())))
    else:
        return None

Page.register_request_processors(require_login_processor)

CONTENT_TYPES = ('text/html','application/xhtml+xml','application/xml')
HEADER_VALUE = getattr(settings, 'X_UA_COMPATIBLE', 'IE=edge,chrome=1')

def set_XUACompatible_processor(page, request, response):
    response_ct = response.get('Content-Type','').split(';', 1)[0].lower()
    if response_ct in CONTENT_TYPES:
        if not 'X-UA-Compatible' in response:
            response['X-UA-Compatible'] = HEADER_VALUE
    return response

Page.register_response_processors(set_XUACompatible_processor)

from feincms.views.cbv.views import Handler
class GenericFeinView(Handler):
    extra_context = {}
        
    def get_context_data(self, **kwargs):
        context = super(Handler, self).get_context_data()
        context.update(self.extra_context)
        return context
    
from django import forms
from django.contrib.auth.decorators import login_required
    
class EventSignup(UpdateView):
    model = Signup
    
    class form_class(forms.ModelForm):
        class Meta:
            model = Signup
            fields = ("coming", "car", "comment")
            widgets = { 'coming': forms.RadioSelect }

    def get_object(self):
        signup = Signup.objects.filter(user=self.request.user, event=self.kwargs["event_pk"]) 
        return signup[0] if signup.exists() else None
    
    def get_context_data(self, **kwargs):
        context = super(EventSignup, self).get_context_data(**kwargs)
        
        event = Event.objects.select_subclasses().get(pk=self.kwargs["event_pk"])        
        context['event'] = event
        context['coming'] = event.signup_set.filter(coming__in=[Signup.HOLE,
                                                                Signup.DIRECT])
        context['not_coming'] = event.signup_set.filter(coming=Signup.NOT_COMING)
        return context
    
    def form_valid(self, form):
        form.instance.event = Event.objects.get(pk=self.kwargs["event_pk"])
        form.instance.user = self.request.user
        return super(EventSignup, self).form_valid(form)
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EventSignup, self).dispatch(*args, **kwargs)
    
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test, login_required
def is_active_required(function):
    actual_decorator = user_passes_test(
        lambda u: u.is_active,
        login_url=None,
        redirect_field_name=REDIRECT_FIELD_NAME
    )
    return login_required(actual_decorator(function))
    

    
