from vortraege.models import Talk

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from icalendar import Event

from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import BaseDetailView

import cairosvg

class AttachmentResponseMixin(TemplateResponseMixin):
    content_type = None
    filename_prefix = None
    filename_suffix = None

    def render_to_response(self, context, **response_kwargs):
        if self.content_type is None:
            raise ImproperlyConfigured(
                "AttachmentResponseMixin requires a definition of 'content_type'")
        response = super(AttachmentResponseMixin, self).render_to_response(context, 
                                                                          **response_kwargs)
        
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



class PdfAttachmentResponseMixin(AttachmentResponseMixin):
    @staticmethod
    def convert_to_pdf(response):
        response.content = cairosvg.svg2pdf(bytestring=response.content)
        return response

    def render_to_response(self, context, **response_kwargs):
        response = super(PdfAttachmentResponseMixin, self).render_to_response(context, 
                                                                           **response_kwargs)
        response.add_post_render_callback(self.convert_to_pdf)
        return response

# Create your views here.
class AttachmentDetailView(AttachmentResponseMixin, BaseDetailView):
    pass

class PdfAttachmentDetailView(PdfAttachmentResponseMixin, BaseDetailView):
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

