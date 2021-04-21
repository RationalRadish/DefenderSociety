# -*- coding: utf-8 -*-

from django.urls import path, include
# from .views import goview
from .views import *
from django.views.decorators.cache import cache_page

from django.views.generic import TemplateView


urlpatterns = [
    # path('go/', goview, name='go'), # Test page
    path('', IndexView.as_view(), name='index'),  # homepage, natural sort
    path('hot/', IndexView.as_view(), {'sort': 'v'}, name='index_hot'),  # Home page, sorted by page views
    path('article/<slug:slug>/', DetailView.as_view(), name='detail'),  # Article content page
    path('category/<slug:slug>/', CategoryView.as_view(), name='category'),
    path('category/<slug:slug>/hot/', CategoryView.as_view(), {'sort': 'v'},
         name='category_hot'),
    path('tag/<slug:slug>/', TagView.as_view(), name='tag'),
    path('tag/<slug:slug>/hot/', TagView.as_view(), {'sort': 'v'}, name='tag_hot'),
    path('about/', AboutView, name='about'),  # About
    path('eligibility/', EligibleView, name='eligibility'),  # eligibility
    path('Contact/', ContactView.as_view(), name='contact'),  # Contact Us page
    path('search/', MySearchView.as_view(), name='search_view'),  # Full text search
    path('event/calendar/', CalendarView.as_view(), name='calendar'),
    path('event/new/', create_event, name='event_new'),
    path('event/edit/<int:pk>/', EventEdit.as_view(), name='event_edit'),
    path('event/<int:event_id>/details/', event_details, name='event-detail'),
    path('add_eventmember/<int:event_id>', add_eventmember, name='add_eventmember'),
    path('event/<int:pk>/remove', EventMemberDeleteView.as_view(), name="remove_event"),
 #   path('instagram-gallery/', include('gallery.urls'))
    
]