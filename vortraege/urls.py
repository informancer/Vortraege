from django.conf.urls import patterns, include, url

urlpatterns = patterns('vortraege.views',
    url(r'^$', 'index'),
    url(r'^(?P<vortrag_id>\d+)/$', 'details', name='details') ,
    url(r'^(?P<vortrag_id>\d+)/ical/$', 'vevent', name='ical') ,
    url(r'^(?P<vortrag_id>\d+)/pressetext/$', 'pressetext') ,
    url(r'^(?P<vortrag_id>\d+)/aushang/$', 'pdf_aushang') ,
    url(r'^(?P<vortrag_id>\d+)/aushang/preview/$', 'svg_aushang'), 
    url(r'^(?P<vortrag_id>\d+)/flyer/$', 'pdf_flyer'),
    url(r'^(?P<vortrag_id>\d+)/flyer/preview/$', 'svg_flyer'), 
)
