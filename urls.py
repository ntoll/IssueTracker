# Django
from django.conf.urls.defaults import *
from django.contrib import admin
import django.contrib.auth.views
from django.conf import settings
from django.views.generic.simple import direct_to_template
admin.autodiscover()

# Project
from IssueTracker.tracker.views import password_done, register, home

urlpatterns = patterns('',
    (r'^tickets/', include('IssueTracker.tracker.urls')),
    (r'^ticket/', include('IssueTracker.tracker.urls')),
    (r'^workflow/', include('IssueTracker.workflow.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^admin/(.*)', admin.site.root),
    (r'^faq$', direct_to_template, {'template': 'faq.html'}),
    (r'^login$', 'django.contrib.auth.views.login', 
        {'template_name':'login.html'}),
    (r'^exit$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    (r'^password/reset$', 'django.contrib.auth.views.password_reset',
        {'template_name':'password_reset_form.html',
        'email_template_name':'password_reset_email.html'}),
    (r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done',
        {'template_name':'password_reset_done.html'}),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'template_name':'password_reset_confirm.html'}),
    (r'^reset/done/$',
        'django.contrib.auth.views.password_reset_complete',
        {'template_name':'password_reset_complete.html'}),
    (r'^password$', 'django.contrib.auth.views.password_change',
        {'template_name':'password.html',
        'post_change_redirect':'/password_done'}),
    (r'^password_done$', password_done),
    (r'^signup$', register),
    (r'^signup_done$', direct_to_template, {'template': 'signup_done.html'}),
    (r'^$', home),
)

if settings.DEBUG:
    urlpatterns = patterns('',
            (r'^static/(?P<path>.*)$',
                'django.views.static.serve',
                {'document_root': settings.MEDIA_ROOT}),
        ) + urlpatterns
