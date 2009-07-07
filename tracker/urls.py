# Django
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

# Project
from IssueTracker.tracker.views import search, ajax_ticket_list, new_ticket, ticket, my_tickets

urlpatterns = patterns('',
    (r'^search$', search),
    (r'^ajax/search/$', ajax_ticket_list),
    (r'^new$', new_ticket),
    (r'^(?P<pk>[\d]+)$$', ticket),
    (r'^$', my_tickets),
)
