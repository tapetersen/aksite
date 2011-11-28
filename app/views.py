# endcoding: utf8

from django.views.generic import ListView
from models import CalendarEntry, MailVerificationSent
from feincms.module.page.models import Page
from django.contrib.auth.models import User
import datetime
import ak

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
    

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def mailsender(request):
    from django.http import HttpResponse
    
    mail = request.FILES[u"file"].read()
    to = request.GET["to"]
    
    i = mail.find("\n\n")
    headers, mail = mail[:i], mail[i:]
    headers = headers.split("\n")
    allowed = {"MIME-Version", "Message-ID", "In-Reply-To", "Content-Type", 
               "Date", "Subject", "From", "To", "Bcc", "Cc", "References"}
    
    from_ = None
    
    h = []
    i=0
    while i<len(headers):
        add = False
        print i
        header = headers[i][:headers[i].find(":")]
        if header in allowed:
            add = True
        if header == "From":
            from_ = headers[i][headers[i].find(":")+1:].strip()
            
        while True:
            if add: 
                h.append(headers[i])
            i += 1
            if i>=len(headers) or headers[i][0] not in " \t":
                break
            
    mail = "\n".join(h) + mail
    
    i = from_.find("<")
    if i != -1:
        from_ = from_[i+1:]
        from_ = from_[:from_.find(">")]
    
    #logging.info("headers: %s", str(headers))
    #logging.info("h: %s", str(h))
    
    logging.info("Mail from %s to %s recieved", from_, to)
    if not from_.endswith("@altekamereren.org") \
            and not from_.endswith("@altekamereren.com") \
            and User.objects.filter(email=from_).count() < 1:
        logging.info("Sender not accepted.")
        return HttpResponse(status=400)
    
    if to == u"flojt":
        to = u"flöjt"
    
    if to in ak.sections:
        d = {instrument:str(short) for short, instrument in ak.instrument_choices}
        to = [user.email for user in User.objects.filter(instrument__in=[
            d[k] for k in ak.instruments if ak.instruments[k] == to], 
                                                         is_active=True)]
        
        logging.info("Sending to section: %s", str(to))
    elif to == u"infolistan":
        to = [user.email for user in User.objects.filter(is_active=True)]
        logging.info("Sending to infolistan: %s", str(to))
    else:
        logging.info("List not accepted.")
        return HttpResponse(status=400)
    
    from django.conf import settings
    from boto.ses import SESConnection
    from boto.exception import BotoServerError
    
    access_key_id = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
    access_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)
    api_endpoint = getattr(settings, 'AWS_SES_API_HOST',
                                     SESConnection.DefaultHost)
    connection = SESConnection(
                aws_access_key_id=access_key_id,
                aws_secret_access_key=access_key,
                host=api_endpoint,
    )
    
    try:
        connection.send_raw_email(mail, "sam@bostream.nu", to)
    except BotoServerError as e:
        i = e.body.find("<Message>")
        message = e.body[i+len("<Message>"):]
        message = message[:message.find("</Message>")]
        
        if message == "Email address is not verified.":
            if MailVerificationSent.objects.filter(email=from_, 
                    sent__gte=datetime.datetime.now() - datetime.timedelta(days=1)
                        ).count() < 1:
                connection.verify_email_address(from_)
                logging.error("Sending verify mail to: %s", from_)
                MailVerificationSent(email=from_).save()
            else:
                logging.error("Verify mail already sent today: %s", from_)
            return HttpResponse(status=444)
        else:
            raise
    
    return HttpResponse()
    
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













