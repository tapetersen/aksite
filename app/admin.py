from django.contrib import admin

from models import Rehearsal, Gig

from django.utils.translation import ugettext_lazy as _

class RehearsalAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('location', 'date', 
            "time_hole", "time_location", "signup", "fika",
            "info", "insiderinfo")} ),
    )
    list_display = ('location', "date", "fika")
    
admin.site.register(Rehearsal, RehearsalAdmin)
    
class GigAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'location', 'date', 
            "time_hole", "time_location", "time_playing", "signup",
            "info", "insiderinfo")} ),
    )
    list_display = ('name', 'location', "date")
    
admin.site.register(Gig, GigAdmin)

# User admin

from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 
                  "address", "zip", "city", "phone", "second_phone", "nation", "instrument",
                  'is_active', 'is_staff', 'is_superuser')

class CustomUserAdmin(UserAdmin):
    fieldsets = None
    form = UserForm
    search_fields = ()
    list_display = ('first_name', 'last_name', "instrument")
    list_display_links = ('first_name', 'last_name')
    list_filter = ('instrument',)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Page admin

from feincms.module.page.models import Page, PageAdmin
PageAdmin.unknown_fields.remove("require_login")
PageAdmin.fieldsets[0][1]["fields"].insert(2, "require_login")

from feincms.admin import editor
PageAdmin.require_login_toggle = editor.ajax_editable_boolean('require_login', _('require login'))
PageAdmin.list_display.insert(3, "require_login_toggle")
PageAdmin.list_filter.insert(2, "require_login")

#admin.site.unregister(Page)
#admin.site.register(Page, PageAdmin)
