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
