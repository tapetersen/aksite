from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group

from .util import DefaultListFilter

from django.utils.translation import ugettext_lazy as _

class GroupFilter(admin.SimpleListFilter):
    title = _('group')
    parameter_name = 'group'
    
    def lookups(self, request, model_admin):
        groups = Group.objects.all()
        return [(str(g.pk), g) for g in groups]
        
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
UserAdmin.list_filter = ('instrument', ActiveFilter, GroupFilter, "is_staff", "is_superuser", "has_key")
def list_mail(self, request, queryset):
    self.message_user(request, u";".join(user.email for user in queryset))
UserAdmin.actions = [list_mail]
