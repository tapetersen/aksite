# coding: utf-8

from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.utils.http import urlquote
from models import Event, Signup
import ak

from django.utils.translation import ugettext_lazy as _
import logging

"""Monkeypatch feincms handler to handle on page.require_login"""

from feincms.views.cbv.views import Handler
from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME
import settings

instancemethod = type(Handler.prepare)
old_prepare = Handler.prepare
def prepare(self):
    bound_prepare = instancemethod(old_prepare, self, Handler)
    
    if self.page.require_permission:
        if not self.request.user.has_perm("page.can_view", self.page):
            return HttpResponseRedirect("%s?%s=%s" % (settings.LOGIN_URL, 
                REDIRECT_FIELD_NAME, urlquote(self.request.get_full_path())))

    if self.page.require_login:
        return login_required(lambda request: bound_prepare())(self.request)
    return bound_prepare()

Handler.prepare = instancemethod(prepare, None, Handler)

class GenericFeinView(Handler):
    extra_context = {}
        
    def get_context_data(self, **kwargs):
        context = super(Handler, self).get_context_data()
        context.update(self.extra_context)
        return context
    
from django import forms
    
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
        
        context['event'] = Event.objects.select_subclasses().get(pk=self.kwargs["event_pk"])        
        return context
    
    def form_valid(self, form):
        form.instance.event = Event.objects.get(pk=self.kwargs["event_pk"])
        form.instance.user = self.request.user
        return super(EventSignup, self).form_valid(form)
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EventSignup, self).dispatch(*args, **kwargs)
    

    
