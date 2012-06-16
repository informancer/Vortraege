from vortraege.models import Talk

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from icalendar import Event

from django.core.exceptions import ImproperlyConfigured
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import BaseDetailView
from django.http import HttpResponse

import cairosvg

def convert_to_pdf(response):
    response.content = cairosvg.svg2pdf(bytestring=response.content)
    return response

class AttachmentResponseMixin(TemplateResponseMixin):
    fieldname = None
    content_type = None
    filename_prefix = None
    filename_suffix = None
    post_render_callbacks = []

    def render_to_response(self, context, **response_kwargs):
        if self.fieldname is None:
            raise ImproperlyConfigured(
                "AttachmentResponseMixin requires a definition of 'fieldname'")
        if self.content_type is None:
            raise ImproperlyConfigured(
                "AttachmentResponseMixin requires a definition of 'content_type'")
        attachment = getattr(context['object'], self.fieldname)
        if attachment:
            response = HttpResponse(attachment)
        else:
            response = super(AttachmentResponseMixin, self).render_to_response(context, 
                                                                               **response_kwargs)
            for callback in self.post_render_callbacks:
                response.add_post_render_callback(callback)
                
        response['Content-Type'] = self.content_type
        response['Content-Disposition']  = 'attachment; filename=%s'%self.get_filename(context)
        return response

    def get_filename(self, context):
        if self.filename_prefix is None:
            raise ImproperlyConfigured(
                "AttachmentResponseMixin requires a definition of 'filename_prefix'")
        if self.filename_suffix is None:
            raise ImproperlyConfigured(
                "AttachmentResponseMixin requires a definition of 'filename_suffix'")
        return '%s-%s.%s'%(self.filename_prefix,
                           context['object'].start.strftime('%Y%m'),
                           self.filename_suffix)

# Create your views here.
class AttachmentDetailView(AttachmentResponseMixin, BaseDetailView):
    pass

def vevent(request, talk_id):
    t = get_object_or_404(Talk, pk=talk_id)
    event = Event()
    event.add('description', t.title)
    ical = event.to_ical
    response = HttpResponse(ical, mimetype='text/calendar')
    response['Filename'] = 'filename.ics'  # IE needs this
    response['Content-Disposition'] = 'attachment; filename=talk-%s.ics'%t.start.strftime('%Y%m')
    return response

