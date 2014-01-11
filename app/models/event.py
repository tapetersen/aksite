#coding: utf-8
import datetime

from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from model_utils.managers import InheritanceManager
from django.utils.translation import ugettext_lazy as _
from collections import OrderedDict

from ..ak import section_choices

class Event(models.Model):   
    date = models.DateField(_("date"))
    time_location = models.TimeField(_("time location"), blank=True, null=True)
    info = models.TextField(_("info"), blank=True)
    
    objects = InheritanceManager()
    
    last_modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    name = "Event"

    # assumes objects annotated
    def get_signup(self, user):
        try:
            return self.user_signup
        except AttributeError:
            try:
                return Signup.objects.get(user=user, event=self)
            except Signup.DoesNotExist:
                return None
    
    def get_coming(self):
        try:
            return self.num_coming
        except AttributeError:
            return self.signup_set.filter(coming__in=[Signup.HOLE, Signup.DIRECT]).count()

    def get_signed_up(self):
        try:
            return self.event_ptr.signup__count
        except AttributeError:
            return self.signup_set.count()
    
    class Meta:
        ordering = ["date"]
        verbose_name = _("event")
        verbose_name_plural = _('events')
        app_label = "app"
    
    def __unicode__(self):
        name = self.name
        if self.__class__ == Event:
            if hasattr(self, "gig"):
                name = self.gig.name
            if hasattr(self, "rehearsal"):
                name = self.rehearsal.name
        return u"%s - %s" % (name, self.date)

class Rehearsal(Event):
    fika = models.CharField(_("fika"), max_length=2, choices=section_choices)
    
    location = models.CharField(_("location"), max_length=128, default=u"Hålan")
    time_hole = models.TimeField(_("time hole"), default=datetime.time(19,00))
    signup = models.BooleanField(_("signup"), default=False)
            
    name = u"Rep"
    
    def isGig(self): return False
    
    def present(self, request):
        columns = ([],[],[])
        columns[0].append()
    
    class Meta:
        verbose_name = _("rehearsal")
        verbose_name_plural = _('rehearsals')
        app_label = "app"


class Gig(Event):
    name = models.CharField(_("name"), max_length=128)
    time_playing = models.TimeField(_("time playing"), blank=True, null=True)
    
    location = models.CharField(_("location"), max_length=128, blank=True, null=True)
    time_hole = models.TimeField(_("time hole"), blank=True, null=True)
    signup = models.BooleanField(_("signup"), default=True)
    
    public_info = models.TextField(_("public info"), blank=True)
    
    secret = models.BooleanField(_("secret"), default=False)
        
    def isGig(self): return True
    
    class Meta:
        verbose_name = _("gig")
        verbose_name_plural = _('gigs')
        app_label = "app"

class Signup(models.Model):
    objects = InheritanceManager()

    user = models.ForeignKey(User)
    event = models.ForeignKey(Event, editable=False)

    HOLE = 'H'
    DIRECT = 'D'
    NOT_COMING = 'I'
    COMING_CHOICES = (
        (HOLE, u"Kommer till hålan"),
        (DIRECT, u"Kommer direkt"),
        (NOT_COMING, u"Kan inte komma"),
    )
    coming = models.CharField(_("coming"), max_length=1, choices=COMING_CHOICES, default="H")

    car = models.BooleanField(_("can bring car"))
    own_instrument = models.BooleanField(_("brings own instrument"))
    comment = models.CharField(_("comment"), max_length=128, blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ("user", "event")
        
        verbose_name = _("signup")
        verbose_name_plural = _('signups')
        app_label = "app"


def get_upcoming_events(user=None):
    events = OrderedDict( (e.pk, e) for e in
        Event.objects.filter(
            date__gte=datetime.date.today())
        .annotate(Count('signup'))
        .select_subclasses())

    # get number coming
    tmp = (Event.objects.filter(pk__in=events.keys())
        .filter(signup__coming__in=[Signup.HOLE, Signup.DIRECT])
        .annotate(num_coming=Count('signup')))
    for e in tmp:
        events[e.pk].num_coming = e.num_coming

    if user is not None:
        # get if user has signed up
        tmp = user.signup_set.filter(
            event_id__in=events.keys())

        for e in events.values():
            e.user_signup = None
        for s in tmp:
            events[s.event_id].user_signup = s

    return events.values()

