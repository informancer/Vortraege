from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from vortraege.views import AttachmentDetailView
from vortraege.models import Talk

urlpatterns = patterns('vortraege.views',
    url(r'^$', 
        ListView.as_view(
            queryset = Talk.objects.all().order_by('start'),
            context_object_name='talks_list',
            template_name='vortraege/index.html'),
        name='vortraege_index'),
    url(r'^(?P<pk>\d+)/$', 
        DetailView.as_view(
            model = Talk,
            template_name = 'vortraege/details.html'), 
        name='vortraege_details'),
    url(r'^(?P<talk_id>\d+)/ical/$', 'vevent', name='vortraege_ical') ,
    url(r'^(?P<pk>\d+)/pressetext/$', 
        AttachmentDetailView.as_view(
            model = Talk,
            template_name = 'vortraege/pressetext.txt',
            content_type = 'text/plain; charset=utf-8',
            filename_prefix = 'pressetext',
            filename_suffix = 'txt'),
        name='vortraege_pressetext'),
    url(r'^(?P<talk_id>\d+)/aushang/$', 'pdf_poster', name='vortraege_pdf_poster') ,
    url(r'^(?P<pk>\d+)/aushang/preview/$', 
        AttachmentDetailView.as_view(
            model = Talk,
            template_name = 'vortraege/aushang.svg',
            content_type = 'image/svg+xml; charset=utf-8',
            filename_prefix = 'flyer',
            filename_suffix = 'svg'), 
        name='vortraege_svg_poster'), 
    url(r'^(?P<talk_id>\d+)/flyer/$', 'pdf_flyer', name='vortraege_pdf_flyer'),
    url(r'^(?P<talk_id>\d+)/flyer/preview/$', 'svg_flyer', name='vortraege_svg_flyer'), 
)
