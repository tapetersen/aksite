from django.conf.urls.defaults import *
from core.models import Kamerer

info_dict = {
    'queryset': Kamerer.objects.all().order_by("instrument", 
                                               "user__last_name", 
                                               "user__first_name"),
}

urlpatterns = patterns('',
    url(r'^$',
        'feincms.views.generic.list_detail.object_list',
        info_dict,
        name = "kamerer_list"),
)
