from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from models import Event, Signup
from feincms.module.page.models import Page
from django.contrib.auth.models import User
import datetime

from django.utils.translation import ugettext_lazy as _
import logging

"""Bolt on login_required to feincms pages"""

from feincms.views.base import Handler
from django.contrib.auth.decorators import login_required

instancemethod = type(Handler.build_response)
old_build_response = Handler.build_response
def build_response(self, request, page):
    bound_build_response = instancemethod(old_build_response, self, Handler)
    if page.require_login:
        return login_required(bound_build_response)(request, page)
    return bound_build_response(request, page)
Handler.build_response = instancemethod(build_response, None, Handler)

class FeinViewMixin(object):
    def get_context_data(self, **kwargs):
        """Adds feincms_page to context to get working navigation on special views."""
        
        context = super(FeinViewMixin, self).get_context_data(**kwargs)
        context['feincms_page'] = Page.objects.for_request(self.request, best_match=True)
        
        return context
    
    def dispatch(self, request, *args, **kwargs):
        """Bolt on login_required"""        
        page = Page.objects.for_request(request, best_match=True)
        if page.require_login:
            return login_required(super(FeinViewMixin, self).dispatch)(request, *args, **kwargs)
        return super(FeinViewMixin, self).dispatch(request, *args, **kwargs)

class Upcoming(FeinViewMixin, ListView):
    context_object_name = "events"
    template_name = "upcoming.html"
    queryset = Event.objects.filter(date__gte=datetime.date.today()).select_subclasses()    
        
class AddressRegister(FeinViewMixin, ListView):
    context_object_name = "kamerers"
    template_name = "address_register.html"
    queryset = User.objects.all().order_by("instrument", 
                                           "last_name", 
                                           "first_name")
    
from django import forms
    
class EventSignup(UpdateView):
    model = Signup
    
    class form_class(forms.ModelForm):
        class Meta:
            model = Signup
            widgets = { 'coming': forms.RadioSelect }

    def get_object(self):
        signup = Signup.objects.filter(user=self.request.user, event=self.kwargs["event_pk"]) 
        return signup[0] if signup.exists() else None
    
    def get_context_data(self, **kwargs):
        context = super(EventSignup, self).get_context_data(**kwargs)
        
        context['event'] = Event.objects.select_subclasses().get(pk=self.kwargs["event_pk"])
        
        return context
    
    def form_valid(self, form):
        form.instance.event = Event.objects.get(pk=self.kwargs["event_pk"])
        form.instance.user = self.request.user
        return super(EventSignup, self).form_valid(form)
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EventSignup, self).dispatch(*args, **kwargs)
    


