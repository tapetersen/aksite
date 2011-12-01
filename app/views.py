# coding: utf-8

from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from models import Event, Signup
from feincms.module.page.models import Page
from django.contrib.auth.models import User
import datetime

from django.utils.translation import ugettext_lazy as _
import logging

"""Monkeypatch feincms handler to handle on page.require_login"""

from feincms.views.cbv.views import Handler
from django.contrib.auth.decorators import login_required

instancemethod = type(Handler.prepare)
old_prepare = Handler.prepare
def prepare(self):
    bound_prepare = instancemethod(old_prepare, self, Handler)
    
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
    
import django_cal.views
django_cal.views.EVENT_ITEMS += (
    ("X-ALT-DESC;FMTTYPE=text/html", "item_html_description"),
)
from django_cal.views import Events
import re
import models
from django.http import HttpResponse, Http404

class CalEvents(Events):
    def __call__(self, request, *args, **kwargs):
        """ Makes Events callable for easy use in your urls.py """
        try:
            obj = self.get_object(request, *args, **kwargs)
        except ObjectDoesNotExist:
            raise Http404('Events object does not exist.')
        ical = self.get_ical(obj, request)
        
        cal_timezone = self._Events__get_dynamic_attr("cal_timezone", obj)
        if cal_timezone:
            ical.add('x-wr-timezone').value = cal_timezone
        
        response = HttpResponse(ical.serialize(), mimetype='text/calendar; charset=utf-8')
        filename = self._Events__get_dynamic_attr('filename', obj)
        # following added for IE, see
        # http://blog.thescoop.org/archives/2007/07/31/django-ical-and-vobject/
        response['Filename'] = filename
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        response["Cache-Control"] = "no-cache, must-revalidate";
        response["Expires"] = "Sat, 26 Jul 1997 05:00:00 GMT";
        return response
    
    def items(self):
        return models.Event.objects.filter(
            date__gte=datetime.date.today() - datetime.timedelta(days=30)
        ).select_subclasses()
        
    def cal_timezone(self):
        return "Europe/Stockholm"

    def cal_name(self):
        return "AKcal"

    def cal_desc(self):
        return "Alte Kamererens eventkalender"
    
    def item_summary(self, item):
        return item.name

    def item_html_description(self, item):
        html = u""
        if item.time_hole is not None:
            html += u"<p>Hålan: %s</p>" % item.time_hole
        if item.time_location is not None:
            html += u"<p>Där: %s</p>" % item.time_location
        if hasattr(item, "time_playing") and item.time_playing is not None:
            html += u"<p>Spelning börjar: %s</p>" % item.time_playing
        return html + item.info
    
    def item_description(self, item):
        desc = self.item_html_description(item)
        desc = desc.replace("</p", "\n</p")
        desc = desc.replace("</br", "\n</br")
        return re.sub(r"\<[^\>]*\>", "", desc)

    def item_start(self, item):
        time = item.time_hole
        if time is None:
            time = item.time_location
        if time is None and hasattr(item, "time_playing"):
            time = item.time_playing
        if time is None:
            time = datetime.time(12, 00)
            
        return datetime.datetime.combine(item.date, time)

    def item_duration(self, item):
        return datetime.timedelta(hours=2)
    
    def item_location(self, item):
        return item.location
    
    def item_last_modified(self, item):
        return item.last_modified
    
    def item_created(self, item):
        return item.created
    
    def item_uid(self, item):
        return "event-%d@altekamereren.org" % item.pk
    
    
