from django.db import models
from django.contrib.auth.models import User

from app.ak import instrument_choices

from django.utils.translation import ugettext_lazy as _

User.__unicode__ = lambda self: u"%s %s" % (self.first_name, self.last_name)
User._meta.fields[2].blank = False # First name
User._meta.fields[3].blank = False # Last name
User._meta.fields[4].blank = False # Email
User.add_to_class("address", models.CharField(_("address"), max_length=128, blank=True, null=True))
User.add_to_class("zip", models.CharField(_("zip"), max_length=5, blank=True, null=True))
User.add_to_class("city", models.CharField(_("city"), max_length=128, blank=True, null=True))
User.add_to_class("phone", models.CharField(_("phone"), max_length=16, blank=True, null=True))
User.add_to_class("second_phone", models.CharField(_("second phone"), max_length=16, blank=True, null=True))
User.add_to_class("nation", models.CharField(_("nation"), max_length=128, blank=True, null=True))
User.add_to_class("instrument", models.CharField(_("instrument"), max_length=2, choices=instrument_choices))
User.add_to_class("has_key", models.BooleanField(_("has key"), default=False))
User.add_to_class("medals_earned", models.IntegerField(_("medals earned"), default=0))
User.add_to_class("medals_awarded", models.IntegerField(_("medals awarded"), default=0))