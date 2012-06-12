from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from vortraege.models import Talk
from textwrap import wrap

from django.template import Context, loader
from django.http import HttpResponse
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import BaseDetailView
from django.views.generic import TemplateView

from icalendar import Event
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

def convert_to_pdf(svg, response):
    cairosvg.svg2pdf(bytestring=svg.encode('utf-8'), write_to=response)
    
def render_svg_poster(talk):
    template = loader.get_template('vortraege/aushang.svg')
    c = Context({'talk': talk})
    return template.render(c)    

def pdf_poster(request, talk_id):
    t = get_object_or_404(Talk, pk=talk_id)

    rendered = render_svg_poster(t)

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition']  = 'attachment; filename=aushang-%s.pdf'%t.start.strftime('%Y%m')
    convert_to_pdf(rendered, response)
    return response

def render_svg_flyer(talk):
    template = loader.get_template('vortraege/flyer.svg')
    c = Context({'talk': talk})
    return template.render(c)    
    
def pdf_flyer(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    rendered = render_svg_flyer(talk)

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition']  = 'attachment; filename=flyer-%s.pdf'%talk.start.strftime('%Y%m')
    convert_to_pdf(rendered, response)
    return response



