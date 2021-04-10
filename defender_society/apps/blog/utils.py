from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Event
from defender_society.helper import get_current_user

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events):
        events_per_day = events.filter(start_time__day=day)
        d = ''
        
        for event in events_per_day:
            d += f'<li> {event.get_html_url} </li>'
        
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    # formats a week as a tr 
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)
        cal = f'<div class="container">'
        cal += f'<table class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        cal += '<br>'
        cal += '</div>'
        return cal

def site_protocol():
    '''
    Return the currently used protocol http|https, which can be called to many places where the full address of the website is needed
    :return: current agreement
    '''
    protocol = getattr(settings,'PROTOCOL_HTTPS','http')
    return protocol


def site_domain():
    '''
    Get the domain name of the current site, this domain name is actually to read the sites table of the database
    SITE_ID needs to be configured in the settings configuration, and django.contrib.sites needs to be added in INSTALLED_APPS
   :return: current site domain name
    '''
    if not django_apps.is_installed('django.contrib.sites'):
        raise ImproperlyConfigured("get site_domain requires django.contrib.sites, which isn't installed.")

    Site = django_apps.get_model('sites.Site')
    current_site = Site.objects.get_current()
    domain = current_site.domain
    return domain


def site_full_url():
    '''
    Return the full address of the current site, agreement + domain name
    :return:
    '''
    protocol = site_protocol()
    domain = site_domain()
    return'{}://{}'.format(protocol, domain)