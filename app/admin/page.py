from feincms.module.page.admin import PageAdmin
from feincms.module.page.models import Page
from guardian.admin import GuardedModelAdmin

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

PageAdmin.__bases__ = (GuardedModelAdmin,) + PageAdmin.__bases__
PageAdmin.fieldsets[0][1]["fields"][1] += (
    "require_login","require_permission", "only_public")
PageAdmin.change_form_template = "admin/page_editor.html"


from feincms.admin import tree_editor
PageAdmin.list_display[3:0] = ["require_login_toggle", "only_public_toggle"]
PageAdmin.list_filter.insert(2, "require_login")

PageAdmin.require_login_toggle = tree_editor.ajax_editable_boolean('require_login', _('require login'))
PageAdmin.only_public_toggle = tree_editor.ajax_editable_boolean('only_public', _('only public'))

admin.site.unregister(Page)
admin.site.register(Page, PageAdmin)

