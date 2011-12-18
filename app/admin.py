from django.contrib import admin
from django.db import models
from django import forms

from models import *
from widgets import RichEditor

from django.utils.translation import ugettext_lazy as _

import datetime
from django.conf import settings

class SignupInline(admin.TabularInline):
    model = Signup
    extra = 0
    
class DefaultListFilter(admin.SimpleListFilter):
    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup or (
                        self.value() is None and lookup==self.default),
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }
    def value(self):
        return self.used_parameters.get(self.parameter_name, self.default)
    
class FutureListFilter(DefaultListFilter):
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
    list_filter = (FutureListFilter,)
    
    
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
    list_filter = (FutureListFilter,)
    
admin.site.register(Gig, GigAdmin)

class EventListFilter(admin.SimpleListFilter):
    title = _('event')
    parameter_name = 'event'
    
    def lookups(self, request, model_admin):
        queryset = Event.objects
        if request.GET.has_key("when"):
            if request.GET["when"] == "future":
                queryset = queryset.filter(date__gte=datetime.date.today())
            elif request.GET["when"] == "past":
                queryset = queryset.filter(date__lt=datetime.date.today())
        return [(e.pk, e) for e in queryset.select_subclasses()]
        
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

class InitialFieldsMixin(object):
    def get_form(self, request, obj=None, **kwargs):
        form = admin.ModelAdmin.get_form(self, request, obj, **kwargs)
        if not hasattr(self.__class__, 'initial'):
            return form

        old_init = form.__init__
        def new_init(_self, *args, **kwargs):
            if 'instance' not in kwargs:
                for field_name, callback in self.__class__.initial.iteritems():
                    kwargs['initial'][field_name] = callback(self, request,
                                                             obj, **kwargs)
            return old_init(_self, *args, **kwargs)
        form.__init__ = new_init

        return form
    
from feincms.admin import item_editor 

class AlbumAdmin(item_editor.ItemEditor):
    pass
    
admin.site.register(Album,AlbumAdmin)

# User admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group

class GroupFilter(admin.SimpleListFilter):
    title = _('group')
    parameter_name = 'group'
    
    def lookups(self, request, model_admin):
        groups = Group.objects.all()
        return [(g.pk, g) for g in groups]
        
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(groups=self.value())

UserAdmin.fieldsets[1][1]["fields"] += ("address", "zip", "city", 
                                        "phone", "second_phone", 
                                        "nation", "instrument", "has_key", 
                                        "medals_earned", "medals_awarded")
UserAdmin.search_fields = ()

class ActiveFilter(DefaultListFilter):
    title = _('is active')
    parameter_name = 'active'
    default = "1"
    
    def lookups(self, request, model_admin):
        return (
            ("all", _("All")),
            ("1", _("is active")),
            ("0", _("not active")),
        )
        
    def queryset(self, request, queryset):
        if self.value() == "1":
            return queryset.filter(is_active=True)
        elif self.value() == "0":
            return queryset.filter(is_active=False)

def groups_display(user):
    return u", ".join(group.name for group in user.groups.all())
groups_display.short_description = _("groups")
    
UserAdmin.list_display =  ('first_name', 'last_name', "instrument", groups_display)
UserAdmin.list_filter = ('instrument', ActiveFilter, GroupFilter)
def list_mail(self, request, queryset):
    self.message_user(request, u";".join(user.email for user in queryset))
UserAdmin.actions = [list_mail]

# Page admin

from feincms.module.page.models import Page, PageAdmin
from guardian.admin import GuardedModelAdmin
PageAdmin.__bases__ = (GuardedModelAdmin,) + PageAdmin.__bases__
PageAdmin.unknown_fields.remove("require_login")
PageAdmin.unknown_fields.remove("require_permission")
PageAdmin.unknown_fields.remove("only_public")
PageAdmin.fieldsets[0][1]["fields"][1] += (
    "require_login","require_permission", "only_public")
PageAdmin.change_form_template = "admin/page_editor.html"


from feincms.admin import tree_editor
#PageAdmin.list_display.insert(3, tree_editor.ajax_editable_boolean('require_login', _('require login')))
PageAdmin.list_filter.insert(2, "require_login")

#admin.site.unregister(Page)
#admin.site.register(Page, PageAdmin)

# Media file admin
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from feincms.module.medialibrary.models import Category, MediaFileAdmin, MediaFile, MediaFileTranslation
from django.http import HttpResponseRedirect

@staticmethod
@csrf_protect
@permission_required('medialibrary.add_mediafile')
def bulk_upload(request):
    from django.core.urlresolvers import reverse
    from os import path

    if request.method == 'POST' and 'data' in request.FILES:

        category = None
        if request.POST.get('category'):
            category = Category.objects.get(pk=int(request.POST.get('category')))
            
        from django.template.defaultfilters import slugify
        from django.core.files.base import ContentFile
        
        for uploaded_file in request.FILES.getlist('data'):
            fname, ext = path.splitext(uploaded_file.name)
            target_fname = slugify(fname) + ext.lower()
            
            mf = MediaFile()
            mf.file.save(target_fname, uploaded_file)
            mf.save()
    
            if category:
                mf.categories.add(category)
    
            mt = MediaFileTranslation()
            mt.parent  = mf
            mt.caption = fname.replace('_', ' ')
            mt.save()

        messages.info(request, _("%d files imported") % len(request.FILES.getlist('data')))
    else:
        messages.error(request, _("No input file given"))
            
    return HttpResponseRedirect(reverse('admin:medialibrary_mediafile_changelist'))
MediaFileAdmin.bulk_upload = bulk_upload

class Media:
    js = (getattr(settings,'JQUERY_URL','js/jquery.js'),
          #"js/libs/jquery.html5_upload.js",
          "js/upload.js")
    
MediaFileAdmin.Media = Media

