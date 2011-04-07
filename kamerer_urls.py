from django.conf.urls.defaults import *
#from django.contrib.auth.models import User
from core.models import Kamerer

info_dict = {
    'queryset': Kamerer.objects.all().order_by("instrument"),
}

urlpatterns = patterns('',
    url(r'^$',
        'feincms.views.generic.list_detail.object_list',
        info_dict,
        name = "kamerer_list"),
)
