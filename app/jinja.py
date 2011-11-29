from feincms.module.page.models import Page
from models import Signup

__all__ = ["navigation", "is_equal_or_parent_of"]

def navigation(request, parent=None):
    pages = Page.objects.active().filter(in_navigation=True, parent=parent)
    if not request.user.is_authenticated():
        pages.filter(require_login=False)
    return pages

def is_equal_or_parent_of(page1, page2):
    try:
        return page1.tree_id == page2.tree_id and page1.lft <= page2.lft and page1.rght >= page2.rght
    except AttributeError:
        return False

