# coding: utf-8
import datetime
from icalendar import Calendar, Event

import re
import app.models.event
from django.http import HttpResponse

def item_start(item):
    time = item.time_hole
    if time is None:
        time = item.time_location
    if time is None and hasattr(item, "time_playing"):
        time = item.time_playing
    if time is None:
        time = datetime.time(12, 00)

    return datetime.datetime.combine(item.date, time)

def item_html_description(item):
    html = u""
    if item.time_hole is not None:
        html += u"<p>Hålan: %s</p>" % item.time_hole
    if item.time_location is not None:
        html += u"<p>Där: %s</p>" % item.time_location
    if hasattr(item, "time_playing") and item.time_playing is not None:
        html += u"<p>Spelning börjar: %s</p>" % item.time_playing
    return html + item.info

def item_description(item):
    desc = item_html_description(item)
    desc = desc.replace("</p", "\n</p")
    desc = desc.replace("</br", "\n</br")
    return re.sub(r"<[^>]*>", "", desc)

def item_uid(item):
    return "event-%d@altekamereren.org" % item.pk

def cal_events(request, *args, **kwargs):
    cal = Calendar()

    cal.add("prodid", "-//AkCalendar//altekamereren.org")
    cal.add("version",  "2.0")

    cal.add("X-WR-CALDESC", "Alte Kamererens eventkalender")
    cal.add("X-WR-CALNAME", "AKcal")
    cal.add("X-WR-TIMEZONE", "Europe/Stockholm")

    items = app.models.event.Event.objects.filter(
        date__gte=datetime.date.today() - datetime.timedelta(days=30)
    ).select_subclasses()

    for item in items:
        event = Event()
        event.add("uid", item_uid(item))
        event.add("summary", item.name)
        event.add("dtstart", item_start(item))
        event.add("duration", datetime.timedelta(hours=2))
        event.add('created', item.created)
        event.add('last-modified', item.last_modified)
        event.add('description', item_description(item))
        event.add('X-ALT-DESC;FMTTYPE=text/html', item_html_description(item))
        event.add('location', item.location)
        cal.add_component(event)

    response = HttpResponse(cal.to_ical(), mimetype='text/calendar; charset=utf-8')
    filename = "events.ics"
    # following added for IE
    response['Filename'] = filename
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    response["Cache-Control"] = "no-cache, must-revalidate"
    response["Expires"] = "Sat, 26 Jul 1997 05:00:00 GMT"
    return response

