from django.views.generic import ListView
from models import CalendarEntry, Kamerer
from feincms.module.page.models import Page
import datetime

class FeinListView(ListView):
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(FeinListView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['feincms_page'] = Page.objects.for_request(self.request, best_match=True)
        return context

class Upcoming(FeinListView):
    context_object_name = "entry_list"
    template_name = "upcoming.html"
    queryset = CalendarEntry.objects.filter(date__gte=datetime.date.today()).select_subclasses()
    
        
class AddressRegister(FeinListView):
    context_object_name = "kamerers"
    template_name = "address_register.html"
    queryset = Kamerer.objects.all().order_by("instrument", 
                                              "user__last_name", 
                                              "user__first_name")