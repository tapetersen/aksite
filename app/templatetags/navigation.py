from django import template
from django.http import HttpRequest
from feincms.module.page.models import Page
from feincms.utils.templatetags import *

register = template.Library()

import logging
logger = logging.getLogger("aksite")

class NavigationNode(SimpleAssignmentNodeWithVarAndArgs):
    def what(self, request, args):
        level = int(args.get('level', 1))
        depth = int(args.get('depth', 1))
        mptt_limit = level + depth - 1 # adjust limit to mptt level indexing

        
        #logger.info(repr(dir(Page)))
        
        if level <= 1:
            if depth == 1:
                entries = Page.objects.toplevel_navigation()
            else:
                raise NotImplementedError()
            if not request.user.is_authenticated():
                entries = entries.filter(require_login=False)
        else:
            raise NotImplementedError()
                
        return entries
        
register.tag('navigation', do_simple_assignment_node_with_var_and_args_helper(NavigationNode))
        