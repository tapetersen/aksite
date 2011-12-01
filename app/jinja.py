from feincms.module.page.models import Page
from collections import OrderedDict, namedtuple

__all__ = ["navigation", "is_equal_or_parent_of"]

PageTuple = namedtuple("PageTuple", "tree_id lft rght title parent url children")

def navigation(request):
    """Get all pages with one query, then aranges in a tree."""
    
    pages = Page.objects.active().filter(in_navigation=True)
    if not request.user.is_authenticated():
        pages = pages.filter(require_login=False)
        
    tree = []
    tree_dict = {None:tree} # References the same list
    
    page_dict = OrderedDict() # To keep order of the pages
    for p in pages:
        page_dict[p.id] = PageTuple(tree_id=p.tree_id,
                                         lft=p.lft,
                                         rght=p.rght, 
                                         title=p.title, 
                                         parent=p.parent.id if p.parent else None,
                                         url=p.get_absolute_url(), 
                                         children=[])
    
    while page_dict:
        for i, page in page_dict.items():
            if page.parent in tree_dict:
                tree_dict[page.parent].append(page)
                tree_dict[i] = page.children
                del page_dict[i]
    
    return tree

def is_equal_or_parent_of(page1, page2):
    return page1.tree_id == page2.tree_id and page1.lft <= page2.lft and page1.rght >= page2.rght

