from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from django.views.generic.simple import direct_to_template
admin.autodiscover()

urlpatterns = patterns('',
    (r'^workflow/', include('IssueTracker.workflow.urls')),
    (r'^admin/(.*)', admin.site.root),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^$', direct_to_template, {'template': 'base.html'}),
)

if settings.DEBUG:
    urlpatterns = patterns('',
            (r'^static/(?P<path>.*)$',
                'django.views.static.serve',
                {'document_root': settings.MEDIA_ROOT}),
        ) + urlpatterns
