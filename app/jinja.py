from feincms.module.page.models import Page
from guardian.shortcuts import get_objects_for_user
from mptt.utils import tree_item_iterator

__all__ = ["navigation", "is_equal_or_parent_of"]


def navigation(request):
    """Get all pages with one query, then aranges in a tree."""
    
    pages = Page.objects.active().filter(in_navigation=True)
    if not request.user.is_authenticated():
        pages = pages.filter(require_login=False)
    else:
        allpages = pages.filter(only_public=False)
        pages = list(allpages.filter(require_permission=False))
        pages += list(get_objects_for_user(request.user, "page.can_view", 
                     allpages.filter(require_permission=True)))
        pages.sort(key=lambda p: (p.tree_id, p.lft))
        
    return tree_item_iterator(pages)

def is_equal_or_parent_of(page1, page2):
    return page1.tree_id == page2.tree_id and page1.lft <= page2.lft and page1.rght >= page2.rght

