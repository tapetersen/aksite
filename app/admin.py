from django.contrib import admin
from django.db import models

from models import Rehearsal, Gig
from widgets import RichEditor

from django.utils.translation import ugettext_lazy as _

class RehearsalAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('location', 'date', 
            "time_hole", "time_location", "signup", "fika",
            "info")} ),
    )
    list_display = ('location', "date", "fika")
    formfield_overrides = {
        models.TextField: {'widget': RichEditor},
    }
    
admin.site.register(Rehearsal, RehearsalAdmin)
    
class GigAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'location', 'date', 
            "time_hole", "time_location", "time_playing", "signup",
            "info", "public_info")} ),
    )
    list_display = ('name', 'location', "date")
    formfield_overrides = {
        models.TextField: {'widget': RichEditor},
    }
    
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
PageAdmin.fieldsets[0][1]["fields"][1] += ("require_login",)

from feincms.admin import tree_editor
PageAdmin.list_display.insert(3, tree_editor.ajax_editable_boolean('require_login', _('require login')))
PageAdmin.list_filter.insert(2, "require_login")

#admin.site.unregister(Page)
#admin.site.register(Page, PageAdmin)
