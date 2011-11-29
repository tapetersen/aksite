from django import forms
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _
import logging

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

