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
        
        context['event'] = Event.objects.select_subclasses().get(pk=self.kwargs["event_pk"])        
        return context
    
    def form_valid(self, form):
        form.instance.event = Event.objects.get(pk=self.kwargs["event_pk"])
        form.instance.user = self.request.user
        return super(EventSignup, self).form_valid(form)
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EventSignup, self).dispatch(*args, **kwargs)
    

    
