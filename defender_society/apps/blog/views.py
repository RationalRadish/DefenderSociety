import calendar
#import datetime
import time
from datetime import datetime, date
from datetime import timedelta
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
import markdown
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.views import generic
from django.views.decorators.cache import cache_page
from haystack.generic_views import SearchView  # Import search view
from haystack.query import SearchQuerySet
from markdown.extensions.toc import TocExtension  # Anchor extension
from .utils import get_tweets
from .forms import EventForm, AddMemberForm
from .models import *
from .utils import Calendar
from .utils import site_full_url
import os
from django.views.decorators.cache import cache_page, never_cache


class CacheMixin(object):
    cache_timeout = 60

    def get_cache_timeout(self):
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        return cache_page(self.get_cache_timeout())(super(CacheMixin, self).dispatch)(*args, **kwargs)
# Create your views here.

#cache content all day
class ContactView(CacheMixin, generic.ListView):
    model = Article
    template_name = 'blog/contact.html'
    context_object_name = 'articles'
    paginate_by = 5
    paginate_orphans = 2
    cache_timeout = 150

class IndexView(CacheMixin, generic.ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'articles'
    paginate_by = getattr(settings, 'BASE_PAGE_BY', 5)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)
    cache_timeout = 100

    def get_ordering(self):
        sort = self.kwargs.get('sort')
        if sort == 'v':
            return ('-views', '-update_date', '-id')
        return ('-is_top', '-create_date')

    def get_context_data(self, **kwargs):
        context_data = super(IndexView, self).get_context_data()
        static_route = getattr(settings, 'MEDIA_ROOT')
        img_list = os.listdir(static_route + '/Instagram/')
        context_data['images'] = img_list
        context_data['tweets'] = get_tweets()
        return context_data



class DetailView(CacheMixin, generic.DetailView):
    model = Article
    template_name = 'blog/detail.html'
    context_object_name = 'article'
    cache_timeout = 200

    def get_object(self):
        obj = super(DetailView, self).get_object()
        # Set the time to judge the increase in page views, the same article is viewed twice for more than half an
        # hour before re-counting the number of views, the author ignores
        ud = obj.update_date.strftime("%Y%m%d%H%M%S")
        md_key = '{}_md_{}'.format(obj.id, ud)
        cache_md = cache.get(md_key)
        if cache_md:
            obj.body, obj.toc = cache_md
        else:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                TocExtension(slugify=slugify),
            ])
            obj.body = md.convert(obj.body)
            obj.toc = md.toc
            cache.set(md_key, (obj.body, obj.toc), 60 * 60 * 12)
        return obj


class CategoryView(CacheMixin, generic.ListView):
    model = Article
    template_name = 'blog/category.html'
    context_object_name = 'articles'
    paginate_by = getattr(settings, 'BASE_PAGE_BY', 5)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 2)
    cache_timeout = 200

    def get_ordering(self):
        ordering = super(CategoryView, self).get_ordering()
        sort = self.kwargs.get('sort')
        if sort == 'v':
            return '-views', '-update_date', '-id'
        return ordering

    def get_queryset(self, **kwargs):
        queryset = super(CategoryView, self).get_queryset()
        cate = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return queryset.filter(category=cate)

    def get_context_data(self, **kwargs):
        context_data = super(CategoryView, self).get_context_data()
        cate = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        context_data['search_tag'] = 'Article category'
        context_data['search_instance'] = cate
        return context_data


class TagView(CacheMixin, generic.ListView):
    model = Article
    template_name = 'blog/tag.html'
    context_object_name = 'articles'
    paginate_by = getattr(settings, 'BASE_PAGE_BY', 5)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 2)
    cache_timeout = 200

    def get_ordering(self):
        ordering = super(TagView, self).get_ordering()
        sort = self.kwargs.get('sort')
        if sort == 'v':
            return '-views', '-update_date', '-id'
        return ordering

    def get_queryset(self, **kwargs):
        queryset = super(TagView, self).get_queryset()
        tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        return queryset.filter(tags=tag)

    def get_context_data(self, **kwargs):
        context_data = super(TagView, self).get_context_data()
        tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        context_data['search_tag'] = 'Article tag'
        context_data['search_instance'] = tag
        return context_data

@cache_page(20000)
def AboutView(request):
    return render(request, 'blog/about.html', context={'body': ''})
@cache_page(20000)
def EligibleView(request):
    return render(request, 'blog/eligibility.html', context={'body': ''})


# Rewrite the search view, you can add some additional parameters, and you can redefine the name
class MySearchView(SearchView):
    context_object_name = 'search_list'
    template_name = 'blog/search.html'
    paginate_by = getattr(settings, 'BASE_PAGE_BY', 5)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 2)
    queryset = SearchQuerySet().order_by('-views')


def robots(request):
    site_url = site_full_url()
    return render(request, 'robots.txt', context={'site_url': site_url}, content_type='text/plain')


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


class CalendarView(LoginRequiredMixin, generic.ListView):
    model = Event
    template_name = 'blog/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def create_event(request):
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        Event.objects.get_or_create(
            user=request.user,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time
        )
        return HttpResponseRedirect(reverse('blog:calendar'))
    return render(request, 'blog/event.html', {'form': form})


class EventEdit(generic.UpdateView):
    model = Event
    fields = ['title', 'description', 'start_time', 'end_time']
    template_name = 'blog/event.html'


def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    eventmember = EventMember.objects.filter(event=event)
    context = {
        'event': event,
        'eventmember': eventmember
    }
    return render(request, 'blog/event-details.html', context)


def add_eventmember(request, event_id):
    forms = AddMemberForm()
    if request.method == 'POST':
        forms = AddMemberForm(request.POST)
        if forms.is_valid():
            member = EventMember.objects.filter(event=event_id)
            event = Event.objects.get(id=event_id)
            if member.count() <= 9:
                user = forms.cleaned_data['user']
                EventMember.objects.create(
                    event=event,
                    user=user
                )
                return redirect('blog:calendar')
            else:
                print('--------------User limit exceed!-----------------')
    context = {
        'form': forms
    }
    return render(request, 'blog/add_member.html', context)


class EventMemberDeleteView(generic.DeleteView):
    model = EventMember
    template_name = 'blog/event_delete.html'
    success_url = reverse_lazy('blog:calendar')
