from django.contrib import admin
from django.db import models

from app.models import Album, Signup, Rehearsal, Event, Gig

from widgets import RichEditor
from util import DefaultListFilter

import datetime

from django.utils.translation import ugettext_lazy as _


class FutureEventFilter(DefaultListFilter):
    title = _('when')
    parameter_name = 'when'
    default = "future"
    
    def lookups(self, request, model_admin):
        return (
            ("all", _("All")),
            ("future", _("In the future")),
            ("past", _("In the past")),
        )
        
    def queryset(self, request, queryset):
        if self.value() == "future":
            return queryset.filter(date__gte=datetime.date.today())
        elif self.value() == "past":
            return queryset.filter(date__lt=datetime.date.today())

class SignupInline(admin.TabularInline):
    model = Signup
    extra = 0
    
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
    inlines = [
        SignupInline,
    ]
    list_filter = (FutureEventFilter,)
    
    
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
    inlines = [
        SignupInline,
    ]
    list_filter = (FutureEventFilter,)
    
admin.site.register(Gig, GigAdmin)

class EventListFilter(admin.SimpleListFilter):
    title = _('event')
    parameter_name = 'event'
    
    def lookups(self, request, model_admin):
        #Only list events in the current timespan
        queryset = Event.objects
        if request.GET.has_key("when"):
            if request.GET["when"] == "future":
                queryset = queryset.filter(date__gte=datetime.date.today())
            elif request.GET["when"] == "past":
                queryset = queryset.filter(date__lt=datetime.date.today())
        return [(str(e.pk), e) for e in queryset.select_subclasses()]
        
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(event=self.value())
        
class FutureSignupFilter(DefaultListFilter):
    title = _('when')
    parameter_name = 'when'
    default = "future"
    
    def lookups(self, request, model_admin):
        return (
            ("all", _("All")),
            ("future", _("In the future")),
            ("past", _("In the past")),
        )
        
    def queryset(self, request, queryset):
        if self.value() == "future":
            return queryset.filter(event__date__gte=datetime.date.today())
        elif self.value() == "past":
            return queryset.filter(event__date__lt=datetime.date.today())

class SignupAdmin(admin.ModelAdmin):
    list_display = ("user", "event", "coming", "car", "comment", "last_modified")
    list_filter = (FutureSignupFilter, EventListFilter, "coming", "car")
    def list_mail(self, request, queryset):
        self.message_user(request, u";".join(signup.user.email for signup in queryset))
    actions = ["list_mail"]

admin.site.register(Signup, SignupAdmin)

from feincms.admin import item_editor 

class AlbumAdmin(item_editor.ItemEditor):
    pass
    
admin.site.register(Album,AlbumAdmin)


