from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models

from ..models.models import Album
from ..models.event import Event, Signup, Rehearsal, Gig

from .widgets import RichEditor
from .util import DefaultListFilter

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
            "time_hole", "time_location", "time_playing", ("signup", "secret"),
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

        when = request.GET.get("when", "future")

        if when == "future":
            queryset = queryset.filter(date__gte=datetime.date.today())
        elif when == "past":
            queryset = queryset.filter(date__lt=datetime.date.today())
        elif when == "all":
            return []

        return [(str(e.pk), e) for e in queryset.select_subclasses()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(event=self.value())

class UserFilter(admin.SimpleListFilter):
    title = _('user')
    parameter_name = 'user'

    def lookups(self, request, model_admin):
        queryset = User.objects.filter(is_active=True).order_by("first_name", "last_name")

        return [(str(e.pk), e) for e in queryset]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user=self.value())

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
    list_display = ("user", "event", "coming", "own_instrument", "car", "comment", "created", "last_modified")
    list_filter = (FutureSignupFilter, "coming", "car", EventListFilter, UserFilter)
    def list_mail(self, request, queryset):
        self.message_user(request, u";".join(signup.user.email for signup in queryset))
    actions = ["list_mail"]

    def get_queryset(self, request):
        qs = super(admin.ModelAdmin, self).get_queryset(request)
        #qs.subclasses = ("event__rehearsal", "event__gig")
        return qs.select_related("user", "event__rehearsal", "event__gig")

admin.site.register(Signup, SignupAdmin)

from feincms.admin import item_editor 

class AlbumAdmin(item_editor.ItemEditor):
    pass
    
admin.site.register(Album,AlbumAdmin)


