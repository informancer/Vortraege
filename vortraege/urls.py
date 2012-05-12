from django.conf.urls import patterns, include, url

urlpatterns = patterns('vortraege.views',
    url(r'^$', 'index', name='vortraege_index'),
    url(r'^(?P<talk_id>\d+)/$', 'details', name='vortraege_details') ,
    url(r'^(?P<talk_id>\d+)/ical/$', 'vevent', name='vortraege_ical') ,
    url(r'^(?P<talk_id>\d+)/pressetext/$', 'pressetext', name='vortraege_pressetext') ,
    url(r'^(?P<talk_id>\d+)/aushang/$', 'pdf_poster', name='vortraege_pdf_poster') ,
    url(r'^(?P<talk_id>\d+)/aushang/preview/$', 'svg_poster', name='vortraege_svg_poster'), 
    url(r'^(?P<talk_id>\d+)/flyer/$', 'pdf_flyer', name='vortraege_pdf_flyer'),
    url(r'^(?P<talk_id>\d+)/flyer/preview/$', 'svg_flyer', name='vortraege_svg_flyer'), 
)
