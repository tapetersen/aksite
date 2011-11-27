from django.views.generic import ListView
from models import CalendarEntry
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

class FeinListView(ListView):
    def get_context_data(self, **kwargs):
        """Adds feincms_page to context to get working navigation on special views."""
        
        context = super(FeinListView, self).get_context_data(**kwargs)
        context['feincms_page'] = Page.objects.for_request(self.request, best_match=True)
        
        return context
    
    def dispatch(self, request, *args, **kwargs):
        """Bolt on login_required"""        
        page = Page.objects.for_request(request, best_match=True)
        f = super(ListView, self).dispatch
        if page.require_login:
            return login_required(f)(request, *args, **kwargs)
        return f(request, *args, **kwargs)

class Upcoming(FeinListView):
    context_object_name = "entry_list"
    template_name = "upcoming.html"
    queryset = CalendarEntry.objects.filter(date__gte=datetime.date.today()).select_subclasses()
    
        
class AddressRegister(FeinListView):
    context_object_name = "kamerers"
    template_name = "address_register.html"
    queryset = User.objects.all().order_by("instrument", 
                                           "last_name", 
                                           "first_name")
    


def mailsender(request):
    logging.info("mailsender %s", str(request.FILES))
    
from django import forms
class UserForm(forms.ModelForm):
    password_old = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                label=_("Current password"), required=False)
    password_new1 = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                label=_("New password"), required=False)
    password_new2 = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                label=_("New password (again)"), required=False)
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", 
                  "password_old", "password_new1", "password_new2",
                  "address", "zip", "city", "phone", "second_phone", "nation", 
                  "instrument")
        
    def clean(self):
        if 'password_new1' in self.cleaned_data and self.cleaned_data["password_new1"]:
            
            if 'password_old' not in self.cleaned_data or not self.cleaned_data["password_old"]:
                self._errors["password_old"] = \
                    self.error_class([u"Missing current password."])
                    
            elif not self.instance.check_password(self.cleaned_data["password_old"]):
                self._errors["password_old"] = \
                    self.error_class([u"Incorrect password."])
                    
            elif "password_new2" not in self.cleaned_data or not self.cleaned_data["password_new2"]:
                self._errors["password_new2"] = \
                    self.error_class([u"Missing password comfirmation."])
                    
            elif self.cleaned_data['password_new1'] != self.cleaned_data['password_new2']:
                self._errors["password_new1"] = \
                    self.error_class([u"The two password fields didn't match."])
                self._errors["password_new2"] = \
                    self.error_class([u"The two password fields didn't match."])
            else:
                self.instance.set_password(self.cleaned_data['password_new1'])
                    
        elif 'password_new2' in self.cleaned_data and self.cleaned_data["password_new2"]:
            self._errors["password_new1"] = \
                self.error_class([u"Missing password comfirmation."])
            
                
        if 'password_new1' in self.cleaned_data: del self.cleaned_data["password_new1"]
        if 'password_new2' in self.cleaned_data: del self.cleaned_data["password_new2"]
        if 'password_old'  in self.cleaned_data: del self.cleaned_data["password_old"]
        
        return self.cleaned_data













